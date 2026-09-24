import { roundCents } from './money'
import { bpsToRate } from './rates'

export type DisplayMode = 'nominal' | 'real'

/**
 * Express a nominal amount `monthsElapsed` months after the as-of month in
 * as-of-month money, deflating by CPI. The engine itself is always nominal.
 */
export function toReal(cents: number, cpiBps: number, monthsElapsed: number): number {
  return roundCents(cents / Math.pow(1 + bpsToRate(cpiBps), monthsElapsed / 12))
}

/** Convert for display. Row `index` is an end-of-month value, so it sits `index + 1` months out. */
export function forDisplay(cents: number, mode: DisplayMode, cpiBps: number, monthsElapsed: number): number {
  return mode === 'real' ? toReal(cents, cpiBps, monthsElapsed) : cents
}
