/**
 * Engine data model.
 *
 * Conventions:
 * - Money is integer cents (`...Cents`).
 * - Rates are integer basis points (`...Bps`): 11.75% is 1175.
 * - Months are 'YYYY-MM' strings (`YearMonth`); calendar months are 1–12.
 * - Amounts on obligations and income are as at the as-of month; escalation and
 *   growth apply from there, even for items that start in the future.
 * - Income is entered net of tax.
 */

export type YearMonth = string
export type CalendarMonth = number

export type Tier = 'T1' | 'T2' | 'T3' | 'T4'
export const TIERS: readonly Tier[] = ['T1', 'T2', 'T3', 'T4']

export interface Asset {
  id: string
  name: string
  tier: Tier
  valueCents: number
  /** Expected annual growth, compounded to a monthly-equivalent rate. May be negative. */
  growthBps: number
  /** Tax or penalty on liquidation. Applies to T2 drawdowns and to the accessible T3 amount. */
  haircutBps?: number
  /** T3 only: the portion that can be withdrawn (e.g. a two-pot savings component). */
  accessibleCents?: number
}

export type RateType = 'fixed' | 'variable'

export interface Debt {
  id: string
  name: string
  balanceCents: number
  rateType: RateType
  /** Annual rate for fixed-rate debt. */
  fixedRateBps: number
  /** Margin over prime for variable-rate debt; may be negative (prime − 0.5% is -50). */
  primeMarginBps: number
  instalmentCents: number
  /** Final month. Any balance still outstanding is settled as a balloon payment in this month. */
  endMonth: YearMonth
}

export type ObligationFrequency = 'monthly' | 'annual'

export interface Obligation {
  id: string
  name: string
  /** Amount per payment: per month, or the annual lump sum. */
  amountCents: number
  frequency: ObligationFrequency
  /** Annual obligations: the calendar month the lump sum is paid. */
  paymentMonth: CalendarMonth
  escalationBps: number
  escalationMonth: CalendarMonth
  startMonth: YearMonth
  endMonth: YearMonth | null
}

export type IncomeFrequency = 'monthly' | 'annual' | 'irregular'
export type Confidence = 'committed' | 'variable'

export interface Income {
  id: string
  name: string
  /** Amount per payment. */
  amountCents: number
  frequency: IncomeFrequency
  /** Annual: one calendar month. Irregular: each calendar month a payment falls in. Ignored for monthly. */
  months: CalendarMonth[]
  growthBps: number
  growthMonth: CalendarMonth
  startMonth: YearMonth
  endMonth: YearMonth | null
  confidence: Confidence
}

export type Direction = 'inflow' | 'outflow'

export interface OneOffEvent {
  id: string
  name: string
  month: YearMonth
  amountCents: number
  direction: Direction
}

export interface ProjectionInputs {
  /** First projected month. Entered balances are as at the start of this month. */
  asOfMonth: YearMonth
  horizonMonths: number
  primeBps: number
  cpiBps: number
  assets: Asset[]
  debts: Debt[]
  obligations: Obligation[]
  incomes: Income[]
  events: OneOffEvent[]
  /** T1 or T2 asset that receives surpluses. Falls back to the first T1 asset, then to unallocated cash. */
  sweepAssetId: string | null
  /** Draw the accessible T3 amount after T1 and T2 are exhausted. */
  includeT3InDrawdown: boolean
  /** Annual interest charged on a carried deficit. */
  overdraftBps: number
}

export type TierAmounts = Record<Tier, number>

/** A balance-sheet position at a point in time. */
export interface Position {
  tiers: TierAmounts
  /** T2 value net of haircut. */
  t2NetCents: number
  /** Accessible T3 amount net of haircut. */
  t3AccessibleNetCents: number
  /** T1 + T2 net + accessible T3 net. */
  liquidAssetsCents: number
  debtCents: number
  deficitCents: number
  /** All assets at full value, less debt and deficit. */
  netWorthCents: number
  /** Liquid assets less debt and deficit. */
  liquidNetWorthCents: number
  assetValues: Record<string, number>
  debtBalances: Record<string, number>
}

export interface MonthRow extends Position {
  month: YearMonth
  /** 0 for the as-of month. */
  index: number

  incomeCents: number
  committedIncomeCents: number
  variableIncomeCents: number
  obligationsCents: number
  debtPaymentsCents: number
  debtInterestCents: number
  oneOffInCents: number
  oneOffOutCents: number
  /** income − obligations − debt payments + one-off in − one-off out. */
  netFlowCents: number

  growthCents: number
  deficitInterestCents: number
  /** Cash raised from drawdowns. */
  drawnCents: number
  /** Value lost to haircuts on drawdowns. */
  haircutCents: number
  deficitRepaidCents: number
  sweptCents: number
  /** Unfunded need added to the carried deficit this month. */
  newDeficitCents: number

  debtsRetired: string[]
  /** True when a deficit is carried at month end. */
  shortfall: boolean
}

export interface ProjectionResult {
  opening: Position
  rows: MonthRow[]
}
