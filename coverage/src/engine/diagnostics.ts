import { debtRateBps, stepDebt } from './debt'
import { fromIndex, toIndex } from './month'
import type { Debt, YearMonth } from './types'

export interface DebtOutlook {
  rateBps: number
  /** Interest in the first month at the current balance. */
  firstInterestCents: number
  /** The instalment does not cover the first month's interest, so the balance grows. */
  negativeAmortisation: boolean
  /** Month the instalments clear the debt before its end month, if they do. */
  earlyPayoffMonth: YearMonth | null
  /** Amount paid in the end month beyond the instalment. */
  balloonCents: number
  /** The end month is before the as-of month; the balance is settled in the first month. */
  overdue: boolean
}

/** Run a single debt to its end month on its own and describe how it finishes. */
export function debtOutlook(debt: Debt, primeBps: number, asOfMonth: YearMonth): DebtOutlook {
  const rateBps = debtRateBps(debt, primeBps)
  const asOf = toIndex(asOfMonth)
  const end = toIndex(debt.endMonth)
  const first = stepDebt(debt.balanceCents, rateBps, debt.instalmentCents, false)
  const outlook: DebtOutlook = {
    rateBps,
    firstInterestCents: first.interestCents,
    negativeAmortisation: debt.balanceCents > 0 && debt.instalmentCents < first.interestCents,
    earlyPayoffMonth: null,
    balloonCents: 0,
    overdue: end < asOf,
  }
  let balance = debt.balanceCents
  for (let m = asOf; balance > 0; m++) {
    const isFinal = m >= end
    const step = stepDebt(balance, rateBps, debt.instalmentCents, isFinal)
    balance = step.balanceCents
    if (isFinal) {
      outlook.balloonCents = Math.max(0, step.paymentCents - debt.instalmentCents)
    } else if (step.retired) {
      outlook.earlyPayoffMonth = fromIndex(m)
    }
  }
  return outlook
}
