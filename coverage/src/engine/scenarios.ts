import { adjustedInstalment } from './debt'
import { roundCents } from './money'
import { toIndex } from './month'
import type { OneOffEvent, ProjectionInputs } from './types'

/**
 * Adjustments applied to the base inputs. When combined, deltas add, factors
 * multiply, exclusions are pooled and extra events are appended.
 */
export interface Overrides {
  /** Shift in prime; moves variable-rate debt and recalculates its instalment. */
  primeDeltaBps?: number
  /** Multiplier on variable income amounts (0.6 is a 40% fall). */
  variableIncomeFactor?: number
  /** Multiplier on committed income amounts. */
  committedIncomeFactor?: number
  /** Added to every income stream's annual growth. */
  incomeGrowthDeltaBps?: number
  /** Added to every recurring obligation's annual escalation. */
  obligationEscalationDeltaBps?: number
  /** Added to the growth rate of T2 and T3 assets. */
  investmentGrowthDeltaBps?: number
  /** Added to T2 and T3 haircuts, clamped to 0–100%. */
  haircutDeltaBps?: number
  /** Ids of assets, debts, obligations, income streams or events to leave out. */
  excludedIds?: string[]
  extraEvents?: OneOffEvent[]
}

export type PresetId = 'rateShock' | 'variableIncomeDown' | 'costEscalation'

export interface Preset {
  id: PresetId
  label: string
  description: string
  overrides: Overrides
}

export const PRESETS: Record<PresetId, Preset> = {
  rateShock: {
    id: 'rateShock',
    label: 'Rate shock',
    description: 'Prime +200 bps on variable-rate debt; instalments recalculated over the remaining term.',
    overrides: { primeDeltaBps: 200 },
  },
  variableIncomeDown: {
    id: 'variableIncomeDown',
    label: 'Variable income down 40%',
    description: 'Every income stream marked variable pays 60% of its amount.',
    overrides: { variableIncomeFactor: 0.6 },
  },
  costEscalation: {
    id: 'costEscalation',
    label: 'Cost escalation',
    description: '+3 percentage points on the annual escalation of every recurring obligation.',
    overrides: { obligationEscalationDeltaBps: 300 },
  },
}

export const PRESET_IDS = Object.keys(PRESETS) as PresetId[]

export interface ScenarioDefinition {
  id: string
  name: string
  presets: PresetId[]
  custom: Overrides
}

function addOpt(a: number | undefined, b: number | undefined): number | undefined {
  return a === undefined && b === undefined ? undefined : (a ?? 0) + (b ?? 0)
}

function mulOpt(a: number | undefined, b: number | undefined): number | undefined {
  return a === undefined && b === undefined ? undefined : (a ?? 1) * (b ?? 1)
}

export function combineOverrides(...list: Overrides[]): Overrides {
  return list.reduce<Overrides>(
    (acc, o) => ({
      primeDeltaBps: addOpt(acc.primeDeltaBps, o.primeDeltaBps),
      variableIncomeFactor: mulOpt(acc.variableIncomeFactor, o.variableIncomeFactor),
      committedIncomeFactor: mulOpt(acc.committedIncomeFactor, o.committedIncomeFactor),
      incomeGrowthDeltaBps: addOpt(acc.incomeGrowthDeltaBps, o.incomeGrowthDeltaBps),
      obligationEscalationDeltaBps: addOpt(acc.obligationEscalationDeltaBps, o.obligationEscalationDeltaBps),
      investmentGrowthDeltaBps: addOpt(acc.investmentGrowthDeltaBps, o.investmentGrowthDeltaBps),
      haircutDeltaBps: addOpt(acc.haircutDeltaBps, o.haircutDeltaBps),
      excludedIds: [...new Set([...(acc.excludedIds ?? []), ...(o.excludedIds ?? [])])],
      extraEvents: [...(acc.extraEvents ?? []), ...(o.extraEvents ?? [])],
    }),
    {},
  )
}

export function resolveOverrides(scenario: Pick<ScenarioDefinition, 'presets' | 'custom'>): Overrides {
  return combineOverrides(...scenario.presets.map((id) => PRESETS[id].overrides), scenario.custom)
}

const clampBps = (bps: number) => Math.min(10_000, Math.max(0, bps))

/** Apply overrides to a copy of the inputs. The inputs are not mutated. */
export function applyOverrides(inputs: ProjectionInputs, o: Overrides): ProjectionInputs {
  const excluded = new Set(o.excludedIds ?? [])
  const keep = <T extends { id: string }>(items: T[]) => items.filter((item) => !excluded.has(item.id))
  const primeDelta = o.primeDeltaBps ?? 0
  const asOf = toIndex(inputs.asOfMonth)
  const investmentDelta = o.investmentGrowthDeltaBps ?? 0
  const haircutDelta = o.haircutDeltaBps ?? 0

  return {
    ...inputs,
    primeBps: inputs.primeBps + primeDelta,
    sweepAssetId: inputs.sweepAssetId !== null && excluded.has(inputs.sweepAssetId) ? null : inputs.sweepAssetId,
    assets: keep(inputs.assets).map((a) => {
      if (a.tier !== 'T2' && a.tier !== 'T3') return { ...a }
      return {
        ...a,
        growthBps: a.growthBps + investmentDelta,
        haircutBps: clampBps((a.haircutBps ?? 0) + haircutDelta),
      }
    }),
    debts: keep(inputs.debts).map((d) => ({
      ...d,
      instalmentCents: adjustedInstalment(d, inputs.primeBps, primeDelta, asOf),
    })),
    obligations: keep(inputs.obligations).map((ob) => ({
      ...ob,
      escalationBps: ob.escalationBps + (o.obligationEscalationDeltaBps ?? 0),
    })),
    incomes: keep(inputs.incomes).map((i) => {
      const factor = (i.confidence === 'variable' ? o.variableIncomeFactor : o.committedIncomeFactor) ?? 1
      return {
        ...i,
        months: [...i.months],
        amountCents: roundCents(i.amountCents * factor),
        growthBps: i.growthBps + (o.incomeGrowthDeltaBps ?? 0),
      }
    }),
    events: [...keep(inputs.events), ...(o.extraEvents ?? [])].map((e) => ({ ...e })),
  }
}
