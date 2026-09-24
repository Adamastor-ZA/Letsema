import { describe, expect, it } from 'vitest'
import { evaluate } from '../evaluate'
import { coverageRatio, firstShortfall } from '../metrics'
import { project } from '../project'
import { asset, event, fixedDebt, income, inputs, obligation } from './helpers'

describe('12-month coverage ratio', () => {
  it('matches a hand calculation', () => {
    const result = project(
      inputs({
        horizonMonths: 24,
        assets: [asset('cash', 'T1', 100_000), asset('ut', 'T2', 100_000, { haircutBps: 1_000 }), asset('ra', 'T3', 900_000, { accessibleCents: 900_000 })],
        incomes: [income('salary', 10_000), income('freelance', 5_000, { confidence: 'variable' })],
        obligations: [obligation('living', 8_000)],
        debts: [fixedDebt('loan', 1_000_000, 0, 2_000, '2040-01')],
        events: [event('holiday', '2026-06', 12_000, 'outflow'), event('gift', '2026-07', 50_000, 'inflow'), event('later', '2027-06', 99_000, 'outflow')],
      }),
    )
    const c = coverageRatio(result)
    // (100 000 + 90 000 + 12 × 10 000) / (12 × 8 000 + 12 × 2 000 + 12 000)
    expect(c).toMatchObject({
      liquidCents: 190_000,
      committedIncomeCents: 120_000,
      obligationsCents: 96_000,
      debtPaymentsCents: 24_000,
      oneOffOutCents: 12_000,
      numeratorCents: 310_000,
      denominatorCents: 132_000,
    })
    expect(c.ratio).toBeCloseTo(310_000 / 132_000, 10)
  })

  it('reflects escalation and a debt retiring inside the window', () => {
    const result = project(
      inputs({
        horizonMonths: 12,
        obligations: [obligation('o', 1_000, { escalationBps: 1_000, escalationMonth: 7 })],
        debts: [fixedDebt('card', 3_000, 0, 1_000, '2030-01')],
      }),
    )
    const c = coverageRatio(result)
    expect(c.obligationsCents).toBe(6 * 1_000 + 6 * 1_100)
    expect(c.debtPaymentsCents).toBe(3_000)
  })

  it('is null when nothing falls due', () => {
    expect(coverageRatio(project(inputs({ assets: [asset('cash', 'T1', 100)] }))).ratio).toBeNull()
  })
})

describe('runway', () => {
  const household = inputs({
    horizonMonths: 24,
    assets: [asset('cash', 'T1', 30_000)],
    incomes: [income('salary', 5_000), income('freelance', 5_000, { confidence: 'variable' })],
    obligations: [obligation('living', 10_000)],
  })

  it('finds no shortfall in a balanced base case', () => {
    expect(evaluate(household).metrics.firstShortfall).toEqual({ months: null, month: null })
  })

  it('counts months until the first shortfall when variable income stops', () => {
    // −5 000 a month against 30 000: six months covered, short in the seventh.
    expect(evaluate(household).metrics.runwayVariableStops).toEqual({ months: 6, month: '2026-07' })
  })

  it('counts months until the first shortfall when all income stops', () => {
    expect(evaluate(household).metrics.runwayAllIncomeStops).toEqual({ months: 3, month: '2026-04' })
  })

  it('still applies one-off inflows when income stops', () => {
    const withInheritance = { ...household, events: [event('inheritance', '2026-03', 20_000, 'inflow')] }
    expect(evaluate(withInheritance).metrics.runwayAllIncomeStops.months).toBe(5)
  })

  it('reports zero months when the first month is already short', () => {
    const rows = project(inputs({ obligations: [obligation('o', 1)] })).rows
    expect(firstShortfall(rows)).toEqual({ months: 0, month: '2026-01' })
  })

  it('reports the base-case first shortfall month', () => {
    const tight = { ...household, events: [event('roof', '2026-09', 40_000, 'outflow')] }
    expect(evaluate(tight).metrics.firstShortfall).toEqual({ months: 8, month: '2026-09' })
  })
})

describe('net worth metrics', () => {
  it('reports today and at the horizon', () => {
    const e = evaluate(
      inputs({
        horizonMonths: 12,
        assets: [asset('cash', 'T1', 100_000), asset('house', 'T4', 1_000_000)],
        debts: [fixedDebt('bond', 600_000, 0, 10_000, '2040-01')],
        incomes: [income('pay', 10_000)],
      }),
    )
    expect(e.metrics).toMatchObject({
      netWorthTodayCents: 500_000,
      liquidNetWorthTodayCents: -500_000,
      // Income exactly services the bond: cash is flat, debt falls by 120 000.
      netWorthHorizonCents: 620_000,
      liquidNetWorthHorizonCents: -380_000,
      horizonMonth: '2026-12',
    })
  })
})

describe('lowest liquid balance', () => {
  it('finds the trough and its month, including a carried deficit', async () => {
    const { lowestLiquid } = await import('../metrics')
    const rows = project(
      inputs({
        horizonMonths: 6,
        assets: [asset('cash', 'T1', 1_000)],
        incomes: [income('pay', 500)],
        events: [event('bill', '2026-03', 3_000, 'outflow')],
      }),
    ).rows
    // Jan 1 500, Feb 2 000, Mar −500 (deficit), Apr 0, May 500, Jun 1 000.
    expect(lowestLiquid(rows)).toEqual({ cents: -500, month: '2026-03' })
    expect(evaluate(inputs({ horizonMonths: 6, assets: [asset('cash', 'T1', 1_000)], incomes: [income('pay', 500)] })).metrics).toMatchObject({
      liquidBalanceHorizonCents: 4_000,
      lowestLiquid: { cents: 1_500, month: '2026-01' },
    })
  })
})
