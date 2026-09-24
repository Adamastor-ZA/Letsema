import type { EntityTable } from 'dexie'
import { buildSampleInputs } from '../sample/sample-data'
import { datasetSchema, inputsToDataset, SCHEMA_VERSION, type Dataset } from '../schema/dataset'
import { entitySchemas, type EntityKind, type EntityRecords } from '../schema/entities'
import { defaultSettings, settingsSchema, type Settings } from '../schema/settings'
import { db } from './db'

export function currentYearMonth(now = new Date()): string {
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
}

export function newId(): string {
  return crypto.randomUUID()
}

function table<K extends EntityKind>(kind: K) {
  return db[kind] as unknown as EntityTable<EntityRecords[K], 'id'>
}

export async function getSettings(): Promise<Settings> {
  return (await db.settings.get('settings')) ?? defaultSettings(currentYearMonth())
}

export async function saveSettings(settings: Settings): Promise<void> {
  const parsed = settingsSchema.parse(settings)
  if (parsed.sweepAssetId !== null) {
    const target = await db.assets.get(parsed.sweepAssetId)
    if (!target || (target.tier !== 'T1' && target.tier !== 'T2')) throw new Error('Sweep asset must be a T1 or T2 asset')
  }
  await db.settings.put(parsed)
}

export async function updateSettings(patch: Partial<Omit<Settings, 'id'>>): Promise<void> {
  await saveSettings({ ...(await getSettings()), ...patch })
}

/** Next sort position at the end of a list. */
export async function nextSortOrder(kind: EntityKind): Promise<number> {
  const last = await table(kind).orderBy('sortOrder').last()
  return last ? last.sortOrder + 1 : 0
}

/** Validate and store an entity. Returns the stored record. */
export async function saveEntity<K extends EntityKind>(kind: K, record: EntityRecords[K]): Promise<EntityRecords[K]> {
  const parsed = entitySchemas[kind].parse(record) as EntityRecords[K]
  await db.transaction('rw', [table(kind), db.settings], async () => {
    await table(kind).put(parsed)
    // An asset moved out of T1/T2 can no longer be the sweep target.
    if (kind === 'assets') {
      const settings = await db.settings.get('settings')
      const asset = parsed as EntityRecords['assets']
      if (settings?.sweepAssetId === asset.id && asset.tier !== 'T1' && asset.tier !== 'T2') {
        await db.settings.put({ ...settings, sweepAssetId: null })
      }
    }
  })
  return parsed
}

/** Delete an entity and clear references to it (sweep target, scenario exclusions). */
export async function deleteEntity(kind: EntityKind, id: string): Promise<void> {
  await db.transaction('rw', [table(kind), db.settings, db.scenarios], async () => {
    await table(kind).delete(id)
    const settings = await db.settings.get('settings')
    if (settings?.sweepAssetId === id) await db.settings.put({ ...settings, sweepAssetId: null })
    await db.scenarios
      .filter((s) => s.custom.excludedIds?.includes(id) ?? false)
      .modify((s) => {
        s.custom.excludedIds = s.custom.excludedIds?.filter((x) => x !== id)
      })
  })
}

/** Swap an entity with its neighbour in list order. */
export async function moveEntity(kind: EntityKind, id: string, direction: -1 | 1): Promise<void> {
  await db.transaction('rw', table(kind), async () => {
    const items = await table(kind).orderBy('sortOrder').toArray()
    const i = items.findIndex((x) => x.id === id)
    const j = i + direction
    if (i === -1 || j < 0 || j >= items.length) return
    const a = items[i]!
    const b = items[j]!
    // Renumber so that ties from imported data cannot make the swap a no-op.
    const reordered = [...items]
    reordered[i] = b
    reordered[j] = a
    await table(kind).bulkPut(reordered.map((x, sortOrder) => ({ ...x, sortOrder })))
  })
}

export async function readDataset(): Promise<Dataset> {
  const [settings, assets, debts, obligations, incomes, events, scenarios, snapshots] = await Promise.all([
    getSettings(),
    db.assets.orderBy('sortOrder').toArray(),
    db.debts.orderBy('sortOrder').toArray(),
    db.obligations.orderBy('sortOrder').toArray(),
    db.incomes.orderBy('sortOrder').toArray(),
    db.events.orderBy('sortOrder').toArray(),
    db.scenarios.toArray(),
    db.snapshots.orderBy('month').toArray(),
  ])
  return { schemaVersion: SCHEMA_VERSION, settings, assets, debts, obligations, incomes, events, scenarios, snapshots }
}

/** Validate a whole dataset and replace everything stored with it, atomically. */
export async function replaceDataset(dataset: unknown): Promise<void> {
  const d = datasetSchema.parse(dataset) as Dataset
  await db.transaction('rw', db.allTables, async () => {
    await Promise.all(db.allTables.map((t) => t.clear()))
    await Promise.all([
      db.settings.put(d.settings),
      db.assets.bulkPut(d.assets),
      db.debts.bulkPut(d.debts),
      db.obligations.bulkPut(d.obligations),
      db.incomes.bulkPut(d.incomes),
      db.events.bulkPut(d.events),
      db.scenarios.bulkPut(d.scenarios),
      db.snapshots.bulkPut(d.snapshots),
    ])
  })
}

export async function clearAllData(): Promise<void> {
  await db.transaction('rw', db.allTables, async () => {
    await Promise.all(db.allTables.map((t) => t.clear()))
  })
}

/** Replace all data with the fictional sample household, dated from `asOfMonth`. Keeps display preferences. */
export async function loadSampleData(asOfMonth = currentYearMonth()): Promise<void> {
  const current = await getSettings()
  await replaceDataset(inputsToDataset(buildSampleInputs(asOfMonth), { ...current, lastExportAt: null }))
}

export async function hasAnyData(): Promise<boolean> {
  const counts = await Promise.all([db.assets.count(), db.debts.count(), db.obligations.count(), db.incomes.count(), db.events.count()])
  return counts.some((n) => n > 0)
}
