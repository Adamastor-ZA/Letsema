import { LiquidChart } from '../charts/LiquidChart'
import { NetWorthChart } from '../charts/NetWorthChart'
import { DisplayToggle } from '../components/DisplayToggle'
import { Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'
import { useModel } from '../hooks/useModel'
import { GettingStarted } from './DashboardPage'

export function ProjectionPage({ ctx }: { ctx: EditorContext }) {
  const model = useModel(ctx.dataset)
  const { settings } = ctx.dataset
  if ('error' in model) return <Notice tone="error">The projection could not run: {model.error}</Notice>

  const e = model.evaluation
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
            subtitle="Liquid assets (T1, T2 after haircut and any accessible T3) less any carried deficit. Below zero, a shortfall is being carried. Select a legend item to show or hide it."
            fmt={ctx.fmt}
            display={model.display}
            firstShortfall={e.metrics.firstShortfall.month}
            height={360}
            series={[
              { key: 'base', label: 'Base case', rows: e.result.rows },
              { key: 'variableStops', label: 'Variable income stops', rows: e.variableStops.rows },
              { key: 'allStops', label: 'All income stops', rows: e.allIncomeStops.rows },
            ]}
          />
          <NetWorthChart result={e.result} fmt={ctx.fmt} display={model.display} />
          <p className="text-xs text-slate-500">Scenario lines (rate shock, income and cost stresses) are added to these charts in Phase 4.</p>
        </>
      )}
    </section>
  )
}
