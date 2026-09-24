import { describe, expect, it } from 'vitest'
import { applyBps, ceilDiv, roundCents } from '../money'
import { addMonths, annualStepsSince, calendarMonth, fromIndex, isYearMonth, monthsBetween, toIndex } from '../month'
import { monthlyEffective, monthlyNominal, pmt } from '../rates'

describe('months', () => {
  it('round-trips YYYY-MM through a month index', () => {
    for (const ym of ['2026-01', '2026-12', '1999-07', '2056-02']) expect(fromIndex(toIndex(ym))).toBe(ym)
  })

  it('does month arithmetic across year boundaries', () => {
    expect(addMonths('2026-11', 3)).toBe('2027-02')
    expect(addMonths('2026-01', -1)).toBe('2025-12')
    expect(monthsBetween('2026-09', '2036-09')).toBe(120)
    expect(calendarMonth(toIndex('2027-02'))).toBe(2)
  })

  it('rejects malformed months', () => {
    expect(isYearMonth('2026-13')).toBe(false)
    expect(isYearMonth('2026-1')).toBe(false)
    expect(() => toIndex('26-01')).toThrow()
  })

  it('counts annual step-ups strictly after the base month', () => {
    const base = toIndex('2026-09')
    expect(annualStepsSince(base, toIndex('2026-12'), 1)).toBe(0)
    expect(annualStepsSince(base, toIndex('2027-01'), 1)).toBe(1)
    expect(annualStepsSince(base, toIndex('2027-12'), 1)).toBe(1)
    expect(annualStepsSince(base, toIndex('2028-01'), 1)).toBe(2)
    // A step-up in the base month is already reflected in the entered amount.
    expect(annualStepsSince(base, toIndex('2026-09'), 9)).toBe(0)
    expect(annualStepsSince(base, toIndex('2027-08'), 9)).toBe(0)
    expect(annualStepsSince(base, toIndex('2027-09'), 9)).toBe(1)
  })
})

describe('money', () => {
  it('rounds half away from zero', () => {
    expect(roundCents(2.5)).toBe(3)
    expect(roundCents(-2.5)).toBe(-3)
    expect(roundCents(-0.4)).toBe(0)
    expect(Object.is(roundCents(-0.4), -0)).toBe(false)
  })

  it('computes integer ceilings and basis-point shares exactly', () => {
    expect(ceilDiv(80_000 * 10_000, 8_000)).toBe(100_000)
    expect(ceilDiv(80_001 * 10_000, 8_000)).toBe(100_002)
    expect(applyBps(100_000, 1_200)).toBe(12_000)
  })
})

describe('rates', () => {
  it('converts nominal annual loan rates to monthly', () => {
    expect(monthlyNominal(1200)).toBeCloseTo(0.01, 12)
  })

  it('makes 12 months of effective growth compound to the annual rate', () => {
    expect(Math.pow(1 + monthlyEffective(1000), 12)).toBeCloseTo(1.1, 12)
    expect(Math.pow(1 + monthlyEffective(-1200), 12)).toBeCloseTo(0.88, 12)
  })

  it('matches published level instalments', () => {
    // R1 000 000 home loan at 11% over 20 years: R10 321.88 per month (exact: 10 321.8839…).
    expect(pmt(100_000_000, monthlyNominal(1100), 240)).toBe(1_032_188)
    // $10 000 at 12% over 12 months: $888.49.
    expect(pmt(1_000_000, monthlyNominal(1200), 12)).toBe(88_849)
    expect(pmt(120_000, 0, 12)).toBe(10_000)
  })
})
