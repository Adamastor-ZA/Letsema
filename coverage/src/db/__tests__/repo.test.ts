import 'fake-indexeddb/auto'
import { beforeEach, describe, expect, it } from 'vitest'
import { datasetToInputs } from '../../schema/dataset'
import { buildSampleInputs } from '../../sample/sample-data'
import { db } from '../db'
import {
  clearAllData,
  deleteEntity,
  getSettings,
  hasAnyData,
  loadSampleData,
  moveEntity,
  nextSortOrder,
  readDataset,
  replaceDataset,
  saveEntity,
  saveSettings,
  updateSettings,
} from '../repo'
import type { AssetRecord } from '../../schema/entities'

const cash = (id: string, sortOrder: number, extra: Partial<AssetRecord> = {}): AssetRecord => ({
  id,
  name: id,
  tier: 'T1',
  valueCents: 100,
  growthBps: 0,
  sortOrder,
  ...extra,
})

beforeEach(async () => {
  await clearAllData()
})

describe('settings', () => {
  it('returns defaults until settings are saved', async () => {
    const s = await getSettings()
    expect(s).toMatchObject({ currency: 'ZAR', horizonYears: 10, display: 'nominal', sweepAssetId: null })
    expect(await db.settings.count()).toBe(0)
  })

  it('validates settings on save', async () => {
    await expect(updateSettings({ horizonYears: 31 })).rejects.toThrow()
    await updateSettings({ horizonYears: 30 })
    expect((await getSettings()).horizonYears).toBe(30)
  })

  it('only accepts a T1 or T2 sweep asset', async () => {
    await saveEntity('assets', cash('mm', 0))
    await saveEntity('assets', cash('house', 1, { tier: 'T4' }))
    await expect(updateSettings({ sweepAssetId: 'house' })).rejects.toThrow()
    await expect(updateSettings({ sweepAssetId: 'missing' })).rejects.toThrow()
    await updateSettings({ sweepAssetId: 'mm' })
    expect((await getSettings()).sweepAssetId).toBe('mm')
  })
})

describe('entities', () => {
  it('validates before storing', async () => {
    await expect(saveEntity('assets', cash('bad', 0, { name: '  ' }))).rejects.toThrow()
    await expect(saveEntity('assets', cash('bad', 0, { valueCents: -1 }))).rejects.toThrow()
    expect(await db.assets.count()).toBe(0)
  })

  it('appends in list order', async () => {
    expect(await nextSortOrder('assets')).toBe(0)
    await saveEntity('assets', cash('a', 0))
    await saveEntity('assets', cash('b', 5))
    expect(await nextSortOrder('assets')).toBe(6)
  })

  it('reorders by swapping neighbours and ignores moves past the ends', async () => {
    for (const [i, id] of ['a', 'b', 'c'].entries()) await saveEntity('assets', cash(id, i))
    await moveEntity('assets', 'c', -1)
    expect((await readDataset()).assets.map((a) => a.id)).toEqual(['a', 'c', 'b'])
    await moveEntity('assets', 'a', -1)
    await moveEntity('assets', 'b', 1)
    expect((await readDataset()).assets.map((a) => a.id)).toEqual(['a', 'c', 'b'])
  })

  it('reorders items with tied sort orders', async () => {
    await saveEntity('assets', cash('a', 0))
    await saveEntity('assets', cash('b', 0))
    const before = (await readDataset()).assets.map((a) => a.id)
    await moveEntity('assets', before[1]!, -1)
    expect((await readDataset()).assets.map((a) => a.id)).toEqual([before[1], before[0]])
  })

  it('clears the sweep target when its asset is deleted or moved out of T1/T2', async () => {
    await saveEntity('assets', cash('mm', 0))
    await updateSettings({ sweepAssetId: 'mm' })
    await saveEntity('assets', cash('mm', 0, { tier: 'T3' }))
    expect((await getSettings()).sweepAssetId).toBeNull()

    await saveEntity('assets', cash('mm', 0))
    await updateSettings({ sweepAssetId: 'mm' })
    await deleteEntity('assets', 'mm')
    expect((await getSettings()).sweepAssetId).toBeNull()
  })

  it('removes deleted ids from scenario exclusions', async () => {
    await db.scenarios.put({ id: 's', name: 's', presets: [], custom: { excludedIds: ['x', 'y'] }, active: true, slot: 1 })
    await saveEntity('assets', cash('x', 0))
    await deleteEntity('assets', 'x')
    expect((await db.scenarios.get('s'))?.custom.excludedIds).toEqual(['y'])
  })
})

describe('whole dataset', () => {
  it('loads the sample household and round-trips it to engine inputs', async () => {
    expect(await hasAnyData()).toBe(false)
    await loadSampleData('2026-09')
    expect(await hasAnyData()).toBe(true)
    const inputs = datasetToInputs(await readDataset())
    expect(inputs).toEqual(buildSampleInputs('2026-09'))
  })

  it('keeps display preferences when loading the sample', async () => {
    await updateSettings({ currency: 'USD', display: 'real' })
    await loadSampleData('2026-09')
    expect(await getSettings()).toMatchObject({ currency: 'USD', display: 'real', sweepAssetId: 'sample-money-market' })
  })

  it('rejects an invalid dataset without touching stored data', async () => {
    await saveEntity('assets', cash('keep', 0))
    const d = await readDataset()
    await expect(replaceDataset({ ...d, assets: [...d.assets, cash('keep', 1)] })).rejects.toThrow(/Duplicate id/)
    await expect(replaceDataset({ ...d, schemaVersion: 99 })).rejects.toThrow()
    expect((await readDataset()).assets.map((a) => a.id)).toEqual(['keep'])
  })

  it('clears everything', async () => {
    await loadSampleData('2026-09')
    await saveSettings({ ...(await getSettings()), currency: 'EUR' })
    await clearAllData()
    expect(await hasAnyData()).toBe(false)
    expect((await getSettings()).currency).toBe('ZAR')
  })
})

describe('scenarios', () => {
  it('seeds the defaults once, and not again after they are deleted', async () => {
    const { ensureDefaultScenarios, deleteScenario } = await import('../repo')
    await ensureDefaultScenarios()
    expect((await readDataset()).scenarios.map((s) => s.name)).toEqual(['Rate shock', 'Variable income down 40%', 'Cost escalation', 'Combined stress'])
    await deleteScenario('default-rate-shock')
    await ensureDefaultScenarios()
    expect((await readDataset()).scenarios).toHaveLength(3)
  })

  it('restores deleted defaults into free colour slots', async () => {
    const { ensureDefaultScenarios, deleteScenario, restoreDefaultScenarios, saveScenario } = await import('../repo')
    await ensureDefaultScenarios()
    await deleteScenario('default-rate-shock')
    await saveScenario({ id: 'mine', name: 'Mine', presets: [], custom: { primeDeltaBps: 100 }, active: true, slot: 1 })
    expect(await restoreDefaultScenarios()).toBe(1)
    const scenarios = (await readDataset()).scenarios
    expect(scenarios.find((s) => s.id === 'default-rate-shock')?.slot).toBe(5)
    expect(new Set(scenarios.map((s) => s.slot)).size).toBe(scenarios.length)
  })

  it('enforces the scenario cap and unique colour slots', async () => {
    const { saveScenario, freeScenarioSlot } = await import('../repo')
    for (let slot = 1; slot <= 7; slot++) await saveScenario({ id: `s${slot}`, name: `S${slot}`, presets: [], custom: {}, active: false, slot })
    expect(await freeScenarioSlot()).toBeNull()
    await expect(saveScenario({ id: 's8', name: 'S8', presets: [], custom: {}, active: false, slot: 1 })).rejects.toThrow(/Up to 7/)
    await expect(saveScenario({ id: 's1', name: 'Renamed', presets: [], custom: {}, active: true, slot: 2 })).rejects.toThrow(/slot/)
    await saveScenario({ id: 's1', name: 'Renamed', presets: ['rateShock'], custom: {}, active: true, slot: 1 })
    expect((await readDataset()).scenarios[0]).toMatchObject({ name: 'Renamed', presets: ['rateShock'] })
  })

  it('ships the default scenarios with the sample data', async () => {
    await loadSampleData('2026-09')
    const d = await readDataset()
    expect(d.scenarios).toHaveLength(4)
    expect(d.settings.scenariosInitialised).toBe(true)
  })
})
