import { useState, type ReactNode } from 'react'

export interface LegendItem {
  key: string
  label: string
  color: string
  shape: 'line' | 'rect'
  /** When set, the legend item toggles the series. */
  hidden?: boolean
  onToggle?: () => void
}

interface ChartCardProps {
  title: string
  subtitle?: ReactNode
  legend?: LegendItem[]
  chart: ReactNode
  table: ReactNode
  actions?: ReactNode
}

/** A chart with its legend and a table-view twin, so no value is reachable only by hovering. */
export function ChartCard({ title, subtitle, legend, chart, table, actions }: ChartCardProps) {
  const [view, setView] = useState<'chart' | 'table'>('chart')
  return (
    <section className="card p-4 sm:p-5" aria-label={title}>
      <header className="mb-3 flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h2 className="text-base font-semibold">{title}</h2>
          {subtitle && <div className="mt-0.5 text-sm text-slate-600">{subtitle}</div>}
        </div>
        <div className="flex items-center gap-2">
          {actions}
          <div role="group" aria-label="View" className="inline-flex rounded-md border border-slate-300 p-0.5">
            {(['chart', 'table'] as const).map((v) => (
              <button
                key={v}
                type="button"
                aria-pressed={view === v}
                className={`rounded px-2 py-0.5 text-xs capitalize ${view === v ? 'bg-slate-800 text-white' : 'text-slate-600 hover:bg-slate-100'}`}
                onClick={() => setView(v)}
              >
                {v}
              </button>
            ))}
          </div>
        </div>
      </header>
      {legend && legend.length > 1 && view === 'chart' && (
        <ul className="mb-2 flex flex-wrap gap-x-4 gap-y-1 text-sm text-slate-700">
          {legend.map((item) => {
            const key =
              item.shape === 'line' ? (
                <span className="inline-block h-0.5 w-4 rounded" style={{ background: item.color }} />
              ) : (
                <span className="inline-block size-3 rounded-sm" style={{ background: item.color }} />
              )
            return (
              <li key={item.key}>
                {item.onToggle ? (
                  <button
                    type="button"
                    aria-pressed={!item.hidden}
                    onClick={item.onToggle}
                    className={`inline-flex items-center gap-1.5 rounded px-1 hover:bg-slate-100 ${item.hidden ? 'opacity-40' : ''}`}
                  >
                    {key}
                    {item.label}
                  </button>
                ) : (
                  <span className="inline-flex items-center gap-1.5 px-1">
                    {key}
                    {item.label}
                  </span>
                )}
              </li>
            )
          })}
        </ul>
      )}
      {view === 'chart' ? chart : <div className="max-h-[28rem] overflow-auto">{table}</div>}
    </section>
  )
}
