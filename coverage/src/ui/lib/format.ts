import { formatMoney } from '../../engine/money'
import type { Runway } from '../../engine/metrics'
import { formatPercentInput } from './parse'
import { MONTH_SHORT } from '../editors/fields'

export interface Formatter {
  money: (cents: number) => string
  /** Short form for axes and tight spaces: R 1.2m, R 850k. */
  moneyCompact: (cents: number) => string
  percent: (bps: number) => string
  month: (ym: string | null) => string
  ratio: (ratio: number | null) => string
  runway: (r: Runway) => string
}

function currencySymbol(currency: string, locale: string): string {
  try {
    return new Intl.NumberFormat(locale, { style: 'currency', currency }).formatToParts(0).find((p) => p.type === 'currency')?.value ?? currency
  } catch {
    return currency
  }
}

export function makeFormatter(currency: string, locale: string): Formatter {
  const symbol = currencySymbol(currency, locale)
  const month = (ym: string | null) => {
    if (!ym) return '–'
    const [y, m] = ym.split('-')
    return `${MONTH_SHORT[Number(m) - 1] ?? m} ${y}`
  }
  return {
    money: (cents) => formatMoney(cents, currency, locale),
    moneyCompact: (cents) => {
      const v = Math.abs(cents) / 100
      const sign = cents < 0 ? '-' : ''
      const [n, unit] = v >= 1e9 ? [v / 1e9, 'bn'] : v >= 1e6 ? [v / 1e6, 'm'] : v >= 1e3 ? [v / 1e3, 'k'] : [v, '']
      const digits = unit === '' || n >= 100 ? 0 : n >= 10 ? 0 : 1
      return `${sign}${symbol} ${n.toFixed(digits).replace(/\.0$/, '')}${unit}`
    },
    percent: (bps) => `${formatPercentInput(bps)}%`,
    month,
    ratio: (r) => (r === null ? 'n/a' : `${r.toFixed(2)}×`),
    runway: (r) => (r.months === null ? 'Beyond horizon' : `${r.months} ${r.months === 1 ? 'month' : 'months'}`),
  }
}
