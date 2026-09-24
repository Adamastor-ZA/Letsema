import 'fake-indexeddb/auto'
import Dexie from 'dexie'
import { describe, expect, it } from 'vitest'
import { CoverageDB } from '../db'

describe('schema migration', () => {
  it('opens a version 1 database and keeps its data', async () => {
    const name = 'migration-test'
    const v1 = new Dexie(name)
    v1.version(1).stores({
      assets: 'id, sortOrder',
      debts: 'id, sortOrder',
      obligations: 'id, sortOrder',
      incomes: 'id, sortOrder',
      events: 'id, sortOrder, month',
      scenarios: 'id',
      snapshots: 'id, month',
      settings: 'id',
    })
    await v1.table('assets').put({ id: 'a', name: 'Cash', tier: 'T1', valueCents: 100, growthBps: 0, sortOrder: 0 })
    v1.close()

    const db = new CoverageDB(name)
    await db.open()
    expect(db.verno).toBe(2)
    expect(await db.assets.get('a')).toMatchObject({ name: 'Cash' })
    await db.scenarios.put({ id: 's', name: 'S', presets: [], custom: {}, active: true, slot: 3 })
    expect((await db.scenarios.orderBy('slot').toArray()).map((s) => s.id)).toEqual(['s'])
    db.close()
  })
})
