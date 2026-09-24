import { useMemo, useState } from 'react'
import { saveSettings } from '../../db/repo'
import { addMonths } from '../../engine/month'
import { CURRENCIES, settingsSchema, type Settings } from '../../schema/settings'
import { Notice } from '../components/Notice'
import { draftToRecord, isVisible, recordToDraft, type Draft, type FieldDef } from '../editors/fields'
import { FieldInput } from '../editors/FieldInput'
import type { EditorContext } from '../editors/types'

function settingsFields(ctx: EditorContext): FieldDef[] {
  const sweepOptions = ctx.dataset.assets
    .filter((a) => a.tier === 'T1' || a.tier === 'T2')
    .map((a) => ({ value: a.id, label: `${a.name} (${a.tier})` }))
  return [
    {
      key: 'asOfMonth',
      label: 'As-of month',
      kind: 'month',
      help: 'The first projected month. Balances you enter are as at the start of it. Use the monthly check-in to move it forward: it also applies annual increases that fell due in between, which editing it here does not.',
    },
    { key: 'horizonYears', label: 'Projection horizon', kind: 'integer', suffix: 'years', help: '1 to 30 years.' },
    { key: 'cpiBps', label: 'CPI', kind: 'percent', suffix: '%', allowNegative: true, help: 'Used to show values in real terms.' },
    { key: 'primeBps', label: 'Prime rate', kind: 'percent', suffix: '%', help: 'Variable-rate debt is charged at prime plus its margin.' },
    {
      key: 'display',
      label: 'Show amounts in',
      kind: 'select',
      options: [
        { value: 'nominal', label: 'Nominal terms (future rands)' },
        { value: 'real', label: "Real terms (today's rands, deflated by CPI)" },
      ],
    },
    { key: 'currency', label: 'Currency', kind: 'select', options: CURRENCIES.map((c) => ({ value: c, label: c })) },
    {
      key: 'sweepAssetId',
      label: 'Sweep surpluses into',
      kind: 'select',
      emptyAsNull: true,
      options: [{ value: '', label: 'Automatic: the first T1 asset' }, ...sweepOptions],
      help: 'A T1 or T2 asset that receives any monthly surplus.',
      wide: true,
    },
    {
      key: 'includeT3InDrawdown',
      label: 'Draw on accessible retirement savings after T1 and T2 run out',
      kind: 'checkbox',
      help: 'Off by default. Uses the accessible T3 amount, net of its haircut, before recording a shortfall.',
      wide: true,
    },
    {
      key: 'overdraftBps',
      label: 'Interest on a carried deficit',
      kind: 'percent',
      suffix: '%',
      help: 'Charged monthly on any shortfall carried forward. 0 treats it as interest-free.',
    },
  ]
}

export function AssumptionsPage({ ctx }: { ctx: EditorContext }) {
  const settings = ctx.dataset.settings
  const fields = useMemo(() => settingsFields(ctx), [ctx])
  const [draft, setDraft] = useState<Draft>(() => recordToDraft(fields, settings as unknown as Record<string, unknown>))
  const [status, setStatus] = useState<{ tone: 'info' | 'error'; text: string } | null>(null)
  const [showErrors, setShowErrors] = useState(false)

  const result = draftToRecord<Settings>(fields, draft, settings as unknown as Record<string, unknown>, settingsSchema)
  const dirty = JSON.stringify(recordToDraft(fields, settings as unknown as Record<string, unknown>)) !== JSON.stringify(draft)

  const save = async (e: React.FormEvent) => {
    e.preventDefault()
    setShowErrors(true)
    if (!result.value) return
    try {
      await saveSettings(result.value)
      setStatus({ tone: 'info', text: 'Assumptions saved.' })
      setShowErrors(false)
    } catch (err) {
      setStatus({ tone: 'error', text: err instanceof Error ? err.message : String(err) })
    }
  }

  const horizonEnd = result.value ? addMonths(result.value.asOfMonth, result.value.horizonYears * 12 - 1) : null

  return (
    <section className="max-w-3xl space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Assumptions</h1>
        <p className="mt-1 text-sm text-slate-600">Global settings for every projection and scenario.</p>
      </header>
      <form noValidate onSubmit={save} className="card space-y-4 p-5">
        <div className="grid gap-4 sm:grid-cols-2">
          {fields
            .filter((f) => isVisible(f, draft))
            .map((f) => (
              <FieldInput
                key={f.key}
                field={f}
                draft={draft}
                value={draft[f.key] ?? ''}
                error={showErrors ? result.fieldErrors[f.key] : undefined}
                onChange={(v) => {
                  setStatus(null)
                  setDraft((d) => ({ ...d, [f.key]: v }))
                }}
              />
            ))}
        </div>
        {horizonEnd && <p className="text-sm text-slate-600">The projection runs to {ctx.fmt.month(horizonEnd)}.</p>}
        {status && <Notice tone={status.tone}>{status.text}</Notice>}
        <div className="flex justify-end gap-2">
          <button
            type="button"
            className="btn"
            disabled={!dirty}
            onClick={() => {
              setDraft(recordToDraft(fields, settings as unknown as Record<string, unknown>))
              setShowErrors(false)
            }}
          >
            Discard changes
          </button>
          <button type="submit" className="btn btn-primary" disabled={!dirty}>
            Save assumptions
          </button>
        </div>
      </form>
    </section>
  )
}
