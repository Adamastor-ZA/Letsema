import { debtRateBps, stepDebt } from './debt'
import { applyBps, ceilDiv, roundCents } from './money'
import { fromIndex, toIndex, type MonthIndex } from './month'
import { monthlyEffective, monthlyNominal } from './rates'
import { incomeDue, obligationDue } from './schedules'
import type { Asset, Debt, FlowItem, MonthRow, ProjectOptions, OneOffEvent, Position, ProjectionInputs, ProjectionResult, Tier } from './types'

/** Id of the notional cash bucket used when there is no T1 asset to sweep into. */
export const UNALLOCATED_CASH_ID = '__unallocated_cash__'

export const MAX_HORIZON_MONTHS = 360

interface AssetState {
  asset: Asset
  value: number
  /** T3 only: accessible amount not yet withdrawn (gross). */
  accessible: number
}

interface DebtState {
  debt: Debt
  balance: number
  rateBps: number
  endIndex: MonthIndex
}

function haircutOf(asset: Asset): number {
  return Math.min(10_000, Math.max(0, asset.haircutBps ?? 0))
}

function accessibleGross(s: AssetState): number {
  return Math.min(s.accessible, s.value)
}

function position(assets: AssetState[], debts: DebtState[], deficit: number): Position {
  const tiers: Record<Tier, number> = { T1: 0, T2: 0, T3: 0, T4: 0 }
  const assetValues: Record<string, number> = {}
  let t2NetCents = 0
  let t3AccessibleNetCents = 0
  for (const s of assets) {
    tiers[s.asset.tier] += s.value
    assetValues[s.asset.id] = s.value
    if (s.asset.tier === 'T2') t2NetCents += s.value - applyBps(s.value, haircutOf(s.asset))
    if (s.asset.tier === 'T3') {
      const gross = accessibleGross(s)
      t3AccessibleNetCents += gross - applyBps(gross, haircutOf(s.asset))
    }
  }
  const debtBalances: Record<string, number> = {}
  let debtCents = 0
  for (const d of debts) {
    debtBalances[d.debt.id] = d.balance
    debtCents += d.balance
  }
  const liquidAssetsCents = tiers.T1 + t2NetCents + t3AccessibleNetCents
  const totalAssets = tiers.T1 + tiers.T2 + tiers.T3 + tiers.T4
  return {
    tiers,
    t2NetCents,
    t3AccessibleNetCents,
    liquidAssetsCents,
    debtCents,
    deficitCents: deficit,
    netWorthCents: totalAssets - debtCents - deficit,
    liquidNetWorthCents: liquidAssetsCents - debtCents - deficit,
    assetValues,
    debtBalances,
  }
}

/**
 * Raise up to `need` in cash by selling from a holding of `cap` (gross) that
 * loses `haircutBps` on sale. Sells the least gross value that covers the need.
 */
function sellWithHaircut(cap: number, haircutBps: number, need: number): { sold: number; cash: number } {
  const netAvailable = cap - applyBps(cap, haircutBps)
  if (netAvailable <= 0) return { sold: 0, cash: 0 }
  if (netAvailable <= need) return { sold: cap, cash: netAvailable }
  return { sold: Math.min(cap, ceilDiv(need * 10_000, 10_000 - haircutBps)), cash: need }
}

function groupEvents(events: OneOffEvent[]): Map<MonthIndex, OneOffEvent[]> {
  const byMonth = new Map<MonthIndex, OneOffEvent[]>()
  for (const e of events) {
    const m = toIndex(e.month)
    const list = byMonth.get(m)
    if (list) list.push(e)
    else byMonth.set(m, [e])
  }
  return byMonth
}

/**
 * Project month by month from the as-of month. Each month:
 * 1. add income due; 2. pay obligations; 3. accrue interest and pay debt
 * instalments (and interest on any carried deficit); 4. apply one-off events;
 * 5. grow assets; 6. repay any carried deficit from a surplus, then sweep the
 * rest into the sweep asset; 7. fund a shortfall from T1, then T2 net of
 * haircut (then accessible T3 if enabled), carrying anything unfunded forward.
 */
export function project(inputs: ProjectionInputs, options: ProjectOptions = {}): ProjectionResult {
  if (!Number.isInteger(inputs.horizonMonths) || inputs.horizonMonths < 1 || inputs.horizonMonths > MAX_HORIZON_MONTHS) {
    throw new Error(`Horizon must be 1–${MAX_HORIZON_MONTHS} months, got ${inputs.horizonMonths}`)
  }
  const asOf = toIndex(inputs.asOfMonth)

  const assets: AssetState[] = inputs.assets.map((asset) => ({
    asset,
    value: Math.max(0, asset.valueCents),
    accessible: asset.tier === 'T3' ? Math.max(0, asset.accessibleCents ?? 0) : 0,
  }))

  let sweep =
    assets.find((s) => s.asset.id === inputs.sweepAssetId && (s.asset.tier === 'T1' || s.asset.tier === 'T2')) ??
    assets.find((s) => s.asset.tier === 'T1')
  if (!sweep) {
    sweep = {
      asset: { id: UNALLOCATED_CASH_ID, name: 'Unallocated cash', tier: 'T1', valueCents: 0, growthBps: 0 },
      value: 0,
      accessible: 0,
    }
    assets.push(sweep)
  }

  const t1 = assets.filter((s) => s.asset.tier === 'T1')
  const t2 = assets.filter((s) => s.asset.tier === 'T2')
  const t3 = inputs.includeT3InDrawdown ? assets.filter((s) => s.asset.tier === 'T3') : []
  const monthlyGrowth = new Map(assets.map((s) => [s, monthlyEffective(s.asset.growthBps)]))

  const debts: DebtState[] = inputs.debts.map((debt) => ({
    debt,
    balance: Math.max(0, debt.balanceCents),
    rateBps: debtRateBps(debt, inputs.primeBps),
    endIndex: toIndex(debt.endMonth),
  }))

  const eventsByMonth = groupEvents(inputs.events)
  const overdraftRate = monthlyNominal(Math.max(0, inputs.overdraftBps))
  let deficit = 0

  const opening = position(assets, debts, deficit)
  const rows: MonthRow[] = []

  for (let index = 0; index < inputs.horizonMonths; index++) {
    const m = asOf + index
    const items: FlowItem[] | undefined = index < (options.detailMonths ?? 0) ? [] : undefined

    // 1. Income
    let committedIncomeCents = 0
    let variableIncomeCents = 0
    for (const income of inputs.incomes) {
      const amount = incomeDue(income, asOf, m)
      if (amount !== 0) items?.push({ kind: 'income', id: income.id, name: income.name, amountCents: amount, direction: 'in', confidence: income.confidence })
      if (income.confidence === 'committed') committedIncomeCents += amount
      else variableIncomeCents += amount
    }
    const incomeCents = committedIncomeCents + variableIncomeCents

    // 2. Recurring obligations
    let obligationsCents = 0
    for (const o of inputs.obligations) {
      const amount = obligationDue(o, asOf, m)
      if (amount !== 0) items?.push({ kind: 'obligation', id: o.id, name: o.name, amountCents: amount, direction: 'out' })
      obligationsCents += amount
    }

    // 3. Debts
    let debtPaymentsCents = 0
    let debtInterestCents = 0
    const debtsRetired: string[] = []
    for (const d of debts) {
      if (d.balance <= 0) continue
      const step = stepDebt(d.balance, d.rateBps, d.debt.instalmentCents, m >= d.endIndex)
      d.balance = step.balanceCents
      if (step.paymentCents !== 0) items?.push({ kind: 'debt', id: d.debt.id, name: d.debt.name, amountCents: step.paymentCents, direction: 'out' })
      debtPaymentsCents += step.paymentCents
      debtInterestCents += step.interestCents
      if (step.retired) debtsRetired.push(d.debt.id)
    }
    const deficitInterestCents = deficit > 0 ? roundCents(deficit * overdraftRate) : 0
    deficit += deficitInterestCents

    // 4. One-off events
    let oneOffInCents = 0
    let oneOffOutCents = 0
    for (const e of eventsByMonth.get(m) ?? []) {
      items?.push({ kind: 'event', id: e.id, name: e.name, amountCents: e.amountCents, direction: e.direction === 'inflow' ? 'in' : 'out' })
      if (e.direction === 'inflow') oneOffInCents += e.amountCents
      else oneOffOutCents += e.amountCents
    }

    const netFlowCents = incomeCents - obligationsCents - debtPaymentsCents + oneOffInCents - oneOffOutCents

    // 5. Growth
    let growthCents = 0
    for (const s of assets) {
      const next = Math.max(0, s.value + roundCents(s.value * (monthlyGrowth.get(s) ?? 0)))
      growthCents += next - s.value
      s.value = next
    }

    // 6 & 7. Settle the month's cash
    let deficitRepaidCents = 0
    let sweptCents = 0
    let drawnCents = 0
    let haircutCents = 0
    let newDeficitCents = 0
    if (netFlowCents >= 0) {
      deficitRepaidCents = Math.min(netFlowCents, deficit)
      deficit -= deficitRepaidCents
      sweptCents = netFlowCents - deficitRepaidCents
      sweep.value += sweptCents
    } else {
      let need = -netFlowCents
      for (const s of t1) {
        if (need === 0) break
        const take = Math.min(s.value, need)
        s.value -= take
        need -= take
        drawnCents += take
      }
      for (const s of t2) {
        if (need === 0) break
        const { sold, cash } = sellWithHaircut(s.value, haircutOf(s.asset), need)
        s.value -= sold
        need -= cash
        drawnCents += cash
        haircutCents += sold - cash
      }
      for (const s of t3) {
        if (need === 0) break
        const { sold, cash } = sellWithHaircut(accessibleGross(s), haircutOf(s.asset), need)
        s.value -= sold
        s.accessible -= sold
        need -= cash
        drawnCents += cash
        haircutCents += sold - cash
      }
      newDeficitCents = need
      deficit += need
    }

    rows.push({
      ...position(assets, debts, deficit),
      month: fromIndex(m),
      index,
      incomeCents,
      committedIncomeCents,
      variableIncomeCents,
      obligationsCents,
      debtPaymentsCents,
      debtInterestCents,
      oneOffInCents,
      oneOffOutCents,
      netFlowCents,
      growthCents,
      deficitInterestCents,
      drawnCents,
      haircutCents,
      deficitRepaidCents,
      sweptCents,
      newDeficitCents,
      debtsRetired,
      shortfall: deficit > 0,
      ...(items ? { items } : {}),
    })
  }

  return { opening, rows }
}
