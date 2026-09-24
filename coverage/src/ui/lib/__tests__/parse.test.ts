import { describe, expect, it } from 'vitest'
import { formatMoneyInput, formatPercentInput, parseInteger, parseMoney, parsePercent } from '../parse'

const cents = (text: string, allowNegative = false) => {
  const r = parseMoney(text, { allowNegative })
  return r.ok ? r.value : r.error
}
const bps = (text: string, allowNegative = false) => {
  const r = parsePercent(text, { allowNegative })
  return r.ok ? r.value : r.error
}

describe('parseMoney', () => {
  it('reads the common grouping and decimal conventions', () => {
    expect(cents('12000')).toBe(1_200_000)
    expect(cents('12 000')).toBe(1_200_000)
    expect(cents('12 000,50')).toBe(1_200_050)
    expect(cents('12,000.50')).toBe(1_200_050)
    expect(cents('12.000,50')).toBe(1_200_050)
    expect(cents('R 12 000')).toBe(1_200_000)
    expect(cents('R12,5')).toBe(1_250)
    expect(cents('1,234,567')).toBe(123_456_700)
    expect(cents('1.234')).toBe(123_400)
    expect(cents('0.5')).toBe(50)
    expect(cents('.75')).toBe(75)
    expect(cents('12.')).toBe(1_200)
  })

  it('rejects bad input with a reason', () => {
    expect(cents('')).toBe('Enter an amount')
    expect(cents('abc')).toBe('Enter a number, e.g. 12 500.00')
    expect(cents('1.234.5')).toBe('Enter a number, e.g. 12 500.00')
    expect(cents('10.005')).toBe(1_000_500) // three digits after a lone dot read as grouping
    expect(cents('10.0055')).toBe('Use at most two decimal places')
    expect(cents('-5')).toBe('Cannot be negative')
    expect(cents('-5', true)).toBe(-500)
    expect(cents('999999999999999')).toBe('Amount is too large')
  })

  it('round-trips with formatMoneyInput', () => {
    for (const c of [0, 5, 1_200_000, 1_200_050, 123_456_789, -250_000]) {
      expect(cents(formatMoneyInput(c), true)).toBe(c)
    }
    expect(formatMoneyInput(1_200_050)).toBe('12 000.50')
    expect(formatMoneyInput(1_200_000)).toBe('12 000')
  })
})

describe('parsePercent', () => {
  it('reads percentages to basis points', () => {
    expect(bps('11.75')).toBe(1175)
    expect(bps('11,75')).toBe(1175)
    expect(bps('7.5%')).toBe(750)
    expect(bps('0')).toBe(0)
    expect(bps('-0.5', true)).toBe(-50)
    expect(bps('-0.5')).toBe('Cannot be negative')
    expect(bps('1.234')).toBe('Use at most two decimal places')
    expect(bps('ten')).toBe('Enter a percentage, e.g. 7.5')
  })

  it('round-trips with formatPercentInput', () => {
    for (const b of [0, 5, 50, 750, 1175, -50, -1200, 10_000]) expect(bps(formatPercentInput(b), true)).toBe(b)
    expect(formatPercentInput(750)).toBe('7.5')
    expect(formatPercentInput(-50)).toBe('-0.5')
  })
})

describe('parseInteger', () => {
  it('accepts whole numbers only', () => {
    expect(parseInteger('10')).toEqual({ ok: true, value: 10 })
    expect(parseInteger('1.5').ok).toBe(false)
  })
})
