import { useState } from 'react'
import { deleteEntity, moveEntity, newId } from '../../db/repo'
import type { EntityKind, EntityRecords } from '../../schema/entities'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { EntityForm } from './EntityForm'
import type { EditorContext, EntityConfig } from './types'

type Editing<K extends EntityKind> =
  | { mode: 'new'; initial: Partial<EntityRecords[K]> & { id: string; sortOrder: number } }
  | { mode: 'edit'; initial: EntityRecords[K] }

export function EntityEditor<K extends EntityKind>({ config, ctx }: { config: EntityConfig<K>; ctx: EditorContext }) {
  const stored = ctx.dataset[config.kind] as EntityRecords[K][]
  const records = config.sort ? [...stored].sort(config.sort) : stored
  const [editing, setEditing] = useState<Editing<K> | null>(null)
  const [deleting, setDeleting] = useState<EntityRecords[K] | null>(null)

  const add = () => {
    const sortOrder = stored.reduce((max, r) => Math.max(max, r.sortOrder + 1), 0)
    setEditing({ mode: 'new', initial: { ...config.defaults(ctx), id: newId(), sortOrder } })
  }

  return (
    <section className="space-y-4">
      <header className="flex flex-wrap items-end justify-between gap-3">
        <div className="max-w-2xl">
          <h1 className="text-xl font-semibold">{config.title}</h1>
          <div className="mt-1 text-sm text-slate-600">{config.intro}</div>
        </div>
        <button type="button" className="btn btn-primary" onClick={add}>
          + Add {config.singular}
        </button>
      </header>

      {config.summary && records.length > 0 && <div>{config.summary(records, ctx)}</div>}

      {records.length === 0 ? (
        <div className="card px-6 py-10 text-center text-sm text-slate-600">
          <p>No {config.title.toLowerCase()} yet.</p>
          <button type="button" className="btn mt-3" onClick={add}>
            Add your first {config.singular}
          </button>
        </div>
      ) : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-slate-200 bg-slate-50 text-left text-xs font-medium tracking-wide text-slate-500 uppercase">
              <tr>
                {config.columns.map((c) => (
                  <th key={c.label} scope="col" className={`px-3 py-2 ${c.numeric ? 'text-right' : ''} ${c.secondary ? 'hidden md:table-cell' : ''}`}>
                    {c.label}
                  </th>
                ))}
                <th scope="col" className="px-3 py-2">
                  <span className="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {records.map((r, i) => {
                const warnings = config.warnings?.(r, ctx) ?? []
                return (
                  <tr key={r.id} className="align-top hover:bg-slate-50/60">
                    {config.columns.map((c, ci) => (
                      <td key={c.label} className={`px-3 py-2 ${c.numeric ? 'num' : ''} ${c.secondary ? 'hidden md:table-cell' : ''}`}>
                        {c.render(r, ctx)}
                        {ci === 0 && warnings.length > 0 && (
                          <ul className="mt-1 space-y-0.5">
                            {warnings.map((w) => (
                              <li key={w.text} className={`text-xs ${w.tone === 'warn' ? 'text-amber-700' : 'text-slate-500'}`}>
                                {w.text}
                              </li>
                            ))}
                          </ul>
                        )}
                      </td>
                    ))}
                    <td className="px-3 py-1.5 whitespace-nowrap text-right">
                      {config.reorder && (
                        <>
                          <button
                            type="button"
                            className="btn btn-ghost btn-sm"
                            disabled={i === 0}
                            aria-label={`Move ${r.name} up`}
                            onClick={() => moveEntity(config.kind, r.id, -1)}
                          >
                            ↑
                          </button>
                          <button
                            type="button"
                            className="btn btn-ghost btn-sm"
                            disabled={i === records.length - 1}
                            aria-label={`Move ${r.name} down`}
                            onClick={() => moveEntity(config.kind, r.id, 1)}
                          >
                            ↓
                          </button>
                        </>
                      )}
                      <button type="button" className="btn btn-ghost btn-sm" aria-label={`Edit ${r.name}`} onClick={() => setEditing({ mode: 'edit', initial: r })}>
                        Edit
                      </button>
                      <button
                        type="button"
                        className="btn btn-ghost btn-sm text-red-700"
                        aria-label={`Delete ${r.name}`}
                        onClick={() => setDeleting(r)}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
          {config.reorder && <p className="border-t border-slate-100 px-3 py-2 text-xs text-slate-500">{config.reorder}</p>}
        </div>
      )}

      {editing && (
        <EntityForm
          key={editing.initial.id}
          config={config}
          ctx={ctx}
          initial={editing.initial}
          isNew={editing.mode === 'new'}
          onClose={() => setEditing(null)}
        />
      )}
      {deleting && (
        <ConfirmDialog
          title={`Delete ${config.singular}?`}
          confirmLabel="Delete"
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            await deleteEntity(config.kind, deleting.id)
            setDeleting(null)
          }}
        >
          <p>
            <strong>{deleting.name}</strong> will be removed from the model. This cannot be undone, except by restoring an export.
          </p>
        </ConfirmDialog>
      )}
    </section>
  )
}
