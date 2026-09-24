import { describe, expect, it } from 'vitest'
import { adjustedInstalment, remainingTerm, stepDebt } from '../debt'
import { toIndex } from '../month'
import { project } from '../project'
import { monthlyNominal, pmt } from '../rates'
import { fixedDebt, inputs, variableDebt } from './helpers'

function schedule(balance: number, rateBps: number, instalment: number, months: number) {
  const rows = []
  for (let k = 1; k <= months; k++) {
    const step = stepDebt(balance, rateBps, instalment, k === months)
    balance = step.balanceCents
    rows.push(step)
  }
  return rows
}

describe('debt amortisation', () => {
  it('reproduces a textbook schedule row by row', () => {
    // $10 000 at 12% nominal over 12 months, instalment $888.49.
    const rows = schedule(1_000_000, 1200, 88_849, 12)
    expect(rows[0]).toEqual({ interestCents: 10_000, paymentCents: 88_849, balanceCents: 921_151, retired: false })
    expect(rows[1]).toEqual({ interestCents: 9_212, paymentCents: 88_849, balanceCents: 841_514, retired: false })
    expect(rows[2]).toEqual({ interestCents: 8_415, paymentCents: 88_849, balanceCents: 761_080, retired: false })
    const last = rows[11]!
    expect(last.balanceCents).toBe(0)
    expect(last.retired).toBe(true)
    expect(Math.abs(last.paymentCents - 88_849)).toBeLessThanOrEqual(5)
    const totalInterest = rows.reduce((s, r) => s + r.interestCents, 0)
    expect(totalInterest).toBe(rows.reduce((s, r) => s + r.paymentCents, 0) - 1_000_000)
  })

  it('tracks the closed-form remaining balance of a 20-year bond', () => {
    const P = 100_000_000
    const i = monthlyNominal(1100)
    const A = pmt(P, i, 240)
    const rows = schedule(P, 1100, A, 240)
    for (const k of [1, 12, 60, 120, 180, 239]) {
      const f = Math.pow(1 + i, k)
      const closedForm = P * f - (A * (f - 1)) / i
      expect(Math.abs(rows[k - 1]!.balanceCents - closedForm)).toBeLessThanOrEqual(50)
    }
    // Rounding the instalment down leaves a residual that the final payment settles.
    const f239 = Math.pow(1 + i, 239)
    const finalOwed = (P * f239 - (A * (f239 - 1)) / i) * (1 + i)
    expect(rows[239]!.balanceCents).toBe(0)
    expect(Math.abs(rows[239]!.paymentCents - finalOwed)).toBeLessThanOrEqual(50)
    expect(rows[239]!.paymentCents - A).toBeLessThan(500)
    expect(rows.slice(0, 239).every((r) => !r.retired)).toBe(true)
  })

  it('settles the outstanding balance as a balloon in the end month', () => {
    const rows = schedule(1_000_000, 0, 100_000, 3)
    expect(rows.map((r) => r.paymentCents)).toEqual([100_000, 100_000, 800_000])
  })

  it('caps the final instalment at what is owed and retires the debt early', () => {
    const rows = schedule(250_000, 0, 100_000, 12)
    expect(rows.map((r) => r.paymentCents).slice(0, 4)).toEqual([100_000, 100_000, 50_000, 0])
    expect(rows[2]!.retired).toBe(true)
    expect(rows[3]!.retired).toBe(false)
  })

  it('lets an instalment below the interest grow the balance', () => {
    const step = stepDebt(1_000_000, 1200, 5_000, false)
    expect(step.balanceCents).toBe(1_005_000)
  })

  it('retires a debt mid-horizon and stops its payments', () => {
    const result = project(inputs({ debts: [fixedDebt('car', 300_000, 0, 100_000, '2030-01')], horizonMonths: 6 }))
    expect(result.rows.map((r) => r.debtPaymentsCents)).toEqual([100_000, 100_000, 100_000, 0, 0, 0])
    expect(result.rows[2]!.debtsRetired).toEqual(['car'])
    expect(result.rows.flatMap((r) => r.debtsRetired)).toEqual(['car'])
    expect(result.rows[5]!.debtCents).toBe(0)
  })

  it('charges variable-rate debt at prime plus margin', () => {
    const result = project(inputs({ primeBps: 1050, debts: [variableDebt('bond', 12_000_000, -50, 0, '2040-01')], horizonMonths: 1 }))
    expect(result.rows[0]!.debtInterestCents).toBe(100_000) // 10% / 12 on R120 000
  })
})

describe('instalment recalculation on a prime shock', () => {
  const asOf = toIndex('2026-01')
  const bond = variableDebt('bond', 200_000_000, 0, 2_000_000, '2045-12')

  it('adds the difference in level instalment over the remaining term', () => {
    const n = remainingTerm(bond, asOf)
    expect(n).toBe(240)
    const delta = pmt(200_000_000, monthlyNominal(1200), n) - pmt(200_000_000, monthlyNominal(1000), n)
    expect(adjustedInstalment(bond, 1000, 200, asOf)).toBe(2_000_000 + delta)
    expect(delta).toBeGreaterThan(0)
  })

  it('leaves fixed-rate debt and zero shocks alone', () => {
    expect(adjustedInstalment(fixedDebt('car', 1_000_000, 1100, 50_000, '2029-01'), 1000, 200, asOf)).toBe(50_000)
    expect(adjustedInstalment(bond, 1000, 0, asOf)).toBe(2_000_000)
  })
})
