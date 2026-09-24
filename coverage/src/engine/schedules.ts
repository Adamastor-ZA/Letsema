import { roundCents } from './money'
import { annualStepsSince, calendarMonth, toIndex, type MonthIndex } from './month'
import { bpsToRate } from './rates'
import type { Income, Obligation, YearMonth } from './types'

function isActive(m: MonthIndex, startMonth: YearMonth, endMonth: YearMonth | null): boolean {
  if (m < toIndex(startMonth)) return false
  return endMonth === null || m <= toIndex(endMonth)
}

/** `amount` stepped up by `rateBps` once a year in `stepMonth`, counting from the as-of month. */
export function escalated(amountCents: number, rateBps: number, asOf: MonthIndex, m: MonthIndex, stepMonth: number): number {
  const steps = annualStepsSince(asOf, m, stepMonth)
  if (steps === 0 || rateBps === 0) return amountCents
  return roundCents(amountCents * Math.pow(1 + bpsToRate(rateBps), steps))
}

/** Amount of an obligation due in month `m` (0 when not due). */
export function obligationDue(o: Obligation, asOf: MonthIndex, m: MonthIndex): number {
  if (!isActive(m, o.startMonth, o.endMonth)) return 0
  if (o.frequency === 'annual' && calendarMonth(m) !== o.paymentMonth) return 0
  return escalated(o.amountCents, o.escalationBps, asOf, m, o.escalationMonth)
}

/** Amount of an income stream received in month `m` (0 when none is due). */
export function incomeDue(i: Income, asOf: MonthIndex, m: MonthIndex): number {
  if (!isActive(m, i.startMonth, i.endMonth)) return 0
  if (i.frequency !== 'monthly' && !i.months.includes(calendarMonth(m))) return 0
  return escalated(i.amountCents, i.growthBps, asOf, m, i.growthMonth)
}
