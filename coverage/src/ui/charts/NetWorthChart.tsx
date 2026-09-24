import { useMemo } from 'react'
import { Bar, CartesianGrid, ComposedChart, Line, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { Position, ProjectionResult, Tier } from '../../engine/types'
import { TIER_LABELS } from '../editors/configs'
import type { Formatter } from '../lib/format'
import { ChartCard, type LegendItem } from './ChartCard'
import { ChartTooltipBox, type TooltipRow } from './ChartTooltip'
import { AXIS_TICK, DEBT_FILL, INK, SERIES } from './theme'

const TIERS: Tier[] = ['T1', 'T2', 'T3', 'T4']
const TIER_COLOR: Record<Tier, string> = { T1: SERIES[0], T2: SERIES[1], T3: SERIES[2], T4: SERIES[3] }

interface Point {
  label: string
  month: string
  T1: number
  T2: number
  T3: number
  T4: number
  debt: number
  netWorth: number
}

/** Opening position, then the position at each 12-month step to the horizon. */
export function yearlyPositions(result: ProjectionResult): { label: string; month: string; monthsElapsed: number; position: Position }[] {
  const points = [{ label: 'Now', month: result.rows[0]?.month ?? '', monthsElapsed: 0, position: result.opening as Position }]
  result.rows.forEach((r, i) => {
    if ((i + 1) % 12 === 0) points.push({ label: '', month: r.month, monthsElapsed: i + 1, position: r })
  })
  return points
}

export function NetWorthChart({
  result,
  fmt,
  display,
  actions,
}: {
  result: ProjectionResult
  fmt: Formatter
  display: (cents: number, monthsElapsed: number) => number
  actions?: React.ReactNode
}) {
  const data: Point[] = useMemo(
    () =>
      yearlyPositions(result).map((p) => {
        const d = (c: number) => display(c, p.monthsElapsed)
        return {
          label: p.label || fmt.month(p.month),
          month: p.month,
          T1: d(p.position.tiers.T1),
          T2: d(p.position.tiers.T2),
          T3: d(p.position.tiers.T3),
          T4: d(p.position.tiers.T4),
          debt: -d(p.position.debtCents + p.position.deficitCents),
          netWorth: d(p.position.netWorthCents),
        }
      }),
    [result, display, fmt],
  )

  const legend: LegendItem[] = [
    ...TIERS.map((t) => ({ key: t, label: TIER_LABELS[t], color: TIER_COLOR[t], shape: 'rect' as const })),
    { key: 'debt', label: 'Debt and carried deficit', color: DEBT_FILL, shape: 'rect' },
    { key: 'netWorth', label: 'Net worth', color: INK.primary, shape: 'line' },
  ]

  const rowsFor = (p: Point): TooltipRow[] => [
    { key: 'netWorth', label: 'Net worth', value: fmt.money(p.netWorth), color: INK.primary, shape: 'line' },
    ...[...TIERS].reverse().map((t) => ({ key: t, label: TIER_LABELS[t], value: fmt.money(p[t]), color: TIER_COLOR[t], shape: 'rect' as const })),
    { key: 'debt', label: 'Debt and deficit', value: fmt.money(p.debt), color: DEBT_FILL, shape: 'rect' },
  ]

  const chart = (
    <div role="img" aria-label="Net worth by liquidity tier at each year, with debt below zero. Switch to the table view for values.">
      <ResponsiveContainer width="100%" height={340}>
        <ComposedChart data={data} stackOffset="sign" margin={{ top: 8, right: 12, bottom: 0, left: 4 }} barCategoryGap="30%">
          <CartesianGrid stroke={INK.grid} vertical={false} />
          <XAxis dataKey="label" tick={AXIS_TICK} tickLine={false} axisLine={{ stroke: INK.axis }} minTickGap={16} />
          <YAxis tickFormatter={(v: number) => fmt.moneyCompact(v)} tick={AXIS_TICK} tickLine={false} axisLine={false} width={72} />
          <ReferenceLine y={0} stroke={INK.secondary} strokeWidth={1} />
          <Tooltip
            cursor={{ fill: 'rgba(15, 23, 42, 0.04)' }}
            isAnimationActive={false}
            content={({ active, payload }) => {
              const p = payload?.[0]?.payload as Point | undefined
              return active && p ? <ChartTooltipBox title={p.label === 'Now' ? 'Now' : p.label} rows={rowsFor(p)} /> : null
            }}
          />
          {TIERS.map((t) => (
            <Bar key={t} dataKey={t} stackId="position" fill={TIER_COLOR[t]} stroke={INK.surface} strokeWidth={1} maxBarSize={24} isAnimationActive={false} />
          ))}
          <Bar dataKey="debt" stackId="position" fill={DEBT_FILL} stroke={INK.surface} strokeWidth={1} maxBarSize={24} isAnimationActive={false} />
          <Line
            dataKey="netWorth"
            stroke={INK.primary}
            strokeWidth={2}
            dot={{ r: 4, fill: INK.primary, stroke: INK.surface, strokeWidth: 2 }}
            activeDot={{ r: 5, stroke: INK.surface, strokeWidth: 2 }}
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )

  const table = (
    <table className="w-full text-sm">
      <thead className="sticky top-0 bg-white text-left text-xs text-slate-500">
        <tr>
          <th scope="col" className="py-1 pr-3 font-medium">
            As at
          </th>
          {TIERS.map((t) => (
            <th key={t} scope="col" className="py-1 pl-3 text-right font-medium">
              {TIER_LABELS[t]}
            </th>
          ))}
          <th scope="col" className="py-1 pl-3 text-right font-medium">
            Debt and deficit
          </th>
          <th scope="col" className="py-1 pl-3 text-right font-medium">
            Net worth
          </th>
        </tr>
      </thead>
      <tbody className="divide-y divide-slate-100">
        {data.map((p) => (
          <tr key={p.month + p.label}>
            <th scope="row" className="py-1 pr-3 text-left font-normal">
              {p.label}
            </th>
            {TIERS.map((t) => (
              <td key={t} className="num py-1 pl-3">
                {fmt.money(p[t])}
              </td>
            ))}
            <td className="num py-1 pl-3">{fmt.money(p.debt)}</td>
            <td className="num py-1 pl-3 font-medium">{fmt.money(p.netWorth)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )

  return (
    <ChartCard
      title="Net worth by tier"
      subtitle="Assets stacked by liquidity above zero, debt below, at each year to the horizon."
      legend={legend}
      chart={chart}
      table={table}
      actions={actions}
    />
  )
}
