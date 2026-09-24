import { coverageRatio, firstShortfall, type CoverageRatio, type Runway } from './metrics'
import { project } from './project'
import { applyOverrides, combineOverrides, resolveOverrides, type Overrides, type ScenarioDefinition } from './scenarios'
import type { ProjectionInputs, ProjectionResult, YearMonth } from './types'

export interface Metrics {
  coverage: CoverageRatio
  /** Base case of this scenario. */
  firstShortfall: Runway
  /** Same scenario with every variable income stream set to zero. */
  runwayVariableStops: Runway
  /** Same scenario with every income stream set to zero. One-off events still apply. */
  runwayAllIncomeStops: Runway
  netWorthTodayCents: number
  liquidNetWorthTodayCents: number
  netWorthHorizonCents: number
  liquidNetWorthHorizonCents: number
  horizonMonth: YearMonth
}

export interface Evaluation {
  /** Inputs after overrides. */
  inputs: ProjectionInputs
  result: ProjectionResult
  metrics: Metrics
}

export function evaluate(base: ProjectionInputs, overrides: Overrides = {}): Evaluation {
  const inputs = applyOverrides(base, overrides)
  const result = project(inputs)
  const variableStops = project(applyOverrides(base, combineOverrides(overrides, { variableIncomeFactor: 0 })))
  const allStops = project(
    applyOverrides(base, combineOverrides(overrides, { variableIncomeFactor: 0, committedIncomeFactor: 0 })),
  )
  const last = result.rows[result.rows.length - 1]!
  return {
    inputs,
    result,
    metrics: {
      coverage: coverageRatio(result),
      firstShortfall: firstShortfall(result.rows),
      runwayVariableStops: firstShortfall(variableStops.rows),
      runwayAllIncomeStops: firstShortfall(allStops.rows),
      netWorthTodayCents: result.opening.netWorthCents,
      liquidNetWorthTodayCents: result.opening.liquidNetWorthCents,
      netWorthHorizonCents: last.netWorthCents,
      liquidNetWorthHorizonCents: last.liquidNetWorthCents,
      horizonMonth: last.month,
    },
  }
}

export interface ScenarioComparison {
  base: Evaluation
  scenarios: { definition: ScenarioDefinition; evaluation: Evaluation }[]
}

export function compareScenarios(inputs: ProjectionInputs, definitions: ScenarioDefinition[]): ScenarioComparison {
  return {
    base: evaluate(inputs),
    scenarios: definitions.map((definition) => ({
      definition,
      evaluation: evaluate(inputs, resolveOverrides(definition)),
    })),
  }
}
