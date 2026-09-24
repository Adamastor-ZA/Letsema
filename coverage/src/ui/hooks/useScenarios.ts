import { useMemo } from 'react'
import { evaluate, type Evaluation } from '../../engine/evaluate'
import { resolveOverrides } from '../../engine/scenarios'
import { datasetToInputs, type Dataset, type ScenarioRecord } from '../../schema/dataset'

export interface ScenarioRun {
  scenario: ScenarioRecord
  evaluation: Evaluation
}

export interface ScenarioModel {
  base: Evaluation
  /** Every stored scenario, evaluated, in colour-slot order. */
  runs: ScenarioRun[]
  active: ScenarioRun[]
}

/** Evaluate the base case and every stored scenario. Re-runs only when the data changes. */
export function useScenarios(dataset: Dataset): ScenarioModel | { error: string } {
  return useMemo(() => {
    try {
      const inputs = datasetToInputs(dataset)
      const runs = [...dataset.scenarios]
        .sort((a, b) => a.slot - b.slot)
        .map((scenario) => ({ scenario, evaluation: evaluate(inputs, resolveOverrides(scenario)) }))
      return { base: evaluate(inputs), runs, active: runs.filter((r) => r.scenario.active) }
    } catch (e) {
      return { error: e instanceof Error ? e.message : String(e) }
    }
  }, [dataset])
}
