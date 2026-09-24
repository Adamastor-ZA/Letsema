import { useLiveQuery } from 'dexie-react-hooks'
import { useMemo } from 'react'
import { readDataset } from '../../db/repo'
import type { Dataset } from '../../schema/dataset'
import { makeFormatter, type Formatter } from '../lib/format'

/** The whole stored dataset, kept live as IndexedDB changes. Undefined while loading. */
export function useDataset(): Dataset | undefined {
  return useLiveQuery(readDataset, [])
}

export function useFormatter(dataset: Dataset | undefined): Formatter {
  const currency = dataset?.settings.currency ?? 'ZAR'
  const locale = dataset?.settings.locale ?? 'en-ZA'
  return useMemo(() => makeFormatter(currency, locale), [currency, locale])
}
