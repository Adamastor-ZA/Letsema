import { liquidBalance } from '../engine/metrics'
import { addMonths, monthsBetween, toIndex } from '../engine/month'
import { MAX_HORIZON_MONTHS, project } from '../engine/project'
import { rollForward, type RolledAmount } from '../engine/schedules'
import type { Position, YearMonth } from '../engine/types'
import { datasetToInputs, type Dataset, type SnapshotRecord } from '../schema/dataset'

/** Months of base-case path stored with each check-in. */
export const SNAPSHOT_PATH_MONTHS = 36

export interface CheckInInput {
  month: YearMonth
  assetValues: Record<string, number>
  debtBalances: Record<string, number>
  note?: string
  takenAt: string
}

export interface CheckInPlan {
  dataset: Dataset
  snapshot: SnapshotRecord
  rolled: RolledAmount[]
}

export interface Totals {
  liquidCents: number
  netWorthCents: number
  debtCents: number
}

const totals = (p: Position): Totals => ({ liquidCents: liquidBalance(p), netWorthCents: p.netWorthCents, debtCents: p.debtCents })

export interface ProjectedPosition extends Totals {
  assetValues: Record<string, number>
  debtBalances: Record<string, number>
}

/** What the current model expects at the start of `month`, or null outside the reachable range. */
export function projectedAt(dataset: Dataset, month: YearMonth): ProjectedPosition | null {
  const inputs = datasetToInputs(dataset)
  const offset = monthsBetween(inputs.asOfMonth, month)
  if (offset < 0 || offset > MAX_HORIZON_MONTHS) return null
  const result = project({ ...inputs, horizonMonths: Math.max(1, offset) })
  const p: Position = offset === 0 ? result.opening : result.rows[offset - 1]!
  return { ...totals(p), assetValues: p.assetValues, debtBalances: p.debtBalances }
}

/**
 * Apply a check-in to a dataset: record the actual balances, move the as-of
 * month forward (rolling obligation and income amounts forward with it) and
 * build the snapshot, including the base-case path projected from the new position.
 */
export function planCheckIn(dataset: Dataset, input: CheckInInput): CheckInPlan {
  const asOf = dataset.settings.asOfMonth
  if (toIndex(input.month) < toIndex(asOf)) throw new Error(`The model is already as of ${asOf}; a check-in cannot go back in time.`)

  const { inputs: rolledInputs, changes } = rollForward(datasetToInputs(dataset), input.month)
  const obligationAmount = new Map(rolledInputs.obligations.map((o) => [o.id, o.amountCents]))
  const incomeAmount = new Map(rolledInputs.incomes.map((i) => [i.id, i.amountCents]))

  const next: Dataset = {
    ...dataset,
    settings: { ...dataset.settings, asOfMonth: input.month },
    assets: dataset.assets.map((a) => {
      const valueCents = input.assetValues[a.id] ?? a.valueCents
      // The accessible part of a retirement asset cannot exceed what it is worth.
      const accessibleCents = a.accessibleCents === undefined ? undefined : Math.min(a.accessibleCents, valueCents)
      return { ...a, valueCents, ...(accessibleCents === undefined ? {} : { accessibleCents }) }
    }),
    debts: dataset.debts.map((d) => ({ ...d, balanceCents: input.debtBalances[d.id] ?? d.balanceCents })),
    obligations: dataset.obligations.map((o) => ({ ...o, amountCents: obligationAmount.get(o.id) ?? o.amountCents })),
    incomes: dataset.incomes.map((i) => ({ ...i, amountCents: incomeAmount.get(i.id) ?? i.amountCents })),
  }

  const result = project({ ...datasetToInputs(next), horizonMonths: SNAPSHOT_PATH_MONTHS - 1 })
  const projected = [
    { month: input.month, ...totals(result.opening) },
    ...result.rows.map((r, i) => ({ month: addMonths(input.month, i + 1), ...totals(r) })),
  ]
  const note = input.note?.trim()
  const snapshot: SnapshotRecord = {
    id: `snapshot-${input.month}`,
    month: input.month,
    takenAt: input.takenAt,
    assets: next.assets.map((a) => ({ assetId: a.id, name: a.name, tier: a.tier, valueCents: a.valueCents })),
    debts: next.debts.map((d) => ({ debtId: d.id, name: d.name, balanceCents: d.balanceCents })),
    actual: totals(result.opening),
    projected,
    ...(note ? { note } : {}),
  }
  const snapshots = [...dataset.snapshots.filter((s) => s.month !== input.month), snapshot].sort((a, b) => a.month.localeCompare(b.month))
  return { dataset: { ...next, snapshots }, snapshot, rolled: changes }
}

export type TrackedMetric = keyof Totals

export interface TrackingPoint {
  month: YearMonth
  actual?: number
  projected?: number
}

/**
 * Actuals from every check-in against the path projected at the baseline
 * check-in, from the baseline month to the later of the latest check-in and
 * twelve months on.
 */
export function trackAgainstBaseline(snapshots: SnapshotRecord[], baselineId: string, metric: TrackedMetric): TrackingPoint[] {
  const baseline = snapshots.find((s) => s.id === baselineId)
  if (!baseline) return []
  const byMonth = new Map<string, TrackingPoint>()
  const later = snapshots.filter((s) => s.month >= baseline.month)
  const last = later.reduce((m, s) => (s.month > m ? s.month : m), baseline.month)
  const yearOn = addMonths(baseline.month, 12)
  const end = last > yearOn ? last : yearOn
  for (const p of baseline.projected) {
    if (p.month > end) break
    byMonth.set(p.month, { month: p.month, projected: p[metric] })
  }
  for (const s of later) byMonth.set(s.month, { ...(byMonth.get(s.month) ?? { month: s.month }), actual: s.actual[metric] })
  return [...byMonth.values()].sort((a, b) => a.month.localeCompare(b.month))
}
