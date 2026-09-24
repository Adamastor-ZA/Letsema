import { formatMoney } from '../../engine/money'
import { formatPercentInput } from './parse'
import { MONTH_SHORT } from '../editors/fields'

export interface Formatter {
  money: (cents: number) => string
  percent: (bps: number) => string
  month: (ym: string | null) => string
}

export function makeFormatter(currency: string, locale: string): Formatter {
  return {
    money: (cents) => formatMoney(cents, currency, locale),
    percent: (bps) => `${formatPercentInput(bps)}%`,
    month: (ym) => {
      if (!ym) return '—'
      const [y, m] = ym.split('-')
      return `${MONTH_SHORT[Number(m) - 1] ?? m} ${y}`
    },
  }
}
