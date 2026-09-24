import type { ReactNode } from 'react'
import type { Evaluation, Metrics } from '../../engine/evaluate'
import { monthsBetween } from '../../engine/month'
import type { Settings } from '../../schema/settings'
import type { Formatter } from '../lib/format'
import { ragFor, type Rag } from '../lib/rag'
import { StatusPill } from './MetricCard'

export interface Column {
  key: string
  label: string
  color: string
  evaluation: Evaluation
}

interface Row {
  label: string
  help?: string
  value: (m: Metrics) => string
  /** Numeric value for the delta against base; higher is better. null when not comparable. */
  measure?: (m: Metrics) => number | null
  delta?: (d: number) => string
  status?: (m: Metrics) => Rag
}

function signed(text: string, d: number) {
  return `${d > 0 ? '+' : '−'}${text}`
}

function rows(settings: Settings, fmt: Formatter, display: (cents: number, monthsElapsed: number) => number, horizonMonths: number): Row[] {
  const t = settings.thresholds
  const atHorizon = (c: number) => display(c, horizonMonths)
  const months = (d: number) => signed(`${Math.abs(d)} ${Math.abs(d) === 1 ? 'month' : 'months'}`, d)
  const money = (d: number) => signed(fmt.moneyCompact(Math.abs(d)), d)
  const lowAt = (m: Metrics) => display(m.lowestLiquid.cents, monthsBetween(settings.asOfMonth, m.lowestLiquid.month) + 1)
  return [
    {
      label: '12-month coverage ratio',
      value: (m) => fmt.ratio(m.coverage.ratio),
      measure: (m) => m.coverage.ratio,
      delta: (d) => signed(`${Math.abs(d).toFixed(2)}×`, d),
      status: (m) => ragFor(m.coverage.ratio, t.coverageRatio),
    },
    {
      label: 'First shortfall',
      value: (m) => (m.firstShortfall.month ? fmt.month(m.firstShortfall.month) : 'None in horizon'),
      measure: (m) => m.firstShortfall.months,
      delta: months,
      status: (m) => ragFor(m.firstShortfall.months, t.firstShortfallMonths),
    },
    {
      label: 'Runway if variable income stops',
      value: (m) => fmt.runway(m.runwayVariableStops),
      measure: (m) => m.runwayVariableStops.months,
      delta: months,
      status: (m) => ragFor(m.runwayVariableStops.months, t.runwayVariableMonths),
    },
    {
      label: 'Runway if all income stops',
      value: (m) => fmt.runway(m.runwayAllIncomeStops),
      measure: (m) => m.runwayAllIncomeStops.months,
      delta: months,
      status: (m) => ragFor(m.runwayAllIncomeStops.months, t.runwayAllMonths),
    },
    {
      label: 'Lowest liquid balance',
      value: (m) => `${fmt.money(lowAt(m))} (${fmt.month(m.lowestLiquid.month)})`,
      measure: lowAt,
      delta: money,
    },
    {
      label: 'Liquid balance at horizon',
      value: (m) => fmt.money(atHorizon(m.liquidBalanceHorizonCents)),
      measure: (m) => atHorizon(m.liquidBalanceHorizonCents),
      delta: money,
    },
    {
      label: 'Net worth at horizon',
      value: (m) => fmt.money(atHorizon(m.netWorthHorizonCents)),
      measure: (m) => atHorizon(m.netWorthHorizonCents),
      delta: money,
    },
    {
      label: 'Liquid net worth at horizon',
      value: (m) => fmt.money(atHorizon(m.liquidNetWorthHorizonCents)),
      measure: (m) => atHorizon(m.liquidNetWorthHorizonCents),
      delta: money,
    },
  ]
}

function Delta({ base, value, format }: { base: number | null; value: number | null; format: (d: number) => string }): ReactNode {
  if (base === null && value === null) return <span className="text-slate-400">No change</span>
  if (base === null || value === null) {
    // One side never bites within the horizon.
    return value === null ? <span className="text-emerald-700">▲ Now beyond horizon</span> : <span className="text-red-700">▼ Now within horizon</span>
  }
  const d = value - base
  if (Math.abs(d) < 1e-9) return <span className="text-slate-400">No change</span>
  return d > 0 ? <span className="text-emerald-700">▲ {format(d)}</span> : <span className="text-red-700">▼ {format(d)}</span>
}

export function ComparisonTable({
  columns,
  settings,
  fmt,
  display,
}: {
  columns: Column[]
  settings: Settings
  fmt: Formatter
  display: (cents: number, monthsElapsed: number) => number
}) {
  const base = columns[0]!
  const horizonMonths = base.evaluation.result.rows.length
  return (
    <div className="card overflow-x-auto">
      <table className="w-full min-w-max text-sm">
        <caption className="sr-only">Headline metrics for the base case and each compared scenario, with the change against base</caption>
        <thead className="border-b border-slate-200 bg-slate-50 text-left text-xs font-medium text-slate-600">
          <tr>
            <th scope="col" className="sticky left-0 bg-slate-50 px-3 py-2">
              Metric
            </th>
            {columns.map((c) => (
              <th key={c.key} scope="col" className="px-3 py-2 align-bottom">
                <span className="flex items-center gap-1.5">
                  <span aria-hidden="true" className="inline-block h-0.5 w-4 rounded" style={{ background: c.color }} />
                  {c.label}
                </span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {rows(settings, fmt, display, horizonMonths).map((r) => (
            <tr key={r.label} className="align-top">
              <th scope="row" className="sticky left-0 bg-white px-3 py-2 text-left font-normal text-slate-700">
                {r.label}
              </th>
              {columns.map((c, i) => {
                const m = c.evaluation.metrics
                return (
                  <td key={c.key} className="px-3 py-2">
                    <div className="flex items-center gap-2">
                      <span className="font-medium whitespace-nowrap text-slate-900">{r.value(m)}</span>
                      {r.status && <StatusPill status={r.status(m)} />}
                    </div>
                    {i > 0 && r.measure && r.delta && (
                      <div className="mt-0.5 text-xs whitespace-nowrap">
                        <Delta base={r.measure(base.evaluation.metrics)} value={r.measure(m)} format={r.delta} />
                      </div>
                    )}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
