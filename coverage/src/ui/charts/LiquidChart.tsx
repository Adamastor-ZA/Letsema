import { useMemo, useState } from 'react'
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import type { MonthRow } from '../../engine/types'
import type { Formatter } from '../lib/format'
import { ChartCard, type LegendItem } from './ChartCard'
import { ChartTooltipBox } from './ChartTooltip'
import { AXIS_TICK, INK, SERIES } from './theme'

export interface LiquidSeries {
  key: string
  label: string
  rows: MonthRow[]
  /** Hidden until the user switches it on. */
  initiallyHidden?: boolean
}

interface LiquidChartProps {
  series: LiquidSeries[]
  fmt: Formatter
  display: (cents: number, monthsElapsed: number) => number
  title?: string
  subtitle?: React.ReactNode
  height?: number
  firstShortfall?: string | null
}

/** Liquid balance: liquid assets less any carried deficit. Negative means a shortfall is being carried. */
export const liquidBalance = (r: MonthRow) => r.liquidAssetsCents - r.deficitCents

export function yearTicks(months: string[]): string[] {
  const januaries = months.filter((m) => m.endsWith('-01'))
  const step = Math.max(1, Math.ceil(januaries.length / 10))
  return januaries.filter((_, i) => i % step === 0)
}

export function LiquidChart({ series, fmt, display, title = 'Liquid balance', subtitle, height = 320, firstShortfall }: LiquidChartProps) {
  const [hidden, setHidden] = useState<Set<string>>(() => new Set(series.filter((s) => s.initiallyHidden).map((s) => s.key)))
  const colors = useMemo(() => Object.fromEntries(series.map((s, i) => [s.key, SERIES[i % SERIES.length]!])), [series])

  const data = useMemo(() => {
    const base = series[0]?.rows ?? []
    return base.map((r, i) => {
      const point: Record<string, number | string> = { month: r.month }
      for (const s of series) {
        const row = s.rows[i]
        if (row) point[s.key] = display(liquidBalance(row), i + 1)
      }
      return point
    })
  }, [series, display])
  const ticks = useMemo(() => yearTicks(data.map((d) => String(d.month))), [data])

  const legend: LegendItem[] = series.map((s) => ({
    key: s.key,
    label: s.label,
    color: colors[s.key]!,
    shape: 'line',
    hidden: hidden.has(s.key),
    onToggle:
      series.length > 1
        ? () =>
            setHidden((h) => {
              const next = new Set(h)
              if (next.has(s.key)) next.delete(s.key)
              else next.add(s.key)
              return next
            })
        : undefined,
  }))

  const chart = (
    <div role="img" aria-label={`${title} by month for ${series.map((s) => s.label).join(', ')}. Switch to the table view for values.`}>
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: 4 }}>
          <CartesianGrid stroke={INK.grid} vertical={false} />
          <XAxis
            dataKey="month"
            ticks={ticks}
            tickFormatter={(m: string) => m.slice(0, 4)}
            tick={AXIS_TICK}
            tickLine={false}
            axisLine={{ stroke: INK.axis }}
            interval="preserveStartEnd"
            minTickGap={12}
          />
          <YAxis tickFormatter={(v: number) => fmt.moneyCompact(v)} tick={AXIS_TICK} tickLine={false} axisLine={false} width={72} />
          <ReferenceLine y={0} stroke={INK.secondary} strokeWidth={1} />
          {firstShortfall && (
            <ReferenceLine
              x={firstShortfall}
              stroke={INK.muted}
              strokeWidth={1}
              label={{ value: `First shortfall ${fmt.month(firstShortfall)}`, position: 'insideTopRight', fill: INK.secondary, fontSize: 12 }}
            />
          )}
          <Tooltip
            cursor={{ stroke: INK.axis, strokeWidth: 1 }}
            isAnimationActive={false}
            content={({ active, label }) =>
              active && label ? (
                <ChartTooltipBox
                  title={fmt.month(String(label))}
                  rows={series
                    .filter((s) => !hidden.has(s.key))
                    .map((s) => {
                      const point = data.find((d) => d.month === label)
                      return { key: s.key, label: s.label, value: fmt.money(Number(point?.[s.key] ?? 0)), color: colors[s.key]!, shape: 'line' as const }
                    })}
                />
              ) : null
            }
          />
          {series.map((s) =>
            hidden.has(s.key) ? null : (
              <Line
                key={s.key}
                type="linear"
                dataKey={s.key}
                name={s.label}
                stroke={colors[s.key]}
                strokeWidth={2}
                strokeLinejoin="round"
                strokeLinecap="round"
                dot={false}
                activeDot={{ r: 4, stroke: INK.surface, strokeWidth: 2 }}
                isAnimationActive={false}
              />
            ),
          )}
        </LineChart>
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
          {series.map((s) => (
            <th key={s.key} scope="col" className="py-1 pl-3 text-right font-medium">
              {s.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody className="divide-y divide-slate-100">
        {data.map((d) => (
          <tr key={String(d.month)}>
            <th scope="row" className="py-1 pr-3 text-left font-normal">
              {fmt.month(String(d.month))}
            </th>
            {series.map((s) => (
              <td key={s.key} className={`num py-1 pl-3 ${Number(d[s.key]) < 0 ? 'text-red-700' : ''}`}>
                {fmt.money(Number(d[s.key] ?? 0))}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )

  return <ChartCard title={title} subtitle={subtitle} legend={legend} chart={chart} table={table} />
}
