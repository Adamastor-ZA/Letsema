import type { Overrides } from '../../engine/scenarios'
import type { Formatter } from './format'

const points = (bps: number) => `${bps > 0 ? '+' : '−'}${Math.abs(bps) / 100}`

/** Percentage change for an income factor: 0.6 → −40%. */
export function factorToChangeBps(factor: number): number {
  return Math.round((factor - 1) * 10_000)
}

export function changeBpsToFactor(bps: number): number {
  return Math.max(0, Math.round((1 + bps / 10_000) * 10_000) / 10_000)
}

/** Plain-language list of what a set of overrides changes. */
type Named = { id: string; name: string }
export type NamedItems = Record<'assets' | 'debts' | 'obligations' | 'incomes' | 'events', Named[]>

export function describeOverrides(o: Overrides, dataset: NamedItems, fmt: Formatter): string[] {
  const out: string[] = []
  if (o.primeDeltaBps) out.push(`Prime ${points(o.primeDeltaBps)} points, variable-rate instalments recalculated`)
  const factor = (f: number | undefined, label: string) => {
    if (f === undefined || f === 1) return
    const change = factorToChangeBps(f)
    out.push(f === 0 ? `No ${label}` : `${label[0]!.toUpperCase()}${label.slice(1)} ${change > 0 ? '+' : '−'}${Math.abs(change) / 100}%`)
  }
  factor(o.variableIncomeFactor, 'variable income')
  factor(o.committedIncomeFactor, 'committed income')
  if (o.incomeGrowthDeltaBps) out.push(`Income growth ${points(o.incomeGrowthDeltaBps)} points a year`)
  if (o.obligationEscalationDeltaBps) out.push(`Obligations escalate ${points(o.obligationEscalationDeltaBps)} points a year`)
  if (o.investmentGrowthDeltaBps) out.push(`Investment and retirement growth ${points(o.investmentGrowthDeltaBps)} points a year`)
  if (o.haircutDeltaBps) out.push(`Haircuts ${points(o.haircutDeltaBps)} points`)
  if (o.excludedIds?.length) {
    const names = new Map<string, string>()
    for (const kind of ['assets', 'debts', 'obligations', 'incomes', 'events'] as const) for (const item of dataset[kind]) names.set(item.id, item.name)
    const known = o.excludedIds.map((id) => names.get(id)).filter((n): n is string => n !== undefined)
    if (known.length) out.push(`Leaves out ${known.join(', ')}`)
  }
  for (const e of o.extraEvents ?? []) {
    out.push(`${e.direction === 'inflow' ? 'Adds' : 'Pays'} ${e.name}: ${fmt.money(e.amountCents)} in ${fmt.month(e.month)}`)
  }
  return out
}
