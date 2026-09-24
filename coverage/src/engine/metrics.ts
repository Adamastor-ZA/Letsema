import type { MonthRow, ProjectionResult, YearMonth } from './types'

export interface CoverageRatio {
  /** null when nothing falls due in the window. */
  ratio: number | null
  months: number
  numeratorCents: number
  denominatorCents: number
  /** Opening T1 plus T2 after haircut. */
  liquidCents: number
  committedIncomeCents: number
  obligationsCents: number
  debtPaymentsCents: number
  oneOffOutCents: number
}

/**
 * (T1 + T2 after haircut + committed income over the window) /
 * (obligations + debt payments + one-off outflows over the window).
 * One-off inflows are excluded: they are not committed income.
 */
export function coverageRatio(result: ProjectionResult, months = 12): CoverageRatio {
  const window = result.rows.slice(0, months)
  const liquidCents = result.opening.tiers.T1 + result.opening.t2NetCents
  let committedIncomeCents = 0
  let obligationsCents = 0
  let debtPaymentsCents = 0
  let oneOffOutCents = 0
  for (const r of window) {
    committedIncomeCents += r.committedIncomeCents
    obligationsCents += r.obligationsCents
    debtPaymentsCents += r.debtPaymentsCents
    oneOffOutCents += r.oneOffOutCents
  }
  const numeratorCents = liquidCents + committedIncomeCents
  const denominatorCents = obligationsCents + debtPaymentsCents + oneOffOutCents
  return {
    ratio: denominatorCents > 0 ? numeratorCents / denominatorCents : null,
    months: window.length,
    numeratorCents,
    denominatorCents,
    liquidCents,
    committedIncomeCents,
    obligationsCents,
    debtPaymentsCents,
    oneOffOutCents,
  }
}

export interface Runway {
  /** Full months covered before the first shortfall; null when none falls within the horizon. */
  months: number | null
  /** The first shortfall month, or null. */
  month: YearMonth | null
}

export function firstShortfall(rows: MonthRow[]): Runway {
  const index = rows.findIndex((r) => r.shortfall)
  if (index === -1) return { months: null, month: null }
  return { months: index, month: rows[index]!.month }
}
