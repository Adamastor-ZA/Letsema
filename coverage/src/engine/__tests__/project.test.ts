import { describe, expect, it } from 'vitest'
import { project, UNALLOCATED_CASH_ID } from '../project'
import { asset, event, fixedDebt, income, inputs, obligation } from './helpers'

describe('drawdown order and haircuts', () => {
  it('draws T1 in order, then T2 net of haircut', () => {
    const result = project(
      inputs({
        horizonMonths: 1,
        assets: [asset('t1a', 'T1', 1_000), asset('t1b', 'T1', 1_000), asset('t2', 'T2', 10_000, { haircutBps: 2_000 })],
        obligations: [obligation('rent', 2_500)],
      }),
    )
    const row = result.rows[0]!
    expect(row.assetValues).toEqual({ t1a: 0, t1b: 0, t2: 9_375 })
    // R5 of cash from T2 at a 20% haircut means selling R6.25.
    expect(row).toMatchObject({ drawnCents: 2_500, haircutCents: 125, newDeficitCents: 0, shortfall: false })
  })

  it('draws the second T1 asset only after the first is empty', () => {
    const result = project(
      inputs({ horizonMonths: 1, assets: [asset('a', 'T1', 1_000), asset('b', 'T1', 1_000)], obligations: [obligation('o', 400)] }),
    )
    expect(result.rows[0]!.assetValues).toEqual({ a: 600, b: 1_000 })
  })

  it('touches T2 only when T1 is exhausted', () => {
    const result = project(
      inputs({ horizonMonths: 1, assets: [asset('t2', 'T2', 5_000, { haircutBps: 1_000 }), asset('t1', 'T1', 1_000)], obligations: [obligation('o', 900)] }),
    )
    expect(result.rows[0]!.assetValues).toEqual({ t2: 5_000, t1: 100 })
  })

  it('liquidates T2 fully net of haircut, then carries the rest as a deficit', () => {
    const result = project(
      inputs({ horizonMonths: 1, assets: [asset('t2', 'T2', 1_000, { haircutBps: 2_000 })], obligations: [obligation('o', 1_000)] }),
    )
    expect(result.rows[0]).toMatchObject({ drawnCents: 800, haircutCents: 200, newDeficitCents: 200, deficitCents: 200, shortfall: true })
  })

  it('skips an asset whose haircut is 100%', () => {
    const result = project(
      inputs({ horizonMonths: 1, assets: [asset('t2', 'T2', 1_000, { haircutBps: 10_000 })], obligations: [obligation('o', 100)] }),
    )
    expect(result.rows[0]!.assetValues.t2).toBe(1_000)
    expect(result.rows[0]!.deficitCents).toBe(100)
  })

  it('never draws T4, and draws T3 only when enabled and only up to the accessible amount', () => {
    const base = {
      horizonMonths: 1,
      assets: [
        asset('house', 'T4', 1_000_000),
        asset('ra', 'T3', 100_000, { accessibleCents: 10_000, haircutBps: 3_000 }),
      ],
      obligations: [obligation('o', 10_000)],
    }
    const locked = project(inputs(base)).rows[0]!
    expect(locked.assetValues).toEqual({ house: 1_000_000, ra: 100_000, [UNALLOCATED_CASH_ID]: 0 })
    expect(locked.deficitCents).toBe(10_000)

    const open = project(inputs({ ...base, includeT3InDrawdown: true })).rows[0]!
    expect(open.assetValues.ra).toBe(90_000)
    expect(open).toMatchObject({ drawnCents: 7_000, haircutCents: 3_000, deficitCents: 3_000, t3AccessibleNetCents: 0 })
  })

  it('reduces the remaining accessible T3 amount after a partial draw', () => {
    const result = project(
      inputs({
        horizonMonths: 2,
        includeT3InDrawdown: true,
        assets: [asset('ra', 'T3', 100_000, { accessibleCents: 10_000, haircutBps: 2_000 })],
        obligations: [obligation('o', 4_000)],
      }),
    )
    expect(result.rows[0]!.assetValues.ra).toBe(95_000)
    expect(result.rows[0]!.t3AccessibleNetCents).toBe(4_000)
    expect(result.rows[1]!.assetValues.ra).toBe(90_000)
    expect(result.rows[1]!.t3AccessibleNetCents).toBe(0)
  })
})

describe('zero balances and carried deficits', () => {
  it('carries an accumulating deficit when there are no assets at all', () => {
    const result = project(inputs({ horizonMonths: 3, obligations: [obligation('o', 100)] }))
    expect(result.rows.map((r) => r.deficitCents)).toEqual([100, 200, 300])
    expect(result.rows.every((r) => r.shortfall)).toBe(true)
    expect(result.rows[2]!.liquidNetWorthCents).toBe(-300)
    expect(result.rows[2]!.netWorthCents).toBe(-300)
  })

  it('repays a carried deficit from later surpluses before sweeping', () => {
    const result = project(
      inputs({ horizonMonths: 3, incomes: [income('pay', 600)], events: [event('bill', '2026-01', 1_000, 'outflow')] }),
    )
    const [m0, m1, m2] = result.rows
    expect(m0).toMatchObject({ netFlowCents: -400, deficitCents: 400, shortfall: true })
    expect(m1).toMatchObject({ deficitRepaidCents: 400, sweptCents: 200, deficitCents: 0, shortfall: false })
    expect(m1!.assetValues[UNALLOCATED_CASH_ID]).toBe(200)
    expect(m2!.assetValues[UNALLOCATED_CASH_ID]).toBe(800)
  })

  it('partially repays a deficit larger than the surplus', () => {
    const result = project(
      inputs({ horizonMonths: 2, incomes: [income('pay', 100)], events: [event('bill', '2026-01', 1_000, 'outflow')] }),
    )
    expect(result.rows.map((r) => r.deficitCents)).toEqual([900, 800])
    expect(result.rows[1]!.shortfall).toBe(true)
  })

  it('charges overdraft interest on a carried deficit when configured', () => {
    const result = project(inputs({ horizonMonths: 2, overdraftBps: 1_200, events: [event('bill', '2026-01', 100_000, 'outflow')] }))
    expect(result.rows[1]).toMatchObject({ deficitInterestCents: 1_000, deficitCents: 101_000 })
  })
})

describe('sweep', () => {
  it('sweeps surplus into the designated asset', () => {
    const result = project(
      inputs({ horizonMonths: 1, sweepAssetId: 't2', assets: [asset('t1', 'T1', 0), asset('t2', 'T2', 0)], incomes: [income('pay', 500)] }),
    )
    expect(result.rows[0]!.assetValues).toEqual({ t1: 0, t2: 500 })
  })

  it('falls back to the first T1 asset when the sweep target is missing or not T1/T2', () => {
    for (const sweepAssetId of [null, 'nope', 'house']) {
      const result = project(
        inputs({
          horizonMonths: 1,
          sweepAssetId,
          assets: [asset('house', 'T4', 0), asset('t1', 'T1', 0)],
          incomes: [income('pay', 500)],
        }),
      )
      expect(result.rows[0]!.assetValues).toEqual({ house: 0, t1: 500 })
    }
  })

  it('does not grow a surplus in the month it arrives', () => {
    const result = project(inputs({ horizonMonths: 2, assets: [asset('mm', 'T1', 0, { growthBps: 1_200 })], incomes: [income('pay', 100_000)] }))
    expect(result.rows[0]!.assetValues.mm).toBe(100_000)
    expect(result.rows[1]!.assetValues.mm).toBeGreaterThan(200_000)
  })
})

describe('growth, events and ordering', () => {
  it('compounds asset growth monthly to the annual rate', () => {
    const result = project(inputs({ assets: [asset('ut', 'T2', 100_000_000, { growthBps: 1_200 })] }))
    expect(Math.abs(result.rows[11]!.assetValues.ut! - 112_000_000)).toBeLessThanOrEqual(12)
  })

  it('shrinks depreciating assets without going negative', () => {
    const result = project(inputs({ assets: [asset('car', 'T4', 10_000_000, { growthBps: -2_000 })] }))
    expect(Math.abs(result.rows[11]!.assetValues.car! - 8_000_000)).toBeLessThanOrEqual(12)
  })

  it('grows assets before drawing on them', () => {
    const result = project(
      inputs({ horizonMonths: 1, assets: [asset('mm', 'T1', 1_000_000, { growthBps: 1_200 })], obligations: [obligation('o', 100_000)] }),
    )
    const growth = result.rows[0]!.growthCents
    expect(growth).toBeGreaterThan(0)
    expect(result.rows[0]!.assetValues.mm).toBe(1_000_000 + growth - 100_000)
  })

  it('applies one-off events in their month only', () => {
    const result = project(
      inputs({
        horizonMonths: 3,
        events: [event('in', '2026-02', 5_000, 'inflow'), event('out', '2026-02', 2_000, 'outflow'), event('late', '2031-01', 1, 'inflow')],
      }),
    )
    expect(result.rows.map((r) => [r.oneOffInCents, r.oneOffOutCents])).toEqual([
      [0, 0],
      [5_000, 2_000],
      [0, 0],
    ])
    expect(result.rows[1]!.netFlowCents).toBe(3_000)
  })

  it('nets every flow of the month before settling', () => {
    const result = project(
      inputs({
        horizonMonths: 1,
        incomes: [income('pay', 10_000)],
        obligations: [obligation('o', 3_000)],
        debts: [fixedDebt('loan', 100_000, 0, 2_000, '2030-01')],
        events: [event('e', '2026-01', 1_000, 'outflow')],
        assets: [asset('cash', 'T1', 0)],
      }),
    )
    expect(result.rows[0]).toMatchObject({ netFlowCents: 4_000, sweptCents: 4_000 })
  })
})

describe('positions', () => {
  it('reports the opening position and the net worth definitions', () => {
    const result = project(
      inputs({
        assets: [
          asset('cash', 'T1', 100_000),
          asset('ut', 'T2', 200_000, { haircutBps: 1_000 }),
          asset('ra', 'T3', 500_000, { accessibleCents: 50_000, haircutBps: 3_000 }),
          asset('house', 'T4', 1_000_000),
        ],
        debts: [fixedDebt('bond', 800_000, 0, 0, '2040-01')],
      }),
    )
    expect(result.opening).toMatchObject({
      tiers: { T1: 100_000, T2: 200_000, T3: 500_000, T4: 1_000_000 },
      t2NetCents: 180_000,
      t3AccessibleNetCents: 35_000,
      liquidAssetsCents: 315_000,
      debtCents: 800_000,
      netWorthCents: 1_000_000,
      liquidNetWorthCents: -485_000,
    })
  })

  it('rejects horizons outside 1–360 months', () => {
    expect(() => project(inputs({ horizonMonths: 0 }))).toThrow()
    expect(() => project(inputs({ horizonMonths: 361 }))).toThrow()
    expect(() => project(inputs({ horizonMonths: 12.5 }))).toThrow()
    expect(project(inputs({ horizonMonths: 360 })).rows).toHaveLength(360)
  })

  it('labels rows from the as-of month', () => {
    const result = project(inputs({ asOfMonth: '2026-11', horizonMonths: 3 }))
    expect(result.rows.map((r) => [r.index, r.month])).toEqual([
      [0, '2026-11'],
      [1, '2026-12'],
      [2, '2027-01'],
    ])
  })
})
