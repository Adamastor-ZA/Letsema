import { Fragment, useState } from 'react'
import type { FlowItem, MonthRow } from '../../engine/types'
import { liquidBalance } from '../../engine/metrics'
import { DisplayToggle } from '../components/DisplayToggle'
import { Badge, Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'
import { useModel } from '../hooks/useModel'
import { GettingStarted } from './DashboardPage'

const KIND_LABEL: Record<FlowItem['kind'], string> = { income: 'Income', obligation: 'Obligation', debt: 'Debt payment', event: 'One-off' }

function ItemList({ items, fmt, d }: { items: FlowItem[]; fmt: EditorContext['fmt']; d: (c: number) => number }) {
  if (items.length === 0) return <p className="text-slate-400">Nothing</p>
  return (
    <ul className="space-y-0.5">
      {[...items]
        .sort((a, b) => b.amountCents - a.amountCents)
        .map((i) => (
          <li key={`${i.kind}-${i.id}`} className="flex justify-between gap-4">
            <span>
              {i.name}{' '}
              <span className="text-xs text-slate-500">
                {KIND_LABEL[i.kind]}
                {i.confidence === 'variable' ? ', variable' : ''}
              </span>
            </span>
            <span className="tabular-nums">{fmt.money(d(i.amountCents))}</span>
          </li>
        ))}
    </ul>
  )
}

function Status({ r, fmt, d }: { r: MonthRow; fmt: EditorContext['fmt']; d: (c: number) => number }) {
  if (r.newDeficitCents > 0 || r.shortfall) return <Badge tone="red">Shortfall {fmt.money(d(r.deficitCents))}</Badge>
  if (r.drawnCents > 0) return <Badge tone="amber">Draws {fmt.money(d(r.drawnCents))}</Badge>
  return <Badge tone="green">Covered</Badge>
}

export function Next12Page({ ctx }: { ctx: EditorContext }) {
  const model = useModel(ctx.dataset)
  const [open, setOpen] = useState<Set<string>>(new Set())
  const { settings } = ctx.dataset
  const fmt = ctx.fmt
  if ('error' in model) return <Notice tone="error">The projection could not run: {model.error}</Notice>

  const rows = model.evaluation.result.rows.slice(0, 12)
  const toggle = (month: string) =>
    setOpen((s) => {
      const next = new Set(s)
      if (next.has(month)) next.delete(month)
      else next.add(month)
      return next
    })

  const inOf = (r: MonthRow) => r.incomeCents + r.oneOffInCents
  const outOf = (r: MonthRow) => r.obligationsCents + r.debtPaymentsCents + r.oneOffOutCents
  const total = (f: (r: MonthRow) => number) => rows.reduce((s, r, i) => s + model.display(f(r), i + 1), 0)
  const deficitMonths = rows.filter((r) => r.netFlowCents < 0).length

  return (
    <section className="space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold">Next 12 months</h1>
          <p className="mt-1 text-sm text-slate-600">What falls due each month against what comes in. Select a month to see every item.</p>
        </div>
        <DisplayToggle settings={settings} />
      </header>
      {model.isEmpty ? (
        <GettingStarted />
      ) : (
        <>
          <p className="text-sm text-slate-700">
            Over the next 12 months {fmt.money(total(inOf))} comes in and {fmt.money(total(outOf))} goes out.{' '}
            {deficitMonths === 0
              ? 'Every month is covered by that month’s income.'
              : `${deficitMonths} ${deficitMonths === 1 ? 'month needs' : 'months need'} savings to cover the gap.`}
          </p>
          <div className="card overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-slate-200 bg-slate-50 text-xs font-medium tracking-wide text-slate-500 uppercase">
                <tr>
                  <th scope="col" className="px-3 py-2 text-left">
                    Month
                  </th>
                  <th scope="col" className="px-3 py-2 text-right">
                    Committed income
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right md:table-cell">
                    Variable income
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right md:table-cell">
                    Obligations
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right md:table-cell">
                    Debt payments
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right lg:table-cell">
                    One-offs
                  </th>
                  <th scope="col" className="px-3 py-2 text-right">
                    Net
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right sm:table-cell">
                    Liquid balance
                  </th>
                  <th scope="col" className="px-3 py-2 text-left">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {rows.map((r, i) => {
                  const d = (c: number) => model.display(c, i + 1)
                  const isOpen = open.has(r.month)
                  const oneOff = r.oneOffInCents - r.oneOffOutCents
                  return (
                    <Fragment key={r.month}>
                      <tr className="hover:bg-slate-50/60">
                        <th scope="row" className="px-3 py-2 text-left font-medium">
                          <button
                            type="button"
                            className="inline-flex items-center gap-1.5 whitespace-nowrap hover:text-brand-700"
                            aria-expanded={isOpen}
                            aria-controls={`detail-${r.month}`}
                            onClick={() => toggle(r.month)}
                          >
                            <span aria-hidden="true" className="text-slate-400">
                              {isOpen ? '▾' : '▸'}
                            </span>
                            {fmt.month(r.month)}
                          </button>
                        </th>
                        <td className="num px-3 py-2">{fmt.money(d(r.committedIncomeCents))}</td>
                        <td className="num hidden px-3 py-2 md:table-cell">{fmt.money(d(r.variableIncomeCents))}</td>
                        <td className="num hidden px-3 py-2 md:table-cell">{fmt.money(d(r.obligationsCents))}</td>
                        <td className="num hidden px-3 py-2 md:table-cell">{fmt.money(d(r.debtPaymentsCents))}</td>
                        <td className="num hidden px-3 py-2 lg:table-cell">{oneOff === 0 ? '–' : fmt.money(d(oneOff))}</td>
                        <td className={`num px-3 py-2 font-medium ${r.netFlowCents < 0 ? 'text-red-700' : ''}`}>{fmt.money(d(r.netFlowCents))}</td>
                        <td className="num hidden px-3 py-2 sm:table-cell">{fmt.money(d(liquidBalance(r)))}</td>
                        <td className="px-3 py-2">
                          <Status r={r} fmt={fmt} d={d} />
                        </td>
                      </tr>
                      {isOpen && (
                        <tr id={`detail-${r.month}`} className="bg-slate-50/70">
                          <td colSpan={9} className="px-3 py-3">
                            <div className="grid gap-4 text-sm md:grid-cols-2">
                              <div>
                                <h3 className="mb-1 text-xs font-medium tracking-wide text-slate-500 uppercase">
                                  Coming in · {fmt.money(d(inOf(r)))}
                                </h3>
                                <ItemList items={(r.items ?? []).filter((x) => x.direction === 'in')} fmt={fmt} d={d} />
                              </div>
                              <div>
                                <h3 className="mb-1 text-xs font-medium tracking-wide text-slate-500 uppercase">
                                  Going out · {fmt.money(d(outOf(r)))}
                                </h3>
                                <ItemList items={(r.items ?? []).filter((x) => x.direction === 'out')} fmt={fmt} d={d} />
                              </div>
                            </div>
                            {r.debtsRetired.length > 0 && (
                              <p className="mt-2 text-xs text-slate-600">
                                Paid off this month:{' '}
                                {r.debtsRetired.map((id) => ctx.dataset.debts.find((x) => x.id === id)?.name ?? id).join(', ')}
                              </p>
                            )}
                          </td>
                        </tr>
                      )}
                    </Fragment>
                  )
                })}
              </tbody>
              <tfoot className="border-t border-slate-200 bg-slate-50 font-medium">
                <tr>
                  <th scope="row" className="px-3 py-2 text-left">
                    Total
                  </th>
                  <td className="num px-3 py-2">{fmt.money(total((r) => r.committedIncomeCents))}</td>
                  <td className="num hidden px-3 py-2 md:table-cell">{fmt.money(total((r) => r.variableIncomeCents))}</td>
                  <td className="num hidden px-3 py-2 md:table-cell">{fmt.money(total((r) => r.obligationsCents))}</td>
                  <td className="num hidden px-3 py-2 md:table-cell">{fmt.money(total((r) => r.debtPaymentsCents))}</td>
                  <td className="num hidden px-3 py-2 lg:table-cell">{fmt.money(total((r) => r.oneOffInCents - r.oneOffOutCents))}</td>
                  <td className="num px-3 py-2">{fmt.money(total((r) => r.netFlowCents))}</td>
                  <td className="hidden sm:table-cell" />
                  <td />
                </tr>
              </tfoot>
            </table>
          </div>
          <p className="text-xs text-slate-500">
            Net is income less obligations, debt payments and one-offs. A negative month draws on T1, then T2 after haircut; the status shows the cash
            raised, or the deficit carried if savings run out.
          </p>
        </>
      )}
    </section>
  )
}
