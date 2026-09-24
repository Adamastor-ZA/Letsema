import { roundCents } from './money'

export function bpsToRate(bps: number): number {
  return bps / 10_000
}

/** Monthly rate for a nominal annual rate compounded monthly (the loan convention). */
export function monthlyNominal(annualBps: number): number {
  return bpsToRate(annualBps) / 12
}

/** Monthly rate equivalent to an effective annual rate (used for asset growth). */
export function monthlyEffective(annualBps: number): number {
  return Math.pow(1 + bpsToRate(annualBps), 1 / 12) - 1
}

/** Level instalment that amortises `principalCents` over `months` at `monthlyRate`, rounded to cents. */
export function pmt(principalCents: number, monthlyRate: number, months: number): number {
  if (months <= 0) return principalCents
  if (monthlyRate === 0) return roundCents(principalCents / months)
  const factor = Math.pow(1 + monthlyRate, months)
  return roundCents((principalCents * monthlyRate * factor) / (factor - 1))
}

