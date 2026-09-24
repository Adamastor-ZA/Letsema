export type Parsed<T> = { ok: true; value: T } | { ok: false; error: string }

const MAX_CENTS = 10_000_000_000_000

/**
 * Normalise a number typed with any common grouping and decimal convention
 * ("12 000,50", "12,000.50", "12.000,50", "R 12 000") to "12000.50".
 * A lone separator followed by exactly three digits is read as grouping.
 */
function normaliseNumber(text: string): string | null {
  let s = text.replace(/[\s\u00a0\u202f']/g, '').replace(/%$/, '')
  s = s.replace(/^([+-]?)[^\d.,+-]+/, '$1') // leading currency symbol or code
  const negative = s.startsWith('-')
  s = s.replace(/^[+-]/, '')
  if (!/^[\d.,]+$/.test(s)) return null
  const lastDot = s.lastIndexOf('.')
  const lastComma = s.lastIndexOf(',')
  let decimal: '.' | ',' | null = null
  if (lastDot !== -1 && lastComma !== -1) {
    decimal = lastDot > lastComma ? '.' : ','
  } else {
    const sep = lastDot !== -1 ? '.' : lastComma !== -1 ? ',' : null
    if (sep) {
      const count = s.split(sep).length - 1
      const after = s.length - s.lastIndexOf(sep) - 1
      decimal = count === 1 && after !== 3 ? sep : null
    }
  }
  const cut = decimal === null ? s.length : s.lastIndexOf(decimal)
  const whole = s.slice(0, cut)
  const frac = decimal === null ? '' : s.slice(cut + 1)
  // Grouping must be in threes: "1 234 567" or "1.234.567", never "1.23.4".
  if (/[.,]/.test(whole) && !/^\d{1,3}([.,]\d{3})+$/.test(whole)) return null
  if (!/^\d*$/.test(frac) || (whole === '' && frac === '')) return null
  return `${negative ? '-' : ''}${whole.replace(/[.,]/g, '') || '0'}${decimal === null ? '' : `.${frac}`}`
}

/** Parse a typed amount to integer cents. */
export function parseMoney(text: string, { allowNegative = false } = {}): Parsed<number> {
  if (text.trim() === '') return { ok: false, error: 'Enter an amount' }
  const n = normaliseNumber(text)
  if (n === null) return { ok: false, error: 'Enter a number, e.g. 12 500.00' }
  const negative = n.startsWith('-')
  const [whole = '0', frac = ''] = n.replace('-', '').split('.')
  if (frac.length > 2) return { ok: false, error: 'Use at most two decimal places' }
  const cents = Number(whole || '0') * 100 + Number(frac.padEnd(2, '0') || '0')
  if (cents > MAX_CENTS) return { ok: false, error: 'Amount is too large' }
  if (negative && !allowNegative) return { ok: false, error: 'Cannot be negative' }
  return { ok: true, value: negative && cents !== 0 ? -cents : cents }
}

/** Parse a typed percentage to integer basis points ("11.75" → 1175). */
export function parsePercent(text: string, { allowNegative = false } = {}): Parsed<number> {
  if (text.trim() === '') return { ok: false, error: 'Enter a rate' }
  const s = text.replace(/[\s%]/g, '').replace(',', '.')
  if (!/^[+-]?(\d+(\.\d*)?|\.\d+)$/.test(s)) return { ok: false, error: 'Enter a percentage, e.g. 7.5' }
  const negative = s.startsWith('-')
  const [whole = '0', frac = ''] = s.replace(/^[+-]/, '').split('.')
  if (frac.length > 2) return { ok: false, error: 'Use at most two decimal places' }
  const bps = Number(whole || '0') * 100 + Number(frac.padEnd(2, '0') || '0')
  if (negative && !allowNegative) return { ok: false, error: 'Cannot be negative' }
  return { ok: true, value: negative && bps !== 0 ? -bps : bps }
}

export function parseInteger(text: string): Parsed<number> {
  const s = text.trim()
  if (!/^[+-]?\d+$/.test(s)) return { ok: false, error: 'Enter a whole number' }
  return { ok: true, value: Number(s) }
}

/** Cents as an editable string: "12 000" or "12 000.50". */
export function formatMoneyInput(cents: number): string {
  const negative = cents < 0
  const abs = Math.abs(cents)
  const whole = Math.floor(abs / 100)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
  const frac = abs % 100
  return `${negative ? '-' : ''}${whole}${frac ? `.${String(frac).padStart(2, '0')}` : ''}`
}

/** Basis points as an editable percentage string: 1175 → "11.75". */
export function formatPercentInput(bps: number): string {
  const negative = bps < 0
  const abs = Math.abs(bps)
  const whole = Math.floor(abs / 100)
  const frac = abs % 100
  const fracText = frac === 0 ? '' : `.${String(frac).padStart(2, '0').replace(/0$/, '')}`
  return `${negative ? '-' : ''}${whole}${fracText}`
}
