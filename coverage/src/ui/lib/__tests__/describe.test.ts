import { describe, expect, it } from 'vitest'
import { resolveOverrides } from '../../../engine/scenarios'
import { buildSampleInputs } from '../../../sample/sample-data'
import { changeBpsToFactor, describeOverrides, factorToChangeBps } from '../describe'
import { makeFormatter } from '../format'

const fmt = makeFormatter('ZAR', 'en-ZA')
const data = buildSampleInputs('2026-09')

describe('describeOverrides', () => {
  it('describes the combined presets', () => {
    expect(describeOverrides(resolveOverrides({ presets: ['rateShock', 'variableIncomeDown', 'costEscalation'], custom: {} }), data, fmt)).toEqual([
      'Prime +2 points, variable-rate instalments recalculated',
      'Variable income −40%',
      'Obligations escalate +3 points a year',
    ])
  })

  it('names excluded items and extra events, ignoring stale ids', () => {
    const lines = describeOverrides(
      {
        committedIncomeFactor: 0,
        excludedIds: ['sample-rental', 'deleted-id'],
        extraEvents: [{ id: 'x', name: 'Retrenchment package', month: '2027-03', amountCents: 5_000_000, direction: 'inflow' }],
      },
      data,
      fmt,
    )
    expect(lines[0]).toBe('No committed income')
    expect(lines[1]).toBe('Leaves out Flatlet rental (sample)')
    expect(lines[2]).toMatch(/^Adds Retrenchment package: R\s?50[\s,]000 in Mar 2027$/)
  })

  it('says nothing for empty overrides', () => {
    expect(describeOverrides({}, data, fmt)).toEqual([])
  })
})

describe('income change conversions', () => {
  it('round-trips percentage changes and factors', () => {
    expect(changeBpsToFactor(-4000)).toBe(0.6)
    expect(factorToChangeBps(0.6)).toBe(-4000)
    expect(changeBpsToFactor(-10_000)).toBe(0)
    expect(changeBpsToFactor(-12_000)).toBe(0)
    expect(factorToChangeBps(changeBpsToFactor(1250))).toBe(1250)
  })
})
