import { useState } from 'react'
import { updateSettings } from '../../db/repo'
import { thresholdsSchema, type Thresholds } from '../../schema/settings'
import { Modal } from '../components/Modal'
import { Notice } from '../components/Notice'

const ROWS: { key: keyof Thresholds; label: string; unit: string; decimals: boolean }[] = [
  { key: 'coverageRatio', label: '12-month coverage ratio', unit: '×', decimals: true },
  { key: 'firstShortfallMonths', label: 'Months until first shortfall', unit: 'months', decimals: false },
  { key: 'runwayVariableMonths', label: 'Runway if variable income stops', unit: 'months', decimals: false },
  { key: 'runwayAllMonths', label: 'Runway if all income stops', unit: 'months', decimals: false },
]

type Draft = Record<keyof Thresholds, { green: string; amber: string }>

export function ThresholdsDialog({ thresholds, onClose }: { thresholds: Thresholds; onClose: () => void }) {
  const [draft, setDraft] = useState<Draft>(
    () => Object.fromEntries(ROWS.map((r) => [r.key, { green: String(thresholds[r.key].green), amber: String(thresholds[r.key].amber) }])) as Draft,
  )
  const [error, setError] = useState<string | null>(null)

  const save = async (e: React.FormEvent) => {
    e.preventDefault()
    const candidate = Object.fromEntries(
      ROWS.map((r) => [r.key, { green: Number(draft[r.key].green.replace(',', '.')), amber: Number(draft[r.key].amber.replace(',', '.')) }]),
    )
    const bad = ROWS.find((r) => {
      const v = candidate[r.key]!
      return !Number.isFinite(v.green) || !Number.isFinite(v.amber) || draft[r.key].green.trim() === '' || draft[r.key].amber.trim() === ''
    })
    if (bad) return setError(`Enter numbers for "${bad.label}".`)
    const parsed = thresholdsSchema.safeParse(candidate)
    if (!parsed.success) {
      const issue = parsed.error.issues[0]!
      const row = ROWS.find((r) => r.key === issue.path[0])
      return setError(`${row?.label ?? 'Thresholds'}: ${issue.message}.`)
    }
    await updateSettings({ thresholds: parsed.data })
    onClose()
  }

  return (
    <Modal
      title="Status thresholds"
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" form="thresholds-form" className="btn btn-primary">
            Save thresholds
          </button>
        </>
      }
    >
      <form id="thresholds-form" noValidate onSubmit={save} className="space-y-3 text-sm">
        <p className="text-slate-600">
          Each metric is green at or above the first value, amber at or above the second and red below it. A metric that never bites within the
          horizon is green.
        </p>
        <table className="w-full">
          <thead className="text-left text-xs text-slate-500">
            <tr>
              <th scope="col" className="pb-1 font-medium">
                Metric
              </th>
              <th scope="col" className="pb-1 font-medium">
                Green at or above
              </th>
              <th scope="col" className="pb-1 font-medium">
                Amber at or above
              </th>
            </tr>
          </thead>
          <tbody>
            {ROWS.map((r) => (
              <tr key={r.key}>
                <th scope="row" className="py-1 pr-3 text-left font-normal">
                  {r.label} <span className="text-xs text-slate-400">({r.unit})</span>
                </th>
                {(['green', 'amber'] as const).map((level) => (
                  <td key={level} className="py-1 pr-2">
                    <input
                      className="input w-24 tabular-nums"
                      inputMode={r.decimals ? 'decimal' : 'numeric'}
                      aria-label={`${r.label}, ${level} threshold`}
                      value={draft[r.key][level]}
                      onChange={(e) => {
                        setError(null)
                        setDraft((d) => ({ ...d, [r.key]: { ...d[r.key], [level]: e.target.value } }))
                      }}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {error && <Notice tone="error">{error}</Notice>}
      </form>
    </Modal>
  )
}
