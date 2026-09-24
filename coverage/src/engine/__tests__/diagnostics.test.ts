import { describe, expect, it } from 'vitest'
import { debtOutlook } from '../diagnostics'
import { monthlyNominal, pmt } from '../rates'
import { fixedDebt, variableDebt } from './helpers'

describe('debt outlook', () => {
  it('reports a clean payoff for a level instalment', () => {
    const a = pmt(1_000_000, monthlyNominal(1200), 12)
    const o = debtOutlook(fixedDebt('loan', 1_000_000, 1200, a, '2026-12'), 1000, '2026-01')
    expect(o).toMatchObject({ rateBps: 1200, firstInterestCents: 10_000, negativeAmortisation: false, earlyPayoffMonth: null, overdue: false })
    expect(o.balloonCents).toBeLessThanOrEqual(5)
  })

  it('reports a balloon when the instalment falls short', () => {
    const o = debtOutlook(fixedDebt('car', 1_000_000, 0, 100_000, '2026-03'), 1000, '2026-01')
    expect(o.balloonCents).toBe(700_000)
  })

  it('reports an early payoff', () => {
    const o = debtOutlook(fixedDebt('card', 250_000, 0, 100_000, '2027-12'), 1000, '2026-01')
    expect(o).toMatchObject({ earlyPayoffMonth: '2026-03', balloonCents: 0 })
  })

  it('flags an instalment below the interest', () => {
    const o = debtOutlook(variableDebt('bond', 100_000_000, 0, 500_000, '2046-01'), 1200, '2026-01')
    expect(o.negativeAmortisation).toBe(true)
    expect(o.balloonCents).toBeGreaterThan(100_000_000)
  })

  it('flags an end month that has already passed', () => {
    const o = debtOutlook(fixedDebt('old', 50_000, 0, 10_000, '2025-06'), 1000, '2026-01')
    expect(o).toMatchObject({ overdue: true, balloonCents: 40_000 })
  })

  it('handles a zero balance', () => {
    expect(debtOutlook(fixedDebt('done', 0, 1000, 1_000, '2030-01'), 1000, '2026-01')).toMatchObject({ balloonCents: 0, earlyPayoffMonth: null })
  })
})
