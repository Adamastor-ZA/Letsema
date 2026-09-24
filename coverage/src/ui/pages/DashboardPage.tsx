import { useState } from 'react'
import type { Metrics } from '../../engine/evaluate'
import type { Settings } from '../../schema/settings'
import { LiquidChart } from '../charts/LiquidChart'
import { MetricCard } from '../components/MetricCard'
import { Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'
import { useModel } from '../hooks/useModel'
import { ragFor } from '../lib/rag'
import { href } from '../routes'
import { ThresholdsDialog } from './ThresholdsDialog'

function bandText(band: { green: number; amber: number }, unit: string) {
  return `Green at ${band.green}${unit} or more, amber at ${band.amber}${unit} or more`
}

export function GettingStarted() {
  return (
    <div className="card max-w-2xl space-y-3 p-6 text-sm text-slate-700">
      <h2 className="text-base font-semibold text-slate-900">Start by describing your position</h2>
      <p>
        This app answers one question: in any future month, do your liquid assets plus reliable income cover what you owe? Add your{' '}
        <a className="text-brand-700 underline" href={href('assets')}>
          assets
        </a>
        ,{' '}
        <a className="text-brand-700 underline" href={href('debts')}>
          debts
        </a>
        ,{' '}
        <a className="text-brand-700 underline" href={href('obligations')}>
          obligations
        </a>{' '}
        and{' '}
        <a className="text-brand-700 underline" href={href('incomes')}>
          income
        </a>
        , then come back here.
      </p>
      <p>
        Or load the fictional{' '}
        <a className="text-brand-700 underline" href={href('data')}>
          sample data
        </a>{' '}
        to explore first.
      </p>
    </div>
  )
}

function Headline({ metrics, settings, fmt }: { metrics: Metrics; settings: Settings; fmt: EditorContext['fmt'] }) {
  const first = metrics.firstShortfall
  if (first.month === null) return <>No shortfall before {fmt.month(metrics.horizonMonth)}, the end of the horizon.</>
  return (
    <>
      Liquid assets run out in <strong>{fmt.month(first.month)}</strong>, {first.months} months from now, on current assumptions
      {settings.includeT3InDrawdown ? ', even after drawing on accessible retirement savings' : ''}.
    </>
  )
}

export function DashboardPage({ ctx }: { ctx: EditorContext }) {
  const model = useModel(ctx.dataset)
  const [editThresholds, setEditThresholds] = useState(false)
  const { settings } = ctx.dataset
  const t = settings.thresholds
  const fmt = ctx.fmt

  if ('error' in model) return <Notice tone="error">The projection could not run: {model.error}</Notice>
  if (model.isEmpty) {
    return (
      <section className="space-y-4">
        <h1 className="text-xl font-semibold">Dashboard</h1>
        <GettingStarted />
      </section>
    )
  }

  const { metrics: m, result } = model.evaluation
  const horizonMonths = result.rows.length
  const c = m.coverage
  const d = model.display

  return (
    <section className="space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold">Dashboard</h1>
          <p className="mt-1 text-sm text-slate-600">
            <Headline metrics={m} settings={settings} fmt={fmt} />
          </p>
        </div>
        <button type="button" className="btn" onClick={() => setEditThresholds(true)}>
          Status thresholds
        </button>
      </header>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          hero
          label="12-month coverage ratio"
          value={fmt.ratio(c.ratio)}
          status={ragFor(c.ratio, t.coverageRatio)}
          detail={
            <>
              <p>
                {fmt.moneyCompact(c.numeratorCents)} available against {fmt.moneyCompact(c.denominatorCents)} due over 12 months.
              </p>
              <p className="mt-1 text-xs text-slate-500">
                Available: T1 and T2 after haircut {fmt.moneyCompact(c.liquidCents)}, committed income {fmt.moneyCompact(c.committedIncomeCents)}.
                Due: obligations {fmt.moneyCompact(c.obligationsCents)}, debt {fmt.moneyCompact(c.debtPaymentsCents)}
                {c.oneOffOutCents > 0 ? `, one-offs ${fmt.moneyCompact(c.oneOffOutCents)}` : ''}.
              </p>
            </>
          }
          threshold={bandText(t.coverageRatio, '×')}
        />
        <MetricCard
          label="First shortfall, base case"
          value={m.firstShortfall.month ? fmt.month(m.firstShortfall.month) : 'None in horizon'}
          status={ragFor(m.firstShortfall.months, t.firstShortfallMonths)}
          detail={m.firstShortfall.months !== null ? `${m.firstShortfall.months} months away` : `Covered to ${fmt.month(m.horizonMonth)}`}
          threshold={bandText(t.firstShortfallMonths, ' months')}
        />
        <MetricCard
          label="Runway if variable income stops"
          value={fmt.runway(m.runwayVariableStops)}
          status={ragFor(m.runwayVariableStops.months, t.runwayVariableMonths)}
          detail={m.runwayVariableStops.month ? `Short from ${fmt.month(m.runwayVariableStops.month)}` : `No shortfall in ${horizonMonths / 12} years`}
          threshold={bandText(t.runwayVariableMonths, ' months')}
        />
        <MetricCard
          label="Runway if all income stops"
          value={fmt.runway(m.runwayAllIncomeStops)}
          status={ragFor(m.runwayAllIncomeStops.months, t.runwayAllMonths)}
          detail={m.runwayAllIncomeStops.month ? `Short from ${fmt.month(m.runwayAllIncomeStops.month)}` : `No shortfall in ${horizonMonths / 12} years`}
          threshold={bandText(t.runwayAllMonths, ' months')}
        />
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        <MetricCard
          label="Liquid assets today"
          value={fmt.money(result.opening.liquidAssetsCents)}
          detail={`T1 ${fmt.moneyCompact(result.opening.tiers.T1)}, T2 after haircut ${fmt.moneyCompact(result.opening.t2NetCents)}, accessible T3 ${fmt.moneyCompact(result.opening.t3AccessibleNetCents)}`}
        />
        <MetricCard
          label="Net worth"
          value={fmt.money(m.netWorthTodayCents)}
          detail={`${fmt.money(d(m.netWorthHorizonCents, horizonMonths))} by ${fmt.month(m.horizonMonth)}${settings.display === 'real' ? " in today's money" : ''}`}
        />
        <MetricCard
          label="Liquid net worth"
          value={fmt.money(m.liquidNetWorthTodayCents)}
          detail={`${fmt.money(d(m.liquidNetWorthHorizonCents, horizonMonths))} by ${fmt.month(m.horizonMonth)}. Liquid assets less all debt.`}
        />
      </div>

      <LiquidChart
        title="Liquid balance"
        subtitle={
          <>
            Liquid assets less any carried deficit, in {settings.display === 'real' ? "today's money" : 'nominal terms'}. Select a legend item to show or hide it.{' '}
            <a className="text-brand-700 underline" href={href('projection')}>
              Full projection
            </a>
          </>
        }
        height={260}
        fmt={fmt}
        display={d}
        firstShortfall={m.firstShortfall.month}
        series={[
          { key: 'base', label: 'Base case', rows: result.rows },
          { key: 'variableStops', label: 'Variable income stops', rows: model.evaluation.variableStops.rows },
          { key: 'allStops', label: 'All income stops', rows: model.evaluation.allIncomeStops.rows, initiallyHidden: true },
        ]}
      />

      {editThresholds && <ThresholdsDialog thresholds={t} onClose={() => setEditThresholds(false)} />}
    </section>
  )
}
