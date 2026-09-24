import { useState } from 'react'
import { deleteScenario, freeScenarioSlot, newId, restoreDefaultScenarios, setScenarioActive } from '../../db/repo'
import { resolveOverrides } from '../../engine/scenarios'
import { MAX_SCENARIOS, defaultScenarios, type ScenarioRecord } from '../../schema/dataset'
import { LiquidChart } from '../charts/LiquidChart'
import { BASE_COLOR, scenarioColor } from '../charts/theme'
import { ComparisonTable } from '../components/ComparisonTable'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { DisplayToggle } from '../components/DisplayToggle'
import { Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'
import { useModel } from '../hooks/useModel'
import { useScenarios } from '../hooks/useScenarios'
import { describeOverrides } from '../lib/describe'
import { GettingStarted } from './DashboardPage'
import { ScenarioForm } from './ScenarioForm'

export function ScenariosPage({ ctx }: { ctx: EditorContext }) {
  const { dataset, fmt } = ctx
  const model = useModel(dataset)
  const scenarios = useScenarios(dataset)
  const [editing, setEditing] = useState<{ record: ScenarioRecord; isNew: boolean } | null>(null)
  const [deleting, setDeleting] = useState<ScenarioRecord | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  if ('error' in model) return <Notice tone="error">The projection could not run: {model.error}</Notice>
  if ('error' in scenarios) return <Notice tone="error">A scenario could not run: {scenarios.error}</Notice>

  const full = dataset.scenarios.length >= MAX_SCENARIOS
  const missingDefaults = defaultScenarios().filter((d) => !dataset.scenarios.some((s) => s.id === d.id)).length

  const create = async () => {
    const slot = await freeScenarioSlot()
    if (slot === null) return
    setEditing({ record: { id: newId(), name: '', presets: [], custom: {}, active: true, slot }, isNew: true })
  }

  const columns = [
    { key: 'base', label: 'Base case', color: BASE_COLOR, evaluation: scenarios.base },
    ...scenarios.active.map((r) => ({ key: r.scenario.id, label: r.scenario.name, color: scenarioColor(r.scenario.slot), evaluation: r.evaluation })),
  ]

  return (
    <section className="space-y-5">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div className="max-w-2xl">
          <h1 className="text-xl font-semibold">Scenarios</h1>
          <p className="mt-1 text-sm text-slate-600">
            Stress the base case. Each scenario combines any of the presets with custom adjustments, and is compared side by side with base.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <DisplayToggle settings={dataset.settings} />
          <button type="button" className="btn btn-primary" onClick={create} disabled={full} title={full ? `Up to ${MAX_SCENARIOS} scenarios` : undefined}>
            + New scenario
          </button>
        </div>
      </header>

      {notice && <Notice>{notice}</Notice>}

      <div className="card divide-y divide-slate-100">
        {scenarios.runs.length === 0 && <p className="p-4 text-sm text-slate-600">No scenarios. Create one, or restore the standard stress tests.</p>}
        {scenarios.runs.map(({ scenario }) => {
          const lines = describeOverrides(resolveOverrides(scenario), dataset, fmt)
          return (
            <div key={scenario.id} className="flex flex-wrap items-start gap-3 p-3 sm:flex-nowrap">
              <label className="flex shrink-0 items-center gap-2 pt-0.5 text-sm" title="Compare against base">
                <input
                  type="checkbox"
                  className="size-4 accent-brand-700"
                  checked={scenario.active}
                  onChange={(e) => setScenarioActive(scenario.id, e.target.checked)}
                  aria-label={`Compare ${scenario.name}`}
                />
                <span aria-hidden="true" className="inline-block h-0.5 w-5 rounded" style={{ background: scenarioColor(scenario.slot) }} />
              </label>
              <div className="min-w-0 flex-1">
                <div className="font-medium">{scenario.name}</div>
                <div className="text-sm text-slate-600">{lines.length ? lines.join('. ') + '.' : 'No changes: matches the base case.'}</div>
              </div>
              <div className="flex shrink-0 gap-1">
                <button type="button" className="btn btn-ghost btn-sm" aria-label={`Edit ${scenario.name}`} onClick={() => setEditing({ record: scenario, isNew: false })}>
                  Edit
                </button>
                <button type="button" className="btn btn-ghost btn-sm text-red-700" aria-label={`Delete ${scenario.name}`} onClick={() => setDeleting(scenario)}>
                  Delete
                </button>
              </div>
            </div>
          )
        })}
        {missingDefaults > 0 && !full && (
          <div className="p-3 text-sm">
            <button
              type="button"
              className="text-brand-700 underline"
              onClick={async () => {
                const n = await restoreDefaultScenarios()
                setNotice(n ? `Restored ${n} standard ${n === 1 ? 'scenario' : 'scenarios'}.` : 'No room to restore more scenarios.')
              }}
            >
              Restore the standard stress scenarios
            </button>
          </div>
        )}
      </div>

      {model.isEmpty ? (
        <GettingStarted />
      ) : (
        <>
          <h2 className="text-base font-semibold">Side by side</h2>
          {scenarios.active.length === 0 && <Notice>Tick a scenario above to compare it against the base case.</Notice>}
          <ComparisonTable columns={columns} settings={dataset.settings} fmt={fmt} display={model.display} />
          <LiquidChart
            title="Liquid balance by scenario"
            subtitle="Liquid assets less any carried deficit. Below zero, a shortfall is being carried. Select a legend item to show or hide it."
            fmt={fmt}
            display={model.display}
            firstShortfall={scenarios.base.metrics.firstShortfall.month}
            series={columns.map((c) => ({ key: c.key, label: c.label, color: c.color, rows: c.evaluation.result.rows }))}
          />
        </>
      )}

      {editing && <ScenarioForm key={editing.record.id} dataset={dataset} initial={editing.record} isNew={editing.isNew} onClose={() => setEditing(null)} />}
      {deleting && (
        <ConfirmDialog
          title="Delete scenario?"
          confirmLabel="Delete"
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            await deleteScenario(deleting.id)
            setDeleting(null)
          }}
        >
          <p>
            <strong>{deleting.name}</strong> will be removed. Your data is not affected.
          </p>
        </ConfirmDialog>
      )}
    </section>
  )
}
