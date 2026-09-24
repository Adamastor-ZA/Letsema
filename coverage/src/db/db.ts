import Dexie, { type EntityTable } from 'dexie'
import type { AssetRecord, DebtRecord, EventRecord, IncomeRecord, ObligationRecord } from '../schema/entities'
import type { ScenarioRecord, SnapshotRecord } from '../schema/dataset'
import type { Settings } from '../schema/settings'

export const DB_NAME = 'letsema-coverage'

export class CoverageDB extends Dexie {
  assets!: EntityTable<AssetRecord, 'id'>
  debts!: EntityTable<DebtRecord, 'id'>
  obligations!: EntityTable<ObligationRecord, 'id'>
  incomes!: EntityTable<IncomeRecord, 'id'>
  events!: EntityTable<EventRecord, 'id'>
  scenarios!: EntityTable<ScenarioRecord, 'id'>
  snapshots!: EntityTable<SnapshotRecord, 'id'>
  settings!: EntityTable<Settings, 'id'>

  constructor(name = DB_NAME) {
    super(name)
    this.version(1).stores({
      assets: 'id, sortOrder',
      debts: 'id, sortOrder',
      obligations: 'id, sortOrder',
      incomes: 'id, sortOrder',
      events: 'id, sortOrder, month',
      scenarios: 'id',
      snapshots: 'id, month',
      settings: 'id',
    })
    // v2: scenarios carry a fixed colour slot, indexed for display order.
    this.version(2).stores({ scenarios: 'id, slot' })
  }

  get allTables() {
    return [this.assets, this.debts, this.obligations, this.incomes, this.events, this.scenarios, this.snapshots, this.settings]
  }
}

export const db = new CoverageDB()
