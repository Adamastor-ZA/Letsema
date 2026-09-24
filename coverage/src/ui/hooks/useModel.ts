import { useMemo } from 'react'
import { forDisplay } from '../../engine/display'
import { evaluate, type Evaluation } from '../../engine/evaluate'
import { datasetToInputs, type Dataset } from '../../schema/dataset'

export interface Model {
  evaluation: Evaluation
  /** Convert a nominal amount `monthsElapsed` after the as-of month for display (nominal or real). */
  display: (cents: number, monthsElapsed: number) => number
  isEmpty: boolean
}

/** Run the base case for the stored data. Re-runs only when the data changes. */
export function useModel(dataset: Dataset): Model | { error: string } {
  return useMemo(() => {
    try {
      const evaluation = evaluate(datasetToInputs(dataset), {}, { detailMonths: 12 })
      const { display: mode, cpiBps } = dataset.settings
      const d = dataset
      return {
        evaluation,
        display: (cents: number, monthsElapsed: number) => forDisplay(cents, mode, cpiBps, monthsElapsed),
        isEmpty: d.assets.length + d.debts.length + d.obligations.length + d.incomes.length + d.events.length === 0,
      }
    } catch (e) {
      return { error: e instanceof Error ? e.message : String(e) }
    }
  }, [dataset])
}
