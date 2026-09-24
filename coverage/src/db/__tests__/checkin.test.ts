import 'fake-indexeddb/auto'
import { beforeEach, describe, expect, it } from 'vitest'
import { datasetToInputs, inputsToDataset, type Dataset } from '../../schema/dataset'
import { defaultSettings } from '../../schema/settings'
import { buildSampleInputs } from '../../sample/sample-data'
import { project } from '../../engine/project'
import { planCheckIn, projectedAt, trackAgainstBaseline, SNAPSHOT_PATH_MONTHS } from '../checkin'
import { clearAllData, deleteSnapshot, loadSampleData, readDataset, saveCheckIn } from '../repo'

const sample = (): Dataset => inputsToDataset(buildSampleInputs('2026-09'), defaultSettings('2026-09'))
const at = '2026-10-01T08:00:00.000Z'

describe('projectedAt', () => {
  it('returns the opening position for the as-of month and end-of-month rows after it', () => {
    const d = sample()
    const result = project(datasetToInputs(d))
    expect(projectedAt(d, '2026-09')!.netWorthCents).toBe(result.opening.netWorthCents)
    const oct = projectedAt(d, '2026-10')!
    expect(oct.netWorthCents).toBe(result.rows[0]!.netWorthCents)
    expect(oct.assetValues['sample-money-market']).toBe(result.rows[0]!.assetValues['sample-money-market'])
    expect(projectedAt(d, '2026-08')).toBeNull()
  })
})

describe('planCheckIn', () => {
  it('records balances, moves the as-of month and rolls amounts forward', () => {
    const d = sample()
    const plan = planCheckIn(d, {
      month: '2027-02',
      assetValues: { 'sample-cheque': 5_000_000, 'sample-ra': 3_000_000 },
      debtBalances: { 'sample-credit-card': 0 },
      note: '  Bonus not yet paid  ',
      takenAt: at,
    })
    const next = plan.dataset
    expect(next.settings.asOfMonth).toBe('2027-02')
    expect(next.assets.find((a) => a.id === 'sample-cheque')!.valueCents).toBe(5_000_000)
    // Untouched values carry over.
    expect(next.assets.find((a) => a.id === 'sample-tfsa')!.valueCents).toBe(22_000_000)
    // The accessible amount is capped at the new value.
    expect(next.assets.find((a) => a.id === 'sample-ra')!.accessibleCents).toBe(3_000_000)
    expect(next.debts.find((d) => d.id === 'sample-credit-card')!.balanceCents).toBe(0)
    // Medical aid escalated 9% in January; salary's March increase is still to come.
    expect(next.obligations.find((o) => o.id === 'sample-medical')!.amountCents).toBe(850_200)
    expect(next.incomes.find((i) => i.id === 'sample-salary')!.amountCents).toBe(7_800_000)
    expect(plan.rolled.map((r) => r.id)).toContain('sample-medical')
    expect(plan.rolled.map((r) => r.id)).not.toContain('sample-salary')
    expect(plan.snapshot).toMatchObject({ id: 'snapshot-2027-02', month: '2027-02', takenAt: at, note: 'Bonus not yet paid' })
  })

  it('stores the actual totals and a start-of-month projected path', () => {
    const plan = planCheckIn(sample(), { month: '2026-10', assetValues: {}, debtBalances: {}, takenAt: at })
    const s = plan.snapshot
    const result = project(datasetToInputs(plan.dataset))
    expect(s.projected).toHaveLength(SNAPSHOT_PATH_MONTHS)
    expect(s.projected[0]).toEqual({ month: '2026-10', ...s.actual })
    expect(s.actual.netWorthCents).toBe(result.opening.netWorthCents)
    expect(s.projected[1]).toMatchObject({ month: '2026-11', netWorthCents: result.rows[0]!.netWorthCents })
    expect(s.assets).toHaveLength(7)
    expect(s.assets[0]).toMatchObject({ assetId: 'sample-cheque', tier: 'T1' })
  })

  it('replaces an earlier check-in for the same month and keeps snapshots in order', () => {
    const first = planCheckIn(sample(), { month: '2026-11', assetValues: {}, debtBalances: {}, takenAt: at }).dataset
    const second = planCheckIn(first, { month: '2026-11', assetValues: { 'sample-cheque': 1 }, debtBalances: {}, takenAt: at }).dataset
    expect(second.snapshots.map((s) => s.month)).toEqual(['2026-11'])
    expect(second.snapshots[0]!.assets[0]!.valueCents).toBe(1)
  })

  it('refuses to go back in time', () => {
    expect(() => planCheckIn(sample(), { month: '2026-08', assetValues: {}, debtBalances: {}, takenAt: at })).toThrow(/cannot go back/)
  })
})

describe('tracking actuals against a baseline', () => {
  it('pairs each later check-in with the baseline projection for that month', () => {
    let d = planCheckIn(sample(), { month: '2026-09', assetValues: {}, debtBalances: {}, takenAt: at }).dataset
    const baselinePath = d.snapshots[0]!.projected
    d = planCheckIn(d, { month: '2026-12', assetValues: { 'sample-cheque': 0 }, debtBalances: {}, takenAt: at }).dataset
    const points = trackAgainstBaseline(d.snapshots, 'snapshot-2026-09', 'netWorthCents')
    expect(points[0]).toEqual({ month: '2026-09', projected: baselinePath[0]!.netWorthCents, actual: baselinePath[0]!.netWorthCents })
    const dec = points.find((p) => p.month === '2026-12')!
    expect(dec.projected).toBe(baselinePath[3]!.netWorthCents)
    expect(dec.actual).toBe(d.snapshots[1]!.actual.netWorthCents)
    expect(points.filter((p) => p.actual !== undefined)).toHaveLength(2)
    // Runs twelve months past the baseline even with few check-ins.
    expect(points[points.length - 1]!.month).toBe('2027-09')
    expect(trackAgainstBaseline(d.snapshots, 'missing', 'netWorthCents')).toEqual([])
  })
})

describe('saveCheckIn', () => {
  beforeEach(async () => {
    await clearAllData()
    await loadSampleData('2026-09')
  })

  it('writes everything in one transaction', async () => {
    await saveCheckIn({ month: '2027-02', assetValues: { 'sample-cheque': 5_000_000 }, debtBalances: {}, takenAt: at })
    const d = await readDataset()
    expect(d.settings.asOfMonth).toBe('2027-02')
    expect(d.assets.find((a) => a.id === 'sample-cheque')!.valueCents).toBe(5_000_000)
    expect(d.obligations.find((o) => o.id === 'sample-medical')!.amountCents).toBe(850_200)
    expect(d.snapshots.map((s) => s.id)).toEqual(['snapshot-2027-02'])
    await deleteSnapshot('snapshot-2027-02')
    expect((await readDataset()).snapshots).toEqual([])
  })

  it('leaves everything untouched when the check-in is invalid', async () => {
    await expect(saveCheckIn({ month: '2027-02', assetValues: { 'sample-cheque': -1 }, debtBalances: {}, takenAt: at })).rejects.toThrow()
    const d = await readDataset()
    expect(d.settings.asOfMonth).toBe('2026-09')
    expect(d.snapshots).toEqual([])
  })
})
