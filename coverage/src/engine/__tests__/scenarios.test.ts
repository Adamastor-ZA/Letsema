import { describe, expect, it } from 'vitest'
import { buildSampleInputs } from '../../sample/sample-data'
import { compareScenarios, evaluate } from '../evaluate'
import { monthlyNominal, pmt } from '../rates'
import { PRESETS, PRESET_IDS, applyOverrides, combineOverrides, resolveOverrides } from '../scenarios'
import { asset, event, fixedDebt, income, inputs, obligation, variableDebt } from './helpers'

describe('combining overrides', () => {
  it('adds deltas, multiplies factors, pools exclusions and appends events', () => {
    const e1 = event('a', '2026-05', 1, 'inflow')
    const e2 = event('b', '2026-06', 2, 'outflow')
    const combined = combineOverrides(
      { primeDeltaBps: 200, variableIncomeFactor: 0.6, excludedIds: ['x'], extraEvents: [e1] },
      { primeDeltaBps: 50, variableIncomeFactor: 0.5, excludedIds: ['x', 'y'], extraEvents: [e2] },
    )
    expect(combined.primeDeltaBps).toBe(250)
    expect(combined.variableIncomeFactor).toBeCloseTo(0.3, 12)
    expect(combined.committedIncomeFactor).toBeUndefined()
    expect(combined.excludedIds).toEqual(['x', 'y'])
    expect(combined.extraEvents).toEqual([e1, e2])
  })

  it('resolves presets plus custom overrides', () => {
    const o = resolveOverrides({ presets: [...PRESET_IDS], custom: { primeDeltaBps: 100 } })
    expect(o).toMatchObject({ primeDeltaBps: 300, variableIncomeFactor: 0.6, obligationEscalationDeltaBps: 300 })
  })

  it('defines the three presets as specified', () => {
    expect(PRESETS.rateShock.overrides).toEqual({ primeDeltaBps: 200 })
    expect(PRESETS.variableIncomeDown.overrides).toEqual({ variableIncomeFactor: 0.6 })
    expect(PRESETS.costEscalation.overrides).toEqual({ obligationEscalationDeltaBps: 300 })
  })
})

describe('applying overrides', () => {
  const base = inputs({
    primeBps: 1000,
    assets: [asset('cash', 'T1', 1_000), asset('ut', 'T2', 1_000, { growthBps: 800, haircutBps: 9_900 }), asset('house', 'T4', 1_000, { growthBps: 500 })],
    debts: [variableDebt('bond', 200_000_000, 0, 2_000_000, '2045-12'), fixedDebt('car', 1_000_000, 1100, 50_000, '2029-01')],
    obligations: [obligation('medical', 1_000, { escalationBps: 900 })],
    incomes: [income('salary', 10_000), income('bonus', 5_000, { confidence: 'variable' })],
    events: [event('trip', '2026-06', 100, 'outflow')],
    sweepAssetId: 'cash',
  })

  it('shifts prime and recalculates only variable-rate instalments', () => {
    const shocked = applyOverrides(base, { primeDeltaBps: 200 })
    expect(shocked.primeBps).toBe(1200)
    const delta = pmt(200_000_000, monthlyNominal(1200), 240) - pmt(200_000_000, monthlyNominal(1000), 240)
    expect(shocked.debts[0]!.instalmentCents).toBe(2_000_000 + delta)
    expect(shocked.debts[1]!.instalmentCents).toBe(50_000)
    const e = evaluate(base, { primeDeltaBps: 200 })
    expect(e.result.rows[0]!.debtInterestCents).toBe(2_000_000 + 9_167) // 12% on the bond, 11% on the car
  })

  it('scales variable income only', () => {
    const o = applyOverrides(base, PRESETS.variableIncomeDown.overrides)
    expect(o.incomes.map((i) => i.amountCents)).toEqual([10_000, 3_000])
  })

  it('adds escalation to every obligation', () => {
    expect(applyOverrides(base, PRESETS.costEscalation.overrides).obligations[0]!.escalationBps).toBe(1_200)
  })

  it('moves investment growth and haircuts on T2 and T3 only, clamping haircuts', () => {
    const o = applyOverrides(base, { investmentGrowthDeltaBps: -300, haircutDeltaBps: 500 })
    expect(o.assets.map((a) => a.growthBps)).toEqual([0, 500, 500])
    expect(o.assets[1]!.haircutBps).toBe(10_000)
    expect(o.assets[0]!.haircutBps).toBeUndefined()
  })

  it('excludes items by id and clears an excluded sweep target', () => {
    const o = applyOverrides(base, { excludedIds: ['cash', 'car', 'bonus', 'trip', 'medical'] })
    expect(o.assets.map((a) => a.id)).toEqual(['ut', 'house'])
    expect(o.debts.map((d) => d.id)).toEqual(['bond'])
    expect(o.incomes.map((i) => i.id)).toEqual(['salary'])
    expect(o.events).toEqual([])
    expect(o.obligations).toEqual([])
    expect(o.sweepAssetId).toBeNull()
  })

  it('appends extra one-off events', () => {
    const o = applyOverrides(base, { extraEvents: [event('retrench', '2027-01', 50_000, 'outflow')] })
    expect(o.events.map((e) => e.id)).toEqual(['trip', 'retrench'])
  })

  it('never mutates the base inputs', () => {
    const snapshot = structuredClone(base)
    applyOverrides(base, resolveOverrides({ presets: [...PRESET_IDS], custom: { excludedIds: ['cash'], haircutDeltaBps: 100 } }))
    expect(base).toEqual(snapshot)
  })

  it('returns equivalent inputs for empty overrides', () => {
    expect(applyOverrides(base, {})).toEqual(base)
  })
})

describe('scenario evaluation', () => {
  const sample = buildSampleInputs('2026-09')

  it('makes each stress preset no better than base on the sample household', () => {
    const { base, scenarios } = compareScenarios(
      sample,
      PRESET_IDS.map((id) => ({ id, name: id, presets: [id], custom: {} })),
    )
    for (const { evaluation } of scenarios) {
      expect(evaluation.metrics.liquidNetWorthHorizonCents).toBeLessThan(base.metrics.liquidNetWorthHorizonCents)
      expect(evaluation.metrics.coverage.ratio!).toBeLessThanOrEqual(base.metrics.coverage.ratio!)
    }
  })

  it('makes combined presets worse than any single one', () => {
    const all = evaluate(sample, resolveOverrides({ presets: [...PRESET_IDS], custom: {} }))
    for (const id of PRESET_IDS) {
      const single = evaluate(sample, PRESETS[id].overrides)
      expect(all.metrics.liquidNetWorthHorizonCents).toBeLessThan(single.metrics.liquidNetWorthHorizonCents)
    }
  })

  it('runs the runway variants on top of the scenario', () => {
    const household = inputs({
      horizonMonths: 36,
      assets: [asset('cash', 'T1', 30_000)],
      incomes: [income('salary', 5_000), income('freelance', 5_000, { confidence: 'variable' })],
      obligations: [obligation('living', 10_000, { escalationBps: 5_000, escalationMonth: 1 })],
    })
    const base = evaluate(household)
    const stressed = evaluate(household, PRESETS.costEscalation.overrides)
    expect(stressed.metrics.runwayAllIncomeStops.months!).toBeLessThanOrEqual(base.metrics.runwayAllIncomeStops.months!)
    // Variable income down 40% does not change the variable-stops runway: it is zero either way.
    expect(evaluate(household, PRESETS.variableIncomeDown.overrides).metrics.runwayVariableStops).toEqual(base.metrics.runwayVariableStops)
    // But it does bring the base-case shortfall forward: −2 000 a month through 2026 leaves 6 000,
    // which the January escalation to 15 000 a month overwhelms.
    expect(base.metrics.firstShortfall.months).toBe(18)
    expect(evaluate(household, PRESETS.variableIncomeDown.overrides).metrics.firstShortfall.months).toBe(12)
  })
})
