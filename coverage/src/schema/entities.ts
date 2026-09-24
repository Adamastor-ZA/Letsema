import { z } from 'zod'
import { isYearMonth, toIndex } from '../engine/month'
import { TIERS, type Asset, type Debt, type Income, type Obligation, type OneOffEvent } from '../engine/types'

export const MAX_CENTS = 10_000_000_000_000 // R100 billion: far beyond any household, well inside safe integers

export const yearMonth = z
  .string()
  .refine((v) => isYearMonth(v) && toIndex(v) >= toIndex('1900-01') && toIndex(v) <= toIndex('2150-12'), {
    error: 'Enter a month as YYYY-MM',
  })
export const cents = z.number().int().min(0, { error: 'Cannot be negative' }).max(MAX_CENTS, { error: 'Too large' })
export const positiveCents = cents.refine((v) => v > 0, { error: 'Must be more than zero' })
export const rateBps = (min: number, max: number) =>
  z
    .number()
    .int()
    .min(min, { error: `Must be at least ${min / 100}%` })
    .max(max, { error: `Must be at most ${max / 100}%` })
export const calendarMonth = z.number().int().min(1).max(12)
const id = z.string().min(1)
const name = z.string().trim().min(1, { error: 'Give it a name' }).max(120, { error: 'Keep it under 120 characters' })
const sortOrder = z.number()

function endNotBeforeStart(v: { startMonth: string; endMonth: string | null }, ctx: z.RefinementCtx) {
  if (v.endMonth !== null && isYearMonth(v.startMonth) && isYearMonth(v.endMonth) && toIndex(v.endMonth) < toIndex(v.startMonth)) {
    ctx.addIssue({ code: 'custom', path: ['endMonth'], message: 'End month is before the start month' })
  }
}

export const assetSchema = z
  .object({
    id,
    name,
    tier: z.enum(TIERS),
    valueCents: cents,
    growthBps: rateBps(-10_000, 10_000),
    haircutBps: rateBps(0, 10_000).optional(),
    accessibleCents: cents.optional(),
    sortOrder,
  })
  .superRefine((v, ctx) => {
    if (v.tier === 'T3' && v.accessibleCents !== undefined && v.accessibleCents > v.valueCents) {
      ctx.addIssue({ code: 'custom', path: ['accessibleCents'], message: 'Cannot exceed the current value' })
    }
  })

export const debtSchema = z.object({
  id,
  name,
  balanceCents: cents,
  rateType: z.enum(['fixed', 'variable']),
  fixedRateBps: rateBps(0, 10_000),
  primeMarginBps: rateBps(-5_000, 5_000),
  instalmentCents: cents,
  endMonth: yearMonth,
  sortOrder,
})

export const obligationSchema = z
  .object({
    id,
    name,
    amountCents: positiveCents,
    frequency: z.enum(['monthly', 'annual']),
    paymentMonth: calendarMonth,
    escalationBps: rateBps(-5_000, 10_000),
    escalationMonth: calendarMonth,
    startMonth: yearMonth,
    endMonth: yearMonth.nullable(),
    sortOrder,
  })
  .superRefine(endNotBeforeStart)

export const incomeSchema = z
  .object({
    id,
    name,
    amountCents: positiveCents,
    frequency: z.enum(['monthly', 'annual', 'irregular']),
    months: z.array(calendarMonth),
    growthBps: rateBps(-5_000, 10_000),
    growthMonth: calendarMonth,
    startMonth: yearMonth,
    endMonth: yearMonth.nullable(),
    confidence: z.enum(['committed', 'variable']),
    sortOrder,
  })
  .superRefine((v, ctx) => {
    endNotBeforeStart(v, ctx)
    if (v.frequency === 'annual' && v.months.length !== 1) {
      ctx.addIssue({ code: 'custom', path: ['months'], message: 'Choose the one month it is paid' })
    }
    if (v.frequency === 'irregular' && v.months.length === 0) {
      ctx.addIssue({ code: 'custom', path: ['months'], message: 'Choose at least one month' })
    }
    if (new Set(v.months).size !== v.months.length) {
      ctx.addIssue({ code: 'custom', path: ['months'], message: 'Months must not repeat' })
    }
  })

export const eventSchema = z.object({
  id,
  name,
  month: yearMonth,
  amountCents: positiveCents,
  direction: z.enum(['inflow', 'outflow']),
  sortOrder,
})

export type Sortable = { sortOrder: number }
export type AssetRecord = Asset & Sortable
export type DebtRecord = Debt & Sortable
export type ObligationRecord = Obligation & Sortable
export type IncomeRecord = Income & Sortable
export type EventRecord = OneOffEvent & Sortable

export interface EntityRecords {
  assets: AssetRecord
  debts: DebtRecord
  obligations: ObligationRecord
  incomes: IncomeRecord
  events: EventRecord
}
export type EntityKind = keyof EntityRecords
export const ENTITY_KINDS: readonly EntityKind[] = ['assets', 'debts', 'obligations', 'incomes', 'events']

export const entitySchemas = {
  assets: assetSchema,
  debts: debtSchema,
  obligations: obligationSchema,
  incomes: incomeSchema,
  events: eventSchema,
} satisfies Record<EntityKind, z.ZodType>

// Compile-time check that each schema's output is assignable to its engine record type.
type Assert<T extends true> = T
export type SchemasMatchEngine = Assert<
  z.output<typeof assetSchema> extends AssetRecord
    ? z.output<typeof debtSchema> extends DebtRecord
      ? z.output<typeof obligationSchema> extends ObligationRecord
        ? z.output<typeof incomeSchema> extends IncomeRecord
          ? z.output<typeof eventSchema> extends EventRecord
            ? true
            : false
          : false
        : false
      : false
    : false
>
