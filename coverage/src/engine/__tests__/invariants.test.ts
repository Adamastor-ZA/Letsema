import { describe, expect, it } from 'vitest'
import { buildSampleInputs } from '../../sample/sample-data'
import { addMonths } from '../month'
import { project } from '../project'
import { PRESET_IDS, applyOverrides, resolveOverrides } from '../scenarios'
import type { ProjectionInputs, Tier } from '../types'
import { asset, checkInvariants, event, fixedDebt, income, inputs, obligation, variableDebt } from './helpers'

/** Small deterministic PRNG so generated households are reproducible. */
function mulberry32(seed: number) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function randomHousehold(seed: number): ProjectionInputs {
  const rnd = mulberry32(seed)
  const int = (lo: number, hi: number) => Math.floor(lo + rnd() * (hi - lo + 1))
  const pick = <T>(xs: readonly T[]) => xs[int(0, xs.length - 1)]!
  const asOf = '2026-01'
  const tiers: Tier[] = ['T1', 'T2', 'T3', 'T4']
  return inputs({
    asOfMonth: asOf,
    horizonMonths: int(12, 360),
    primeBps: int(500, 1500),
    includeT3InDrawdown: rnd() < 0.5,
    overdraftBps: pick([0, 0, 1800]),
    sweepAssetId: pick(['a0', 'a1', null]),
    assets: Array.from({ length: int(0, 6) }, (_, i) =>
      asset(`a${i}`, pick(tiers), int(0, 50_000_000), {
        growthBps: int(-1500, 1500),
        haircutBps: int(0, 10_000),
        accessibleCents: int(0, 5_000_000),
      }),
    ),
    debts: Array.from({ length: int(0, 3) }, (_, i) => {
      const end = addMonths(asOf, int(-2, 300))
      return rnd() < 0.5
        ? fixedDebt(`d${i}`, int(0, 300_000_000), int(0, 2500), int(0, 3_000_000), end)
        : variableDebt(`d${i}`, int(0, 300_000_000), int(-200, 800), int(0, 3_000_000), end)
    }),
    obligations: Array.from({ length: int(0, 5) }, (_, i) =>
      obligation(`o${i}`, int(0, 5_000_000), {
        frequency: pick(['monthly', 'annual'] as const),
        paymentMonth: int(1, 12),
        escalationBps: int(0, 1500),
        escalationMonth: int(1, 12),
        startMonth: addMonths(asOf, int(-12, 120)),
        endMonth: pick([null, addMonths(asOf, int(0, 360))]),
      }),
    ),
    incomes: Array.from({ length: int(0, 4) }, (_, i) =>
      income(`i${i}`, int(0, 10_000_000), {
        frequency: pick(['monthly', 'annual', 'irregular'] as const),
        months: [int(1, 12), int(1, 12)],
        growthBps: int(-500, 1000),
        growthMonth: int(1, 12),
        startMonth: addMonths(asOf, int(-12, 60)),
        endMonth: pick([null, addMonths(asOf, int(0, 360))]),
        confidence: pick(['committed', 'variable'] as const),
      }),
    ),
    events: Array.from({ length: int(0, 4) }, (_, i) =>
      event(`e${i}`, addMonths(asOf, int(0, 360)), int(0, 50_000_000), pick(['inflow', 'outflow'] as const)),
    ),
  })
}

describe('conservation and non-negativity invariants', () => {
  it('holds for the sample household under every scenario and runway variant', () => {
    const sample = { ...buildSampleInputs('2026-09'), horizonMonths: 360 }
    const variants = [
      {},
      ...PRESET_IDS.map((id) => resolveOverrides({ presets: [id], custom: {} })),
      resolveOverrides({ presets: [...PRESET_IDS], custom: {} }),
      { variableIncomeFactor: 0 },
      { variableIncomeFactor: 0, committedIncomeFactor: 0 },
      { variableIncomeFactor: 0, committedIncomeFactor: 0, investmentGrowthDeltaBps: -2000, haircutDeltaBps: 2000 },
    ]
    for (const overrides of variants) {
      expect(checkInvariants(project(applyOverrides(sample, overrides)))).toEqual([])
    }
    expect(checkInvariants(project({ ...sample, includeT3InDrawdown: true, overdraftBps: 2000 }))).toEqual([])
  })

  it('holds for 300 generated households', () => {
    for (let seed = 1; seed <= 300; seed++) {
      const errors = checkInvariants(project(randomHousehold(seed)))
      expect(errors.slice(0, 3), `seed ${seed}`).toEqual([])
    }
  })
})
