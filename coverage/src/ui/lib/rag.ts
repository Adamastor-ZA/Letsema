import type { Thresholds } from '../../schema/settings'

export type Rag = 'green' | 'amber' | 'red'

export interface Band {
  green: number
  amber: number
}

/**
 * Status for a "higher is better" metric. `null` means the metric never
 * bites within the horizon (no shortfall, nothing due) and is green.
 */
export function ragFor(value: number | null, band: Band): Rag {
  if (value === null) return 'green'
  if (value >= band.green) return 'green'
  if (value >= band.amber) return 'amber'
  return 'red'
}

export const RAG_LABEL: Record<Rag, string> = { green: 'On track', amber: 'Watch', red: 'Act' }

export type ThresholdKey = keyof Thresholds
