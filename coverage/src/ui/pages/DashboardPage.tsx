import { useState } from 'react'
import type { Metrics } from '../../engine/evaluate'
import type { Settings } from '../../schema/settings'
import { LiquidChart } from '../charts/LiquidChart'
import { MetricCard } from '../components/MetricCard'
import { Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'
import { useModel } from '../hooks/useModel'
import { useScenarios, type ScenarioModel } from '../hooks/useScenarios'
import { BASE_COLOR, scenarioColor } from '../charts/theme'
import { StatusPill } from '../components/MetricCard'
import { ragFor } from '../lib/rag'
import { href } from '../routes'
import { ThresholdsDialog } from './ThresholdsDialog'
import { currentYearMonth } from '../../db/repo'
import { toIndex } from '../../engine/month'

const BACKUP_REMINDER_DAYS = 35

/** Nudges for the two habits the app depends on: monthly check-ins and backups. */
function Reminders({ settings, fmt, now = new Date() }: { settings: Settings; fmt: EditorContext['fmt']; now?: Date }) {
  const month = currentYearMonth(now)
  const checkInDue = toIndex(month) > toIndex(settings.asOfMonth)
  const daysSinceBackup = settings.lastExportAt ? Math.floor((now.getTime() - new Date(settings.lastExportAt).getTime()) / 86_400_000) : null
  const backupDue = daysSinceBackup === null || daysSinceBackup > BACKUP_REMINDER_DAYS
  if (!checkInDue && !backupDue) return null
  return (
    <div className="space-y-2">
      {checkInDue && (
        <Notice tone="warn">
          It is {fmt.month(month)} and the model is still as of {fmt.month(settings.asOfMonth)}.{' '}
          <a className="font-medium underline" href={href('checkin')}>
            Do your monthly check-in
          </a>
          .
        </Notice>
      )}
      {backupDue && (
        <Notice tone="warn">
          {daysSinceBackup === null ? 'You have not backed up yet.' : `Your last backup was ${daysSinceBackup} days ago.`} Your data lives only in this
          browser.{' '}
          <a className="font-medium underline" href={href('data')}>
            Export a backup
          </a>
          .
        </Notice>
      )}
    </div>
  )
}

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

function StressTests({ scenarios, settings, fmt, display }: { scenarios: ScenarioModel; settings: Settings; fmt: EditorContext['fmt']; display: (c: number, m: number) => number }) {
  const t = settings.thresholds
  const horizon = scenarios.base.result.rows.length
  const rows = [
    { key: 'base', name: 'Base case', color: BASE_COLOR, m: scenarios.base.metrics },
    ...scenarios.active.map((r) => ({ key: r.scenario.id, name: r.scenario.name, color: scenarioColor(r.scenario.slot), m: r.evaluation.metrics })),
  ]
  return (
    <section className="card p-4 sm:p-5" aria-label="Stress tests">
      <header className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="text-base font-semibold">Stress tests</h2>
        <a className="text-sm text-brand-700 underline" href={href('scenarios')}>
          {scenarios.active.length ? 'Compare in detail' : 'Choose scenarios to compare'}
        </a>
      </header>
      <div className="overflow-x-auto">
        <table className="w-full min-w-max text-sm">
          <thead className="text-left text-xs text-slate-500">
            <tr>
              <th scope="col" className="py-1 pr-3 font-medium">
                Scenario
              </th>
              <th scope="col" className="px-3 py-1 font-medium">
                Coverage
              </th>
              <th scope="col" className="px-3 py-1 font-medium">
                First shortfall
              </th>
              <th scope="col" className="px-3 py-1 text-right font-medium">
                Liquid balance at horizon
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((r) => (
              <tr key={r.key}>
                <th scope="row" className="py-1.5 pr-3 text-left font-normal">
                  <span className="flex items-center gap-1.5">
                    <span aria-hidden="true" className="inline-block h-0.5 w-4 rounded" style={{ background: r.color }} />
                    {r.name}
                  </span>
                </th>
                <td className="px-3 py-1.5">
                  <span className="flex items-center gap-2 whitespace-nowrap">
                    {fmt.ratio(r.m.coverage.ratio)} <StatusPill status={ragFor(r.m.coverage.ratio, t.coverageRatio)} />
                  </span>
                </td>
                <td className="px-3 py-1.5">
                  <span className="flex items-center gap-2 whitespace-nowrap">
                    {r.m.firstShortfall.month ? fmt.month(r.m.firstShortfall.month) : 'None'}{' '}
                    <StatusPill status={ragFor(r.m.firstShortfall.months, t.firstShortfallMonths)} />
                  </span>
                </td>
                <td className="num px-3 py-1.5">{fmt.money(display(r.m.liquidBalanceHorizonCents, horizon))}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

export function DashboardPage({ ctx }: { ctx: EditorContext }) {
  const model = useModel(ctx.dataset)
  const scenarios = useScenarios(ctx.dataset)
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

      <Reminders settings={settings} fmt={fmt} />

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

      {!('error' in scenarios) && <StressTests scenarios={scenarios} settings={settings} fmt={fmt} display={d} />}

      {editThresholds && <ThresholdsDialog thresholds={t} onClose={() => setEditThresholds(false)} />}
    </section>
  )
}
