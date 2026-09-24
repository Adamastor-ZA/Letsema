import { useState } from 'react'
import { LiquidChart, type LiquidSeries } from '../charts/LiquidChart'
import { NetWorthChart } from '../charts/NetWorthChart'
import { BASE_COLOR, SERIES, scenarioColor } from '../charts/theme'
import { DisplayToggle } from '../components/DisplayToggle'
import { Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'
import { useModel } from '../hooks/useModel'
import { useScenarios } from '../hooks/useScenarios'
import { href } from '../routes'
import { GettingStarted } from './DashboardPage'

type Compare = 'scenarios' | 'income'

export function ProjectionPage({ ctx }: { ctx: EditorContext }) {
  const model = useModel(ctx.dataset)
  const scenarios = useScenarios(ctx.dataset)
  const [compare, setCompare] = useState<Compare>('scenarios')
  const [netWorthOf, setNetWorthOf] = useState('base')
  const { settings } = ctx.dataset
  if ('error' in model) return <Notice tone="error">The projection could not run: {model.error}</Notice>
  if ('error' in scenarios) return <Notice tone="error">A scenario could not run: {scenarios.error}</Notice>

  const e = model.evaluation
  const series: LiquidSeries[] =
    compare === 'scenarios'
      ? [
          { key: 'base', label: 'Base case', color: BASE_COLOR, rows: e.result.rows },
          ...scenarios.active.map((r) => ({ key: r.scenario.id, label: r.scenario.name, color: scenarioColor(r.scenario.slot), rows: r.evaluation.result.rows })),
        ]
      : [
          { key: 'base', label: 'Base case', color: SERIES[0], rows: e.result.rows },
          { key: 'variableStops', label: 'Variable income stops', color: SERIES[1], rows: e.variableStops.rows },
          { key: 'allStops', label: 'All income stops', color: SERIES[2], rows: e.allIncomeStops.rows },
        ]
  const netWorthRun = scenarios.runs.find((r) => r.scenario.id === netWorthOf)
  const netWorthResult = netWorthRun ? netWorthRun.evaluation.result : e.result

  return (
    <section className="space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold">Projection</h1>
          <p className="mt-1 text-sm text-slate-600">
            {settings.horizonYears} years from {ctx.fmt.month(settings.asOfMonth)}, month by month.
            {settings.display === 'real' && ` Amounts deflated by CPI of ${ctx.fmt.percent(settings.cpiBps)} a year.`}
          </p>
        </div>
        <DisplayToggle settings={settings} />
      </header>
      {model.isEmpty ? (
        <GettingStarted />
      ) : (
        <>
          <LiquidChart
            key={compare}
            subtitle={
              compare === 'scenarios' ? (
                <>
                  Liquid assets less any carried deficit, for the base case and each scenario ticked on the{' '}
                  <a className="text-brand-700 underline" href={href('scenarios')}>
                    Scenarios
                  </a>{' '}
                  page. Below zero, a shortfall is being carried.
                </>
              ) : (
                'Liquid assets less any carried deficit, with variable income or all income stopped from now. Below zero, a shortfall is being carried.'
              )
            }
            actions={
              <div role="group" aria-label="Compare" className="inline-flex rounded-md border border-slate-300 p-0.5 text-xs">
                {(
                  [
                    ['scenarios', 'Scenarios'],
                    ['income', 'Income stops'],
                  ] as const
                ).map(([value, label]) => (
                  <button
                    key={value}
                    type="button"
                    aria-pressed={compare === value}
                    className={`rounded px-2 py-0.5 ${compare === value ? 'bg-slate-800 text-white' : 'text-slate-600 hover:bg-slate-100'}`}
                    onClick={() => setCompare(value)}
                  >
                    {label}
                  </button>
                ))}
              </div>
            }
            fmt={ctx.fmt}
            display={model.display}
            firstShortfall={e.metrics.firstShortfall.month}
            height={360}
            series={series}
          />
          <NetWorthChart
            result={netWorthResult}
            fmt={ctx.fmt}
            display={model.display}
            actions={
              scenarios.runs.length > 0 && (
                <label className="flex items-center gap-1.5 text-xs text-slate-600">
                  <span>Showing</span>
                  <select className="input w-auto py-0.5 text-xs" value={netWorthOf} onChange={(ev) => setNetWorthOf(ev.target.value)}>
                    <option value="base">Base case</option>
                    {scenarios.runs.map((r) => (
                      <option key={r.scenario.id} value={r.scenario.id}>
                        {r.scenario.name}
                      </option>
                    ))}
                  </select>
                </label>
              )
            }
          />
        </>
      )}
    </section>
  )
}
