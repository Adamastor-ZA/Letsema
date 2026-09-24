import { useId, useState } from 'react'
import { isYearMonth } from '../../engine/month'
import { PRESET_IDS, PRESETS, type Overrides, type PresetId } from '../../engine/scenarios'
import type { OneOffEvent } from '../../engine/types'
import { newId, saveScenario } from '../../db/repo'
import type { Dataset, ScenarioRecord } from '../../schema/dataset'
import { Modal } from '../components/Modal'
import { Notice } from '../components/Notice'
import { changeBpsToFactor, factorToChangeBps } from '../lib/describe'
import { formatMoneyInput, formatPercentInput, parseMoney, parsePercent } from '../lib/parse'
import { scenarioColor } from '../charts/theme'

type AdjustKey = 'prime' | 'variableIncome' | 'committedIncome' | 'incomeGrowth' | 'escalation' | 'investmentGrowth' | 'haircut'

const ADJUSTMENTS: { key: AdjustKey; label: string; help: string; unit: string }[] = [
  { key: 'prime', label: 'Prime rate', help: 'Moves variable-rate debt; instalments are recalculated over the remaining term.', unit: 'points' },
  { key: 'variableIncome', label: 'Variable income', help: 'Change in every variable income stream. −100 removes it.', unit: '%' },
  { key: 'committedIncome', label: 'Committed income', help: 'Change in every committed income stream. −100 removes it.', unit: '%' },
  { key: 'incomeGrowth', label: 'Income growth', help: 'Added to each income stream’s annual increase.', unit: 'points a year' },
  { key: 'escalation', label: 'Obligation escalation', help: 'Added to each obligation’s annual escalation.', unit: 'points a year' },
  { key: 'investmentGrowth', label: 'Investment growth', help: 'Added to the growth rate of T2 and T3 assets.', unit: 'points a year' },
  { key: 'haircut', label: 'Haircuts', help: 'Added to T2 and T3 haircuts, kept between 0% and 100%.', unit: 'points' },
]

interface EventDraft {
  id: string
  name: string
  month: string
  amount: string
  direction: OneOffEvent['direction']
}

function toDraft(o: Overrides): Record<AdjustKey, string> {
  const pct = (bps: number | undefined) => (bps ? formatPercentInput(bps) : '')
  const factor = (f: number | undefined) => (f === undefined || f === 1 ? '' : formatPercentInput(factorToChangeBps(f)))
  return {
    prime: pct(o.primeDeltaBps),
    variableIncome: factor(o.variableIncomeFactor),
    committedIncome: factor(o.committedIncomeFactor),
    incomeGrowth: pct(o.incomeGrowthDeltaBps),
    escalation: pct(o.obligationEscalationDeltaBps),
    investmentGrowth: pct(o.investmentGrowthDeltaBps),
    haircut: pct(o.haircutDeltaBps),
  }
}

const KIND_LABELS = { assets: 'Assets', debts: 'Debts', obligations: 'Obligations', incomes: 'Income', events: 'One-off events' } as const

interface ScenarioFormProps {
  dataset: Dataset
  initial: ScenarioRecord
  isNew: boolean
  onClose: () => void
}

export function ScenarioForm({ dataset, initial, isNew, onClose }: ScenarioFormProps) {
  const uid = useId()
  const [name, setName] = useState(initial.name)
  const [presets, setPresets] = useState<PresetId[]>(initial.presets)
  const [adjust, setAdjust] = useState(() => toDraft(initial.custom))
  const [excluded, setExcluded] = useState<Set<string>>(() => new Set(initial.custom.excludedIds ?? []))
  const [events, setEvents] = useState<EventDraft[]>(() =>
    (initial.custom.extraEvents ?? []).map((e) => ({ id: e.id, name: e.name, month: e.month, amount: formatMoneyInput(e.amountCents), direction: e.direction })),
  )
  const [active, setActive] = useState(initial.active)
  const [showErrors, setShowErrors] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)

  // Validate on every render; errors are shown after the first save attempt.
  const errors: Record<string, string> = {}
  if (name.trim() === '') errors.name = 'Give the scenario a name'
  const custom: Overrides = {}
  const readBps = (key: AdjustKey, min: number, max: number): number | undefined => {
    const text = adjust[key].trim()
    if (text === '') return undefined
    const r = parsePercent(text, { allowNegative: true })
    if (!r.ok) {
      errors[key] = r.error
      return undefined
    }
    if (r.value < min || r.value > max) {
      errors[key] = `Between ${min / 100} and ${max / 100}`
      return undefined
    }
    return r.value === 0 ? undefined : r.value
  }
  const prime = readBps('prime', -5_000, 5_000)
  const variableIncome = readBps('variableIncome', -10_000, 90_000)
  const committedIncome = readBps('committedIncome', -10_000, 90_000)
  const incomeGrowth = readBps('incomeGrowth', -5_000, 5_000)
  const escalation = readBps('escalation', -5_000, 5_000)
  const investmentGrowth = readBps('investmentGrowth', -5_000, 5_000)
  const haircut = readBps('haircut', -10_000, 10_000)
  if (prime !== undefined) custom.primeDeltaBps = prime
  if (variableIncome !== undefined) custom.variableIncomeFactor = changeBpsToFactor(variableIncome)
  if (committedIncome !== undefined) custom.committedIncomeFactor = changeBpsToFactor(committedIncome)
  if (incomeGrowth !== undefined) custom.incomeGrowthDeltaBps = incomeGrowth
  if (escalation !== undefined) custom.obligationEscalationDeltaBps = escalation
  if (investmentGrowth !== undefined) custom.investmentGrowthDeltaBps = investmentGrowth
  if (haircut !== undefined) custom.haircutDeltaBps = haircut
  // Keep only exclusions that still point at something.
  const liveIds = new Set((['assets', 'debts', 'obligations', 'incomes', 'events'] as const).flatMap((k) => dataset[k].map((x) => x.id)))
  const excludedIds = [...excluded].filter((id) => liveIds.has(id))
  if (excludedIds.length) custom.excludedIds = excludedIds
  const extraEvents: OneOffEvent[] = []
  events.forEach((e, i) => {
    const amount = parseMoney(e.amount)
    if (e.name.trim() === '') errors[`event-${i}-name`] = 'Name it'
    if (!isYearMonth(e.month)) errors[`event-${i}-month`] = 'YYYY-MM'
    if (!amount.ok) errors[`event-${i}-amount`] = amount.error
    else if (amount.value <= 0) errors[`event-${i}-amount`] = 'More than zero'
    if (amount.ok && amount.value > 0 && e.name.trim() && isYearMonth(e.month)) {
      extraEvents.push({ id: e.id, name: e.name.trim(), month: e.month, amountCents: amount.value, direction: e.direction })
    }
  })
  if (extraEvents.length) custom.extraEvents = extraEvents
  const nothing = presets.length === 0 && Object.keys(custom).length === 0
  const valid = Object.keys(errors).length === 0

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault()
    setShowErrors(true)
    if (!valid) return
    try {
      await saveScenario({ ...initial, name: name.trim(), presets: PRESET_IDS.filter((p) => presets.includes(p)), custom, active })
      onClose()
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : String(err))
    }
  }

  const err = (key: string) =>
    showErrors && errors[key] ? (
      <p id={`${uid}-${key}-error`} className="mt-1 text-xs font-medium text-red-700">
        {errors[key]}
      </p>
    ) : null
  const invalid = (key: string) => (showErrors && errors[key] ? { 'aria-invalid': true as const, 'aria-describedby': `${uid}-${key}-error` } : {})

  return (
    <Modal
      title={isNew ? 'New scenario' : `Edit ${initial.name}`}
      size="lg"
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" form="scenario-form" className="btn btn-primary">
            {isNew ? 'Create scenario' : 'Save scenario'}
          </button>
        </>
      }
    >
      <form id="scenario-form" noValidate onSubmit={submit} className="space-y-5 text-sm">
        <div className="grid gap-4 sm:grid-cols-[1fr_auto] sm:items-end">
          <div>
            <label htmlFor={`${uid}-name`} className="mb-1 block font-medium">
              Name
            </label>
            <div className="flex items-center gap-2">
              <span aria-hidden="true" className="inline-block h-0.5 w-5 shrink-0 rounded" style={{ background: scenarioColor(initial.slot) }} />
              <input id={`${uid}-name`} className="input" value={name} onChange={(e) => setName(e.target.value)} {...invalid('name')} />
            </div>
            {err('name')}
          </div>
          <label className="flex items-center gap-2 pb-1.5">
            <input type="checkbox" className="size-4 accent-brand-700" checked={active} onChange={(e) => setActive(e.target.checked)} />
            Compare against base
          </label>
        </div>

        <fieldset>
          <legend className="mb-1 font-medium">Presets</legend>
          <p className="mb-2 text-xs text-slate-500">Combine any of them. They stack with the custom adjustments below.</p>
          <div className="grid gap-2 sm:grid-cols-3">
            {PRESET_IDS.map((id) => (
              <label key={id} className="flex items-start gap-2 rounded-md border border-slate-200 p-2 hover:bg-slate-50">
                <input
                  type="checkbox"
                  className="mt-0.5 size-4 accent-brand-700"
                  checked={presets.includes(id)}
                  onChange={(e) => setPresets((p) => (e.target.checked ? [...p, id] : p.filter((x) => x !== id)))}
                />
                <span>
                  <span className="block font-medium">{PRESETS[id].label}</span>
                  <span className="block text-xs text-slate-500">{PRESETS[id].description}</span>
                </span>
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="mb-1 font-medium">Custom adjustments</legend>
          <p className="mb-2 text-xs text-slate-500">Leave blank for no change. Use a minus sign for a fall, e.g. −1.5.</p>
          <div className="grid gap-3 sm:grid-cols-2">
            {ADJUSTMENTS.map((a) => (
              <div key={a.key}>
                <label htmlFor={`${uid}-${a.key}`} className="mb-1 block font-medium text-slate-800">
                  {a.label} <span className="font-normal text-slate-500">({a.unit})</span>
                </label>
                <input
                  id={`${uid}-${a.key}`}
                  className="input tabular-nums"
                  inputMode="text"
                  autoComplete="off"
                  placeholder="No change"
                  value={adjust[a.key]}
                  onChange={(e) => setAdjust((d) => ({ ...d, [a.key]: e.target.value }))}
                  {...invalid(a.key)}
                />
                <p className="mt-1 text-xs text-slate-500">{a.help}</p>
                {err(a.key)}
              </div>
            ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="mb-1 font-medium">Leave out</legend>
          <p className="mb-2 text-xs text-slate-500">Model life without an item: a sold car, a lost rental, a cancelled policy.</p>
          <div className="grid gap-3 sm:grid-cols-2">
            {(Object.keys(KIND_LABELS) as (keyof typeof KIND_LABELS)[])
              .filter((k) => dataset[k].length > 0)
              .map((k) => (
                <div key={k}>
                  <h3 className="mb-1 text-xs font-medium tracking-wide text-slate-500 uppercase">{KIND_LABELS[k]}</h3>
                  <ul className="space-y-0.5">
                    {dataset[k].map((item) => (
                      <li key={item.id}>
                        <label className="flex items-center gap-2">
                          <input
                            type="checkbox"
                            className="size-4 accent-brand-700"
                            checked={excluded.has(item.id)}
                            onChange={(e) =>
                              setExcluded((s) => {
                                const next = new Set(s)
                                if (e.target.checked) next.add(item.id)
                                else next.delete(item.id)
                                return next
                              })
                            }
                          />
                          {item.name}
                        </label>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
          </div>
        </fieldset>

        <fieldset>
          <legend className="mb-1 font-medium">Extra one-off events</legend>
          <p className="mb-2 text-xs text-slate-500">Only in this scenario: a retrenchment package, an emergency, a delayed payout.</p>
          {events.length > 0 && (
            <div className="space-y-2">
              {events.map((e, i) => (
                <div key={e.id} className="grid grid-cols-2 gap-2 rounded-md border border-slate-200 p-2 sm:grid-cols-[2fr_1fr_1fr_1fr_auto] sm:items-start">
                  <div className="col-span-2 sm:col-span-1">
                    <input
                      aria-label={`Event ${i + 1} name`}
                      className="input"
                      placeholder="Name"
                      value={e.name}
                      onChange={(x) => setEvents((es) => es.map((y) => (y.id === e.id ? { ...y, name: x.target.value } : y)))}
                      {...invalid(`event-${i}-name`)}
                    />
                    {err(`event-${i}-name`)}
                  </div>
                  <div>
                    <input
                      aria-label={`Event ${i + 1} month`}
                      type="month"
                      className="input"
                      placeholder="YYYY-MM"
                      value={e.month}
                      onChange={(x) => setEvents((es) => es.map((y) => (y.id === e.id ? { ...y, month: x.target.value } : y)))}
                      {...invalid(`event-${i}-month`)}
                    />
                    {err(`event-${i}-month`)}
                  </div>
                  <div>
                    <input
                      aria-label={`Event ${i + 1} amount`}
                      className="input tabular-nums"
                      inputMode="decimal"
                      placeholder="Amount"
                      value={e.amount}
                      onChange={(x) => setEvents((es) => es.map((y) => (y.id === e.id ? { ...y, amount: x.target.value } : y)))}
                      {...invalid(`event-${i}-amount`)}
                    />
                    {err(`event-${i}-amount`)}
                  </div>
                  <select
                    aria-label={`Event ${i + 1} direction`}
                    className="input"
                    value={e.direction}
                    onChange={(x) =>
                      setEvents((es) => es.map((y) => (y.id === e.id ? { ...y, direction: x.target.value as OneOffEvent['direction'] } : y)))
                    }
                  >
                    <option value="outflow">Outflow</option>
                    <option value="inflow">Inflow</option>
                  </select>
                  <button
                    type="button"
                    className="btn btn-ghost btn-sm text-red-700"
                    aria-label={`Remove event ${i + 1}`}
                    onClick={() => setEvents((es) => es.filter((y) => y.id !== e.id))}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
          <button
            type="button"
            className="btn btn-sm mt-2"
            onClick={() => setEvents((es) => [...es, { id: newId(), name: '', month: dataset.settings.asOfMonth, amount: '', direction: 'outflow' }])}
          >
            + Add event
          </button>
        </fieldset>

        {nothing && <Notice tone="warn">This scenario changes nothing yet, so it will match the base case.</Notice>}
        {showErrors && !valid && <Notice tone="error">Fix the highlighted fields.</Notice>}
        {saveError && <Notice tone="error">{saveError}</Notice>}
      </form>
    </Modal>
  )
}
