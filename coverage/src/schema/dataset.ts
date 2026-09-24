import { z } from 'zod'
import type { ProjectionInputs } from '../engine/types'
import { PRESET_IDS, type PresetId } from '../engine/scenarios'
import {
  assetSchema,
  cents,
  debtSchema,
  eventSchema,
  incomeSchema,
  obligationSchema,
  rateBps,
  yearMonth,
  type AssetRecord,
  type DebtRecord,
  type EventRecord,
  type IncomeRecord,
  type ObligationRecord,
} from './entities'
import { settingsSchema, type Settings } from './settings'

export const SCHEMA_VERSION = 1

/** One colour slot per scenario; the base case takes the first palette colour. */
export const MAX_SCENARIOS = 7

const overridesSchema = z.object({
  primeDeltaBps: rateBps(-5_000, 5_000).optional(),
  variableIncomeFactor: z.number().min(0).max(10).optional(),
  committedIncomeFactor: z.number().min(0).max(10).optional(),
  incomeGrowthDeltaBps: rateBps(-5_000, 5_000).optional(),
  obligationEscalationDeltaBps: rateBps(-5_000, 5_000).optional(),
  investmentGrowthDeltaBps: rateBps(-5_000, 5_000).optional(),
  haircutDeltaBps: rateBps(-10_000, 10_000).optional(),
  excludedIds: z.array(z.string()).optional(),
  extraEvents: z.array(eventSchema.omit({ sortOrder: true })).optional(),
})

export const scenarioSchema = z.object({
  id: z.string().min(1),
  name: z.string().trim().min(1).max(120),
  presets: z.array(z.enum(PRESET_IDS as [PresetId, ...PresetId[]])),
  custom: overridesSchema,
  /** Included in comparisons and charts. */
  active: z.boolean(),
  /** Fixed colour slot (1–7), so a scenario keeps its colour whatever else is shown. */
  slot: z.number().int().min(1).max(MAX_SCENARIOS),
})
export type ScenarioRecord = z.output<typeof scenarioSchema>

export const snapshotSchema = z.object({
  id: z.string().min(1),
  month: yearMonth,
  takenAt: z.string(),
  assets: z.array(z.object({ assetId: z.string(), name: z.string(), tier: z.string(), valueCents: cents })),
  debts: z.array(z.object({ debtId: z.string(), name: z.string(), balanceCents: cents })),
  projected: z.array(
    z.object({ month: yearMonth, liquidCents: z.number().int(), netWorthCents: z.number().int(), debtCents: z.number().int() }),
  ),
  note: z.string().max(2000).optional(),
})
export type SnapshotRecord = z.output<typeof snapshotSchema>

export const datasetSchema = z
  .object({
    schemaVersion: z.literal(SCHEMA_VERSION),
    settings: settingsSchema,
    assets: z.array(assetSchema),
    debts: z.array(debtSchema),
    obligations: z.array(obligationSchema),
    incomes: z.array(incomeSchema),
    events: z.array(eventSchema),
    scenarios: z.array(scenarioSchema),
    snapshots: z.array(snapshotSchema),
  })
  .superRefine((d, ctx) => {
    const ids = new Set<string>()
    for (const kind of ['assets', 'debts', 'obligations', 'incomes', 'events', 'scenarios', 'snapshots'] as const) {
      d[kind].forEach((item, i) => {
        if (ids.has(item.id)) ctx.addIssue({ code: 'custom', path: [kind, i, 'id'], message: `Duplicate id ${item.id}` })
        ids.add(item.id)
      })
    }
    const slots = d.scenarios.map((s) => s.slot)
    if (new Set(slots).size !== slots.length) ctx.addIssue({ code: 'custom', path: ['scenarios'], message: 'Scenario colour slots must be unique' })
    const sweep = d.settings.sweepAssetId
    if (sweep !== null && !d.assets.some((a) => a.id === sweep && (a.tier === 'T1' || a.tier === 'T2'))) {
      ctx.addIssue({ code: 'custom', path: ['settings', 'sweepAssetId'], message: 'Sweep asset must be an existing T1 or T2 asset' })
    }
  })

export interface Dataset {
  schemaVersion: typeof SCHEMA_VERSION
  settings: Settings
  assets: AssetRecord[]
  debts: DebtRecord[]
  obligations: ObligationRecord[]
  incomes: IncomeRecord[]
  events: EventRecord[]
  scenarios: ScenarioRecord[]
  snapshots: SnapshotRecord[]
}

const bySortOrder = <T extends { sortOrder: number }>(items: T[]) => [...items].sort((a, b) => a.sortOrder - b.sortOrder)
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const strip = <T extends { sortOrder: number }>({ sortOrder, ...rest }: T) => rest

/** Build engine inputs from stored data, in list order. */
export function datasetToInputs(d: Pick<Dataset, 'settings' | 'assets' | 'debts' | 'obligations' | 'incomes' | 'events'>): ProjectionInputs {
  const s = d.settings
  return {
    asOfMonth: s.asOfMonth,
    horizonMonths: s.horizonYears * 12,
    primeBps: s.primeBps,
    cpiBps: s.cpiBps,
    sweepAssetId: s.sweepAssetId,
    includeT3InDrawdown: s.includeT3InDrawdown,
    overdraftBps: s.overdraftBps,
    assets: bySortOrder(d.assets).map(strip),
    debts: bySortOrder(d.debts).map(strip),
    obligations: bySortOrder(d.obligations).map(strip),
    incomes: bySortOrder(d.incomes).map(strip),
    events: bySortOrder(d.events).map(strip),
  }
}

/** Build a dataset from engine inputs (used for sample data). */
export function inputsToDataset(inputs: ProjectionInputs, base: Settings): Dataset {
  const withOrder = <T>(items: T[]) => items.map((item, sortOrder) => ({ ...item, sortOrder }))
  return {
    schemaVersion: SCHEMA_VERSION,
    settings: {
      ...base,
      asOfMonth: inputs.asOfMonth,
      horizonYears: Math.max(1, Math.round(inputs.horizonMonths / 12)),
      primeBps: inputs.primeBps,
      cpiBps: inputs.cpiBps,
      sweepAssetId: inputs.sweepAssetId,
      includeT3InDrawdown: inputs.includeT3InDrawdown,
      overdraftBps: inputs.overdraftBps,
      scenariosInitialised: true,
    },
    assets: withOrder(inputs.assets),
    debts: withOrder(inputs.debts),
    obligations: withOrder(inputs.obligations),
    incomes: withOrder(inputs.incomes),
    events: withOrder(inputs.events),
    scenarios: defaultScenarios(),
    snapshots: [],
  }
}

/** The three stress presets on their own and combined, all compared by default. */
export function defaultScenarios(): ScenarioRecord[] {
  return [
    { id: 'default-rate-shock', name: 'Rate shock', presets: ['rateShock'], custom: {}, active: true, slot: 1 },
    { id: 'default-variable-income-down', name: 'Variable income down 40%', presets: ['variableIncomeDown'], custom: {}, active: true, slot: 2 },
    { id: 'default-cost-escalation', name: 'Cost escalation', presets: ['costEscalation'], custom: {}, active: true, slot: 3 },
    {
      id: 'default-combined',
      name: 'Combined stress',
      presets: ['rateShock', 'variableIncomeDown', 'costEscalation'],
      custom: {},
      active: true,
      slot: 4,
    },
  ]
}
