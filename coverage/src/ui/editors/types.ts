import type { ReactNode } from 'react'
import type { Dataset } from '../../schema/dataset'
import type { EntityKind, EntityRecords } from '../../schema/entities'
import type { Formatter } from '../lib/format'
import type { FieldDef } from './fields'

export interface EditorContext {
  dataset: Dataset
  fmt: Formatter
}

export interface Column<R> {
  label: string
  render: (record: R, ctx: EditorContext) => ReactNode
  numeric?: boolean
  /** Hide on narrow screens. */
  secondary?: boolean
}

export interface Warning {
  tone: 'warn' | 'info'
  text: string
}

export interface EntityConfig<K extends EntityKind> {
  kind: K
  title: string
  singular: string
  intro: ReactNode
  fields: (ctx: EditorContext) => FieldDef[]
  defaults: (ctx: EditorContext) => Partial<EntityRecords[K]>
  columns: Column<EntityRecords[K]>[]
  warnings?: (record: EntityRecords[K], ctx: EditorContext) => Warning[]
  summary?: (records: EntityRecords[K][], ctx: EditorContext) => ReactNode
  /** Items can be reordered, with an explanation of what the order means. */
  reorder?: string
  /** Display order when not reorderable. */
  sort?: (a: EntityRecords[K], b: EntityRecords[K]) => number
}
