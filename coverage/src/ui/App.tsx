import { useMemo } from 'react'
import { EntityEditor } from './editors/EntityEditor'
import { assetsConfig, debtsConfig, eventsConfig, incomesConfig, obligationsConfig } from './editors/configs'
import type { EditorContext } from './editors/types'
import { useDataset, useFormatter } from './hooks/useDataset'
import { AssumptionsPage } from './pages/AssumptionsPage'
import { DashboardPage } from './pages/DashboardPage'
import { Next12Page } from './pages/Next12Page'
import { ProjectionPage } from './pages/ProjectionPage'
import { DataPage } from './pages/DataPage'
import { Placeholder } from './pages/Placeholder'
import { NAV, href, useRoute, type RouteId } from './routes'

function Page({ route, ctx }: { route: RouteId; ctx: EditorContext }) {
  switch (route) {
    case 'dashboard':
      return <DashboardPage ctx={ctx} />
    case 'projection':
      return <ProjectionPage ctx={ctx} />
    case 'next12':
      return <Next12Page ctx={ctx} />
    case 'assets':
      return <EntityEditor config={assetsConfig} ctx={ctx} />
    case 'debts':
      return <EntityEditor config={debtsConfig} ctx={ctx} />
    case 'obligations':
      return <EntityEditor config={obligationsConfig} ctx={ctx} />
    case 'incomes':
      return <EntityEditor config={incomesConfig} ctx={ctx} />
    case 'events':
      return <EntityEditor config={eventsConfig} ctx={ctx} />
    case 'assumptions':
      return <AssumptionsPage ctx={ctx} />
    case 'data':
      return <DataPage ctx={ctx} />
    default: {
      const item = NAV.flatMap((g) => g.items).find((i) => i.id === route)!
      return <Placeholder item={item} ctx={ctx} />
    }
  }
}

export function App() {
  const route = useRoute()
  const dataset = useDataset()
  const fmt = useFormatter(dataset)
  const ctx = useMemo<EditorContext | null>(() => (dataset ? { dataset, fmt } : null), [dataset, fmt])

  return (
    <div className="min-h-screen lg:flex">
      <aside className="border-b border-slate-200 bg-white lg:sticky lg:top-0 lg:h-screen lg:w-60 lg:shrink-0 lg:border-r lg:border-b-0">
        <div className="flex items-center justify-between px-4 py-3 lg:block lg:py-5">
          <a href={href('dashboard')} className="block">
            <span className="text-base font-semibold text-brand-800">Coverage</span>
            <span className="block text-xs text-slate-500">Obligations against assets and income</span>
          </a>
        </div>
        <nav aria-label="Main" className="flex gap-4 overflow-x-auto px-4 pb-3 lg:block lg:space-y-5 lg:overflow-visible lg:pb-0">
          {NAV.map((group) => (
            <div key={group.heading} className="shrink-0">
              <h2 className="mb-1 hidden text-xs font-medium tracking-wide text-slate-400 uppercase lg:block">{group.heading}</h2>
              <ul className="flex gap-1 lg:block lg:space-y-0.5">
                {group.items.map((item) => {
                  const active = item.id === route
                  return (
                    <li key={item.id}>
                      <a
                        href={href(item.id)}
                        aria-current={active ? 'page' : undefined}
                        className={`block rounded-md px-2 py-1.5 text-sm whitespace-nowrap ${
                          active ? 'bg-brand-50 font-medium text-brand-800' : 'text-slate-700 hover:bg-slate-100'
                        } ${item.phase ? 'text-slate-400' : ''}`}
                      >
                        {item.label}
                      </a>
                    </li>
                  )
                })}
              </ul>
            </div>
          ))}
        </nav>
        <p className="hidden px-4 pt-6 text-xs text-slate-400 lg:block">Stored only in this browser. No network access.</p>
      </aside>

      <main className="min-w-0 flex-1">
        {ctx && (
          <div className="border-b border-slate-200 bg-white px-4 py-2 text-xs text-slate-500 sm:px-8">
            As of {ctx.fmt.month(ctx.dataset.settings.asOfMonth)} · {ctx.dataset.settings.horizonYears}-year horizon · {ctx.dataset.settings.currency} ·{' '}
            {ctx.dataset.settings.display === 'real' ? 'real terms' : 'nominal terms'}
          </div>
        )}
        <div className="px-4 py-6 sm:px-8">{ctx ? <Page route={route} ctx={ctx} /> : <p className="text-sm text-slate-500">Loading…</p>}</div>
      </main>
    </div>
  )
}
