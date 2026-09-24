import type { CalendarMonth, YearMonth } from './types'

/** Months since year 0; lets month arithmetic be plain integer arithmetic. */
export type MonthIndex = number

const PATTERN = /^(\d{4})-(0[1-9]|1[0-2])$/

export function isYearMonth(value: unknown): value is YearMonth {
  return typeof value === 'string' && PATTERN.test(value)
}

export function toIndex(ym: YearMonth): MonthIndex {
  const match = PATTERN.exec(ym)
  if (!match) throw new Error(`Invalid month "${ym}", expected YYYY-MM`)
  return Number(match[1]) * 12 + Number(match[2]) - 1
}

export function fromIndex(index: MonthIndex): YearMonth {
  const year = Math.floor(index / 12)
  const month = index - year * 12 + 1
  return `${String(year).padStart(4, '0')}-${String(month).padStart(2, '0')}`
}

export function calendarMonth(index: MonthIndex): CalendarMonth {
  return (((index % 12) + 12) % 12) + 1
}

export function addMonths(ym: YearMonth, months: number): YearMonth {
  return fromIndex(toIndex(ym) + months)
}

export function monthsBetween(from: YearMonth, to: YearMonth): number {
  return toIndex(to) - toIndex(from)
}

/**
 * Number of annual step-ups that have taken effect by month `m`, counting
 * occurrences of `stepMonth` strictly after `base` up to and including `m`.
 * The base month's amount already reflects any step-up due that month.
 */
export function annualStepsSince(base: MonthIndex, m: MonthIndex, stepMonth: CalendarMonth): number {
  let delta = (stepMonth - calendarMonth(base) + 12) % 12
  if (delta === 0) delta = 12
  const first = base + delta
  return m < first ? 0 : Math.floor((m - first) / 12) + 1
}
