import { useMemo, useState } from 'react'
import { planCheckIn, projectedAt, trackAgainstBaseline, type TrackedMetric } from '../../db/checkin'
import { currentYearMonth, deleteSnapshot, saveCheckIn } from '../../db/repo'
import { isYearMonth, toIndex } from '../../engine/month'
import type { Dataset } from '../../schema/dataset'
import { TrackingChart } from '../charts/TrackingChart'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Badge, Notice } from '../components/Notice'
import { TIER_LABELS } from '../editors/configs'
import type { EditorContext } from '../editors/types'
import { formatMoneyInput, parseMoney } from '../lib/parse'
import { href } from '../routes'

const METRICS: { key: TrackedMetric; label: string }[] = [
  { key: 'liquidCents', label: 'Liquid balance' },
  { key: 'netWorthCents', label: 'Net worth' },
  { key: 'debtCents', label: 'Debt' },
]

function defaultMonth(asOf: string): string {
  const now = currentYearMonth()
  return toIndex(now) > toIndex(asOf) ? now : asOf
}

function initialValues(d: Dataset): Record<string, string> {
  return Object.fromEntries([...d.assets.map((a) => [a.id, formatMoneyInput(a.valueCents)]), ...d.debts.map((x) => [x.id, formatMoneyInput(x.balanceCents)])])
}

function CheckInForm({ ctx, onSaved }: { ctx: EditorContext; onSaved: (message: string) => void }) {
  const { dataset: d, fmt } = ctx
  const asOf = d.settings.asOfMonth
  const [month, setMonth] = useState(() => defaultMonth(asOf))
  const [values, setValues] = useState<Record<string, string>>(() => initialValues(d))
  const [note, setNote] = useState('')
  const [confirming, setConfirming] = useState(false)
  const [showErrors, setShowErrors] = useState(false)

  const monthError = !isYearMonth(month) ? 'Enter a month as YYYY-MM' : toIndex(month) < toIndex(asOf) ? `Must be ${fmt.month(asOf)} or later` : null
  const projected = useMemo(() => (monthError ? null : projectedAt(d, month)), [d, month, monthError])

  const parsed: Record<string, number> = {}
  const errors: Record<string, string> = {}
  for (const [id, text] of Object.entries(values)) {
    const r = parseMoney(text)
    if (r.ok) parsed[id] = r.value
    else errors[id] = r.error
  }
  const valid = !monthError && Object.keys(errors).length === 0
  const assetValues = Object.fromEntries(d.assets.map((a) => [a.id, parsed[a.id] ?? a.valueCents]))
  const debtBalances = Object.fromEntries(d.debts.map((x) => [x.id, parsed[x.id] ?? x.balanceCents]))
  const plan = useMemo(() => {
    if (monthError) return null
    const read = (id: string) => {
      const r = parseMoney(values[id] ?? '')
      return r.ok ? r.value : null
    }
    const av: Record<string, number> = {}
    const db: Record<string, number> = {}
    for (const a of d.assets) {
      const v = read(a.id)
      if (v === null) return null
      av[a.id] = v
    }
    for (const x of d.debts) {
      const v = read(x.id)
      if (v === null) return null
      db[x.id] = v
    }
    try {
      return planCheckIn(d, { month, assetValues: av, debtBalances: db, takenAt: new Date().toISOString() })
    } catch {
      return null
    }
  }, [d, month, values, monthError])
  const replacing = d.snapshots.some((s) => s.month === month)

  const fillProjected = () => {
    if (!projected) return
    setValues((v) => {
      const next = { ...v }
      for (const a of d.assets) if (projected.assetValues[a.id] !== undefined) next[a.id] = formatMoneyInput(projected.assetValues[a.id]!)
      for (const x of d.debts) if (projected.debtBalances[x.id] !== undefined) next[x.id] = formatMoneyInput(projected.debtBalances[x.id]!)
      return next
    })
  }

  const row = (id: string, name: string, last: number, proj: number | undefined, tier?: string) => {
    const actual = parsed[id]
    const diff = actual !== undefined && proj !== undefined ? actual - proj : null
    return (
      <tr key={id}>
        <th scope="row" className="px-3 py-1.5 text-left font-normal">
          <label htmlFor={`checkin-${id}`}>{name}</label>
          {tier && <span className="ml-1 text-xs text-slate-500">{tier}</span>}
        </th>
        <td className="num hidden px-3 py-1.5 text-slate-600 sm:table-cell">{fmt.money(last)}</td>
        <td className="num hidden px-3 py-1.5 text-slate-600 md:table-cell">{proj === undefined ? '–' : fmt.money(proj)}</td>
        <td className="px-3 py-1.5">
          <input
            id={`checkin-${id}`}
            className="input w-36 text-right tabular-nums"
            inputMode="decimal"
            autoComplete="off"
            value={values[id] ?? ''}
            aria-invalid={showErrors && errors[id] ? true : undefined}
            onChange={(e) => setValues((v) => ({ ...v, [id]: e.target.value }))}
          />
          {showErrors && errors[id] && <p className="mt-0.5 text-xs text-red-700">{errors[id]}</p>}
        </td>
        <td className="num hidden px-3 py-1.5 text-xs text-slate-600 md:table-cell">{diff === null ? '' : `${diff > 0 ? '+' : ''}${fmt.money(diff)}`}</td>
      </tr>
    )
  }

  const tableHead = (label: string) => (
    <thead className="border-b border-slate-200 bg-slate-50 text-xs font-medium text-slate-500">
      <tr>
        <th scope="col" className="px-3 py-2 text-left">
          {label}
        </th>
        <th scope="col" className="hidden px-3 py-2 text-right sm:table-cell">
          Last recorded
        </th>
        <th scope="col" className="hidden px-3 py-2 text-right md:table-cell">
          Projected
        </th>
        <th scope="col" className="px-3 py-2 text-left">
          Actual at start of {monthError ? 'month' : fmt.month(month)}
        </th>
        <th scope="col" className="hidden px-3 py-2 text-right md:table-cell">
          Against projection
        </th>
      </tr>
    </thead>
  )

  const actual = plan?.snapshot.actual
  const compare = (label: string, a: number | undefined, p: number | undefined) => (
    <div className="card px-3 py-2">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="text-lg font-semibold">{a === undefined ? '–' : fmt.money(a)}</div>
      {a !== undefined && p !== undefined && (
        <div className="text-xs text-slate-600">
          {fmt.money(p)} projected · {a - p >= 0 ? '+' : ''}
          {fmt.money(a - p)}
        </div>
      )}
    </div>
  )

  return (
    <form
      noValidate
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault()
        setShowErrors(true)
        if (valid && plan) setConfirming(true)
      }}
    >
      <div className="card flex flex-wrap items-end gap-4 p-4">
        <div>
          <label htmlFor="checkin-month" className="mb-1 block text-sm font-medium">
            Check-in month
          </label>
          <input id="checkin-month" type="month" className="input w-44" value={month} min={asOf} onChange={(e) => setMonth(e.target.value)} aria-invalid={monthError ? true : undefined} />
          {monthError && <p className="mt-1 text-xs text-red-700">{monthError}</p>}
        </div>
        <p className="max-w-xl text-sm text-slate-600">
          Enter balances as at the start of the month. Saving moves the model to that month and records a snapshot to compare against later.
          {replacing && ' A check-in for this month exists and will be replaced.'}
        </p>
        <button type="button" className="btn ml-auto" onClick={fillProjected} disabled={!projected}>
          Fill with projected values
        </button>
      </div>

      {d.assets.length > 0 && (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            {tableHead('Asset')}
            <tbody className="divide-y divide-slate-100">
              {d.assets.map((a) => row(a.id, a.name, a.valueCents, projected?.assetValues[a.id], TIER_LABELS[a.tier].split(' ')[0]))}
            </tbody>
          </table>
        </div>
      )}
      {d.debts.length > 0 && (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            {tableHead('Debt')}
            <tbody className="divide-y divide-slate-100">{d.debts.map((x) => row(x.id, x.name, x.balanceCents, projected?.debtBalances[x.id]))}</tbody>
          </table>
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-3">
        {compare('Liquid balance', actual?.liquidCents, projected?.liquidCents)}
        {compare('Net worth', actual?.netWorthCents, projected?.netWorthCents)}
        {compare('Debt', actual?.debtCents, projected?.debtCents)}
      </div>

      {plan && plan.rolled.length > 0 && (
        <Notice>
          <p className="font-medium">Annual increases since {fmt.month(asOf)} will be applied:</p>
          <ul className="mt-1 list-disc pl-5">
            {plan.rolled.map((r) => (
              <li key={r.id}>
                {r.name}: {fmt.money(r.fromCents)} to {fmt.money(r.toCents)}
              </li>
            ))}
          </ul>
        </Notice>
      )}

      <div>
        <label htmlFor="checkin-note" className="mb-1 block text-sm font-medium">
          Note <span className="font-normal text-slate-500">(optional)</span>
        </label>
        <textarea id="checkin-note" className="input" rows={2} maxLength={2000} value={note} onChange={(e) => setNote(e.target.value)} />
      </div>

      {showErrors && !valid && <Notice tone="error">Fix the highlighted values.</Notice>}
      <div className="flex justify-end">
        <button type="submit" className="btn btn-primary">
          Review and save check-in
        </button>
      </div>

      {confirming && plan && (
        <ConfirmDialog
          title={`Save check-in for ${fmt.month(month)}?`}
          confirmLabel="Save check-in"
          danger={false}
          onCancel={() => setConfirming(false)}
          onConfirm={async () => {
            await saveCheckIn({ month, assetValues, debtBalances, note, takenAt: new Date().toISOString() })
            setConfirming(false)
            onSaved(`Checked in for ${fmt.month(month)}.`)
          }}
        >
          <ul className="list-disc space-y-1 pl-5">
            <li>
              Asset and debt balances are updated{month !== asOf ? `, and the model moves from ${fmt.month(asOf)} to ${fmt.month(month)}` : ''}.
            </li>
            {plan.rolled.length > 0 && <li>{plan.rolled.length} obligation and income amounts pick up the increases that fell due.</li>}
            {replacing && <li>The existing check-in for {fmt.month(month)} is replaced.</li>}
          </ul>
          <p>
            Export a backup from the <a className="text-brand-700 underline" href={href('data')}>Data</a> page first if you may want to undo this.
          </p>
        </ConfirmDialog>
      )}
    </form>
  )
}

export function CheckInPage({ ctx }: { ctx: EditorContext }) {
  const { dataset: d, fmt } = ctx
  const [saved, setSaved] = useState<{ message: string; key: number } | null>(null)
  const [metric, setMetric] = useState<TrackedMetric>('liquidCents')
  const [baselineId, setBaselineId] = useState<string | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)
  const snapshots = d.snapshots
  const baseline = snapshots.find((s) => s.id === baselineId) ?? snapshots[0]
  const points = baseline ? trackAgainstBaseline(snapshots, baseline.id, metric) : []
  const last = snapshots[snapshots.length - 1]
  const empty = d.assets.length + d.debts.length === 0

  return (
    <section className="space-y-5">
      <header>
        <h1 className="text-xl font-semibold">Monthly check-in</h1>
        <p className="mt-1 text-sm text-slate-600">
          Model as of {fmt.month(d.settings.asOfMonth)}. {last ? `Last check-in: ${fmt.month(last.month)}.` : 'No check-ins yet.'}
        </p>
      </header>

      {saved && <Notice>{saved.message}</Notice>}

      {empty ? (
        <Notice>
          Add your <a className="text-brand-700 underline" href={href('assets')}>assets</a> and{' '}
          <a className="text-brand-700 underline" href={href('debts')}>debts</a> first.
        </Notice>
      ) : (
        <CheckInForm key={`${d.settings.asOfMonth}-${saved?.key ?? 0}`} ctx={ctx} onSaved={(message) => setSaved({ message, key: Date.now() })} />
      )}

      <h2 className="pt-2 text-base font-semibold">Actual against projected</h2>
      {baseline ? (
        <TrackingChart
          points={points}
          fmt={fmt}
          metricLabel={METRICS.find((m) => m.key === metric)!.label}
          baselineMonth={baseline.month}
          actions={
            <>
              <select aria-label="Metric" className="input w-auto py-0.5 text-xs" value={metric} onChange={(e) => setMetric(e.target.value as TrackedMetric)}>
                {METRICS.map((m) => (
                  <option key={m.key} value={m.key}>
                    {m.label}
                  </option>
                ))}
              </select>
              <select aria-label="Projection from" className="input w-auto py-0.5 text-xs" value={baseline.id} onChange={(e) => setBaselineId(e.target.value)}>
                {snapshots.map((s) => (
                  <option key={s.id} value={s.id}>
                    Projected {fmt.month(s.month)}
                  </option>
                ))}
              </select>
            </>
          }
        />
      ) : (
        <p className="text-sm text-slate-600">Your first check-in sets the baseline. Each later check-in is plotted against what was projected.</p>
      )}

      {snapshots.length > 0 && (
        <>
          <h2 className="pt-2 text-base font-semibold">History</h2>
          <div className="card overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-slate-200 bg-slate-50 text-xs font-medium text-slate-500">
                <tr>
                  <th scope="col" className="px-3 py-2 text-left">
                    Month
                  </th>
                  <th scope="col" className="px-3 py-2 text-right">
                    Liquid balance
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right sm:table-cell">
                    Net worth
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-right sm:table-cell">
                    Debt
                  </th>
                  <th scope="col" className="hidden px-3 py-2 text-left md:table-cell">
                    Note
                  </th>
                  <th scope="col" className="px-3 py-2">
                    <span className="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {[...snapshots].reverse().map((s) => (
                  <tr key={s.id}>
                    <th scope="row" className="px-3 py-1.5 text-left font-normal whitespace-nowrap">
                      {fmt.month(s.month)} {s.id === baseline?.id && <Badge tone="brand">Baseline</Badge>}
                    </th>
                    <td className="num px-3 py-1.5">{fmt.money(s.actual.liquidCents)}</td>
                    <td className="num hidden px-3 py-1.5 sm:table-cell">{fmt.money(s.actual.netWorthCents)}</td>
                    <td className="num hidden px-3 py-1.5 sm:table-cell">{fmt.money(s.actual.debtCents)}</td>
                    <td className="hidden px-3 py-1.5 text-slate-600 md:table-cell">{s.note}</td>
                    <td className="px-3 py-1.5 text-right">
                      <button type="button" className="btn btn-ghost btn-sm text-red-700" aria-label={`Delete check-in for ${fmt.month(s.month)}`} onClick={() => setDeleting(s.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {deleting && (
        <ConfirmDialog
          title="Delete this check-in?"
          confirmLabel="Delete"
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            await deleteSnapshot(deleting)
            setDeleting(null)
          }}
        >
          <p>The snapshot is removed from the history and the chart. Current balances and the as-of month are not changed.</p>
        </ConfirmDialog>
      )}
    </section>
  )
}
