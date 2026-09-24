/**
 * Prints the sample household's projection, headline metrics and scenario
 * comparison to the terminal. Run with `npm run demo [-- YYYY-MM]`.
 */
import {
  PRESET_IDS,
  PRESETS,
  compareScenarios,
  formatMoney,
  type Evaluation,
  type MonthRow,
  type Runway,
  type ScenarioDefinition,
} from '../src/engine'
import { buildSampleInputs } from '../src/sample/sample-data'

const inputs = buildSampleInputs(process.argv[2] ?? '2026-09')
const money = (cents: number) => formatMoney(cents)

function table(headers: string[], rows: string[][]): string {
  const widths = headers.map((h, i) => Math.max(h.length, ...rows.map((r) => r[i]!.length)))
  const line = (cells: string[]) => cells.map((c, i) => (i === 0 ? c.padEnd(widths[i]!) : c.padStart(widths[i]!))).join('  ')
  return [line(headers), widths.map((w) => '-'.repeat(w)).join('  '), ...rows.map(line)].join('\n')
}

const runway = (r: Runway) => (r.months === null ? 'beyond horizon' : `${r.months} months (${r.month})`)

function monthRow(r: MonthRow): string[] {
  return [
    r.month,
    money(r.incomeCents),
    money(r.obligationsCents + r.debtPaymentsCents + r.oneOffOutCents - r.oneOffInCents),
    money(r.netFlowCents),
    money(r.tiers.T1),
    money(r.tiers.T2),
    money(r.tiers.T3),
    money(r.tiers.T4),
    money(r.debtCents),
    money(r.liquidAssetsCents - r.deficitCents),
    money(r.netWorthCents),
    r.shortfall ? 'SHORT' : '',
  ]
}

const headers = ['Month', 'Income', 'Outgoings', 'Net flow', 'T1', 'T2', 'T3', 'T4', 'Debt', 'Liquid', 'Net worth', '']

const scenarios: ScenarioDefinition[] = [
  ...PRESET_IDS.map((id) => ({ id, name: PRESETS[id].label, presets: [id], custom: {} })),
  { id: 'combined', name: 'All three combined', presets: PRESET_IDS, custom: {} },
]
const comparison = compareScenarios(inputs, scenarios)
const base = comparison.base
const rows = base.result.rows

console.log(`Sample household, as of ${inputs.asOfMonth}, ${inputs.horizonMonths / 12}-year horizon (nominal)\n`)

console.log('Next 12 months')
console.log(table(headers, rows.slice(0, 12).map(monthRow)))

console.log('\nEach December thereafter')
console.log(table(headers, rows.filter((r, i) => i >= 12 && r.month.endsWith('-12')).map(monthRow)))

const retired = rows.flatMap((r) => r.debtsRetired.map((id) => `${inputs.debts.find((d) => d.id === id)?.name}: ${r.month}`))
console.log(`\nDebts retired: ${retired.join('; ') || 'none'}`)

const metricRows = (e: Evaluation) => {
  const m = e.metrics
  return [
    m.coverage.ratio === null ? 'n/a' : `${m.coverage.ratio.toFixed(2)}x`,
    runway(m.firstShortfall),
    runway(m.runwayVariableStops),
    runway(m.runwayAllIncomeStops),
    money(m.liquidNetWorthHorizonCents),
    money(m.netWorthHorizonCents),
  ]
}

console.log('\nHeadline metrics')
const c = base.metrics.coverage
console.log(
  `  12-month coverage: (${money(c.liquidCents)} liquid + ${money(c.committedIncomeCents)} committed income) / ` +
    `(${money(c.obligationsCents)} obligations + ${money(c.debtPaymentsCents)} debt + ${money(c.oneOffOutCents)} one-offs)`,
)
console.log(`  Net worth today ${money(base.metrics.netWorthTodayCents)}, liquid ${money(base.metrics.liquidNetWorthTodayCents)}`)

console.log('\nScenarios against base')
console.log(
  table(
    ['Scenario', 'Coverage', 'First shortfall', 'Runway (variable stops)', 'Runway (all stops)', 'Liquid NW at horizon', 'NW at horizon'],
    [
      ['Base case', ...metricRows(base)],
      ...comparison.scenarios.map((s) => [s.definition.name, ...metricRows(s.evaluation)]),
    ],
  ),
)
