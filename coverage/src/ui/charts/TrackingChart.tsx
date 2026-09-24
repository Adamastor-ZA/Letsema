import { useMemo } from 'react'
import { CartesianGrid, ComposedChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { TrackingPoint } from '../../db/checkin'
import type { Formatter } from '../lib/format'
import { ChartCard, type LegendItem } from './ChartCard'
import { ChartTooltipBox, type TooltipRow } from './ChartTooltip'
import { AXIS_TICK, BASE_COLOR, INK, PALETTE } from './theme'

const ACTUAL = PALETTE[1]

export function TrackingChart({
  points,
  fmt,
  metricLabel,
  baselineMonth,
  actions,
}: {
  points: TrackingPoint[]
  fmt: Formatter
  metricLabel: string
  baselineMonth: string
  actions?: React.ReactNode
}) {
  const legend: LegendItem[] = [
    { key: 'actual', label: 'Actual at check-in', color: ACTUAL, shape: 'line' },
    { key: 'projected', label: `Projected in ${fmt.month(baselineMonth)}`, color: BASE_COLOR, shape: 'line' },
  ]
  const actualCount = useMemo(() => points.filter((p) => p.actual !== undefined).length, [points])

  const chart = (
    <div role="img" aria-label={`${metricLabel}: actual at each check-in against the projection made in ${fmt.month(baselineMonth)}. Switch to the table view for values.`}>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={points} margin={{ top: 8, right: 12, bottom: 0, left: 4 }}>
          <CartesianGrid stroke={INK.grid} vertical={false} />
          <XAxis dataKey="month" tickFormatter={(m: string) => fmt.month(m)} tick={AXIS_TICK} tickLine={false} axisLine={{ stroke: INK.axis }} minTickGap={24} />
          <YAxis tickFormatter={(v: number) => fmt.moneyCompact(v)} tick={AXIS_TICK} tickLine={false} axisLine={false} width={72} domain={['auto', 'auto']} />
          <Tooltip
            cursor={{ stroke: INK.axis, strokeWidth: 1 }}
            isAnimationActive={false}
            content={({ active, payload }) => {
              const p = payload?.[0]?.payload as TrackingPoint | undefined
              if (!active || !p) return null
              const rows: TooltipRow[] = []
              if (p.actual !== undefined) rows.push({ key: 'a', label: 'Actual', value: fmt.money(p.actual), color: ACTUAL, shape: 'line' })
              if (p.projected !== undefined) rows.push({ key: 'p', label: 'Projected', value: fmt.money(p.projected), color: BASE_COLOR, shape: 'line' })
              const note = p.actual !== undefined && p.projected !== undefined ? `Difference ${fmt.money(p.actual - p.projected)}` : undefined
              return <ChartTooltipBox title={fmt.month(p.month)} rows={rows} note={note} />
            }}
          />
          <Line dataKey="projected" stroke={BASE_COLOR} strokeWidth={2} dot={false} isAnimationActive={false} connectNulls />
          <Line
            dataKey="actual"
            stroke={ACTUAL}
            strokeWidth={2}
            dot={{ r: 4, fill: ACTUAL, stroke: INK.surface, strokeWidth: 2 }}
            activeDot={{ r: 5, stroke: INK.surface, strokeWidth: 2 }}
            isAnimationActive={false}
            connectNulls
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
            Month
          </th>
          <th scope="col" className="py-1 pl-3 text-right font-medium">
            Actual
          </th>
          <th scope="col" className="py-1 pl-3 text-right font-medium">
            Projected
          </th>
          <th scope="col" className="py-1 pl-3 text-right font-medium">
            Difference
          </th>
        </tr>
      </thead>
      <tbody className="divide-y divide-slate-100">
        {points.map((p) => (
          <tr key={p.month}>
            <th scope="row" className="py-1 pr-3 text-left font-normal">
              {fmt.month(p.month)}
            </th>
            <td className="num py-1 pl-3">{p.actual === undefined ? '–' : fmt.money(p.actual)}</td>
            <td className="num py-1 pl-3">{p.projected === undefined ? '–' : fmt.money(p.projected)}</td>
            <td className="num py-1 pl-3">{p.actual !== undefined && p.projected !== undefined ? fmt.money(p.actual - p.projected) : '–'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )

  return (
    <ChartCard
      title={`${metricLabel}: actual against projected`}
      subtitle={
        actualCount < 2
          ? 'Each monthly check-in adds an actual point. The line is the path projected at the chosen check-in, in nominal terms.'
          : 'Actual balances at each check-in against the path projected at the chosen check-in, in nominal terms.'
      }
      legend={legend}
      chart={chart}
      table={table}
      actions={actions}
    />
  )
}
