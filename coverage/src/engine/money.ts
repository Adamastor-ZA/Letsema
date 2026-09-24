/** Round to whole cents, half away from zero. */
export function roundCents(value: number): number {
  const r = Math.sign(value) * Math.round(Math.abs(value))
  return r === 0 ? 0 : r
}

/** Integer ceiling of a / b for non-negative integers, without floating-point error. */
export function ceilDiv(a: number, b: number): number {
  return Math.floor((a + b - 1) / b)
}

/** Portion of `cents` represented by `bps`, rounded to cents. */
export function applyBps(cents: number, bps: number): number {
  return roundCents((cents * bps) / 10_000)
}

export function sum(values: Iterable<number>): number {
  let total = 0
  for (const v of values) total += v
  return total
}

export function formatMoney(cents: number, currency = 'ZAR', locale = 'en-ZA', fractionDigits = 0): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  }).format(cents / 100)
}
