import { roundCents } from './money'
import { toIndex, type MonthIndex } from './month'
import { monthlyNominal, pmt } from './rates'
import type { Debt } from './types'

export function debtRateBps(debt: Debt, primeBps: number): number {
  return debt.rateType === 'fixed' ? debt.fixedRateBps : primeBps + debt.primeMarginBps
}

/** Months of repayments from `from` to the debt's end month, inclusive (at least 1). */
export function remainingTerm(debt: Debt, from: MonthIndex): number {
  return Math.max(1, toIndex(debt.endMonth) - from + 1)
}

export interface DebtStep {
  interestCents: number
  paymentCents: number
  balanceCents: number
  retired: boolean
}

/**
 * One month of amortisation: accrue interest at the nominal monthly rate, then
 * pay the instalment (capped at what is owed). In or after the end month the
 * whole outstanding balance is paid, as a balloon if the instalment fell short.
 */
export function stepDebt(balanceCents: number, rateBps: number, instalmentCents: number, isFinalMonth: boolean): DebtStep {
  if (balanceCents <= 0) return { interestCents: 0, paymentCents: 0, balanceCents: 0, retired: false }
  const interestCents = roundCents(balanceCents * monthlyNominal(rateBps))
  const owed = balanceCents + interestCents
  const paymentCents = isFinalMonth ? owed : Math.min(Math.max(instalmentCents, 0), owed)
  const newBalance = owed - paymentCents
  return { interestCents, paymentCents, balanceCents: newBalance, retired: newBalance <= 0 }
}

/**
 * Instalment for a variable-rate debt after prime moves by `primeDeltaBps`,
 * the way a bank recalculates: the user's instalment plus the difference in
 * level instalment at the new and old rates over the remaining term. Any extra
 * the user already pays is preserved.
 */
export function adjustedInstalment(debt: Debt, primeBps: number, primeDeltaBps: number, asOf: MonthIndex): number {
  if (debt.rateType !== 'variable' || primeDeltaBps === 0) return debt.instalmentCents
  const n = remainingTerm(debt, asOf)
  const base = pmt(debt.balanceCents, monthlyNominal(primeBps + debt.primeMarginBps), n)
  const shocked = pmt(debt.balanceCents, monthlyNominal(primeBps + primeDeltaBps + debt.primeMarginBps), n)
  return Math.max(0, debt.instalmentCents + shocked - base)
}
