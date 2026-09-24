import type { Asset, Debt, Income, Obligation, OneOffEvent, ProjectionInputs, ProjectionResult, Tier } from '../types'

export function inputs(p: Partial<ProjectionInputs> = {}): ProjectionInputs {
  return {
    asOfMonth: '2026-01',
    horizonMonths: 12,
    primeBps: 1000,
    cpiBps: 500,
    assets: [],
    debts: [],
    obligations: [],
    incomes: [],
    events: [],
    sweepAssetId: null,
    includeT3InDrawdown: false,
    overdraftBps: 0,
    ...p,
  }
}

export function asset(id: string, tier: Tier, valueCents: number, extra: Partial<Asset> = {}): Asset {
  return { id, name: id, tier, valueCents, growthBps: 0, ...extra }
}

export function fixedDebt(id: string, balanceCents: number, rateBps: number, instalmentCents: number, endMonth: string): Debt {
  return { id, name: id, balanceCents, rateType: 'fixed', fixedRateBps: rateBps, primeMarginBps: 0, instalmentCents, endMonth }
}

export function variableDebt(id: string, balanceCents: number, marginBps: number, instalmentCents: number, endMonth: string): Debt {
  return { id, name: id, balanceCents, rateType: 'variable', fixedRateBps: 0, primeMarginBps: marginBps, instalmentCents, endMonth }
}

export function obligation(id: string, amountCents: number, extra: Partial<Obligation> = {}): Obligation {
  return {
    id,
    name: id,
    amountCents,
    frequency: 'monthly',
    paymentMonth: 1,
    escalationBps: 0,
    escalationMonth: 1,
    startMonth: '2000-01',
    endMonth: null,
    ...extra,
  }
}

export function income(id: string, amountCents: number, extra: Partial<Income> = {}): Income {
  return {
    id,
    name: id,
    amountCents,
    frequency: 'monthly',
    months: [],
    growthBps: 0,
    growthMonth: 1,
    startMonth: '2000-01',
    endMonth: null,
    confidence: 'committed',
    ...extra,
  }
}

export function event(id: string, month: string, amountCents: number, direction: OneOffEvent['direction']): OneOffEvent {
  return { id, name: id, month, amountCents, direction }
}

export function totalAssets(tiers: Record<Tier, number>): number {
  return tiers.T1 + tiers.T2 + tiers.T3 + tiers.T4
}

/** Every cent that moves is accounted for, and nothing goes negative. Returns a list of violations. */
export function checkInvariants(result: ProjectionResult): string[] {
  const errors: string[] = []
  let prev = result.opening
  for (const r of result.rows) {
    const assetChange = totalAssets(r.tiers) - totalAssets(prev.tiers)
    const deficitChange = r.deficitCents - prev.deficitCents
    const expected = r.netFlowCents + r.growthCents - r.haircutCents - r.deficitInterestCents
    if (assetChange - deficitChange !== expected) {
      errors.push(`${r.month}: cash not conserved (${assetChange - deficitChange} vs ${expected})`)
    }
    if (prev.debtCents + r.debtInterestCents - r.debtPaymentsCents !== r.debtCents) {
      errors.push(`${r.month}: debt roll-forward broken`)
    }
    if (r.deficitCents < 0) errors.push(`${r.month}: negative deficit`)
    if (Object.values(r.assetValues).some((v) => v < 0)) errors.push(`${r.month}: negative asset`)
    if (Object.values(r.debtBalances).some((v) => v < 0)) errors.push(`${r.month}: negative debt`)
    if (r.shortfall !== r.deficitCents > 0) errors.push(`${r.month}: shortfall flag mismatch`)
    prev = r
  }
  return errors
}
