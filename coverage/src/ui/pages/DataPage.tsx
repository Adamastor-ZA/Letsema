import { useEffect, useState } from 'react'
import { clearAllData, loadSampleData } from '../../db/repo'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Notice } from '../components/Notice'
import type { EditorContext } from '../editors/types'

function usePersistence() {
  const [persisted, setPersisted] = useState<boolean | null>(null)
  useEffect(() => {
    let live = true
    navigator.storage?.persisted?.().then((p) => live && setPersisted(p), () => live && setPersisted(null))
    return () => {
      live = false
    }
  }, [])
  const request = async () => setPersisted((await navigator.storage?.persist?.()) ?? null)
  return { persisted, request }
}

export function DataPage({ ctx }: { ctx: EditorContext }) {
  const [confirm, setConfirm] = useState<'sample' | 'clear' | null>(null)
  const [done, setDone] = useState<string | null>(null)
  const { persisted, request } = usePersistence()
  const d = ctx.dataset
  const count = d.assets.length + d.debts.length + d.obligations.length + d.incomes.length + d.events.length

  return (
    <section className="max-w-3xl space-y-4">
      <header>
        <h1 className="text-xl font-semibold">Data</h1>
        <p className="mt-1 text-sm text-slate-600">
          Everything is stored in this browser&rsquo;s IndexedDB on this device. Nothing is sent anywhere. Clearing your browser&rsquo;s site data
          deletes it.
        </p>
      </header>

      {done && <Notice>{done}</Notice>}

      <div className="card divide-y divide-slate-100">
        <div className="flex flex-wrap items-center justify-between gap-3 p-4">
          <div className="text-sm">
            <h2 className="font-medium">Persistent storage</h2>
            <p className="text-slate-600">
              {persisted === true
                ? 'Granted: the browser will not clear this data to free up space.'
                : persisted === false
                  ? 'Not granted: the browser may clear this data if the device runs low on space.'
                  : 'Status unavailable in this browser.'}
            </p>
          </div>
          {persisted === false && (
            <button type="button" className="btn" onClick={request}>
              Request persistence
            </button>
          )}
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 p-4">
          <div className="text-sm">
            <h2 className="font-medium">Load sample data</h2>
            <p className="text-slate-600">A fictional household, to explore the app. Replaces everything currently stored.</p>
          </div>
          <button type="button" className="btn" onClick={() => setConfirm('sample')}>
            Load sample data
          </button>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 p-4">
          <div className="text-sm">
            <h2 className="font-medium">Export and import</h2>
            <p className="text-slate-600">JSON and encrypted backups arrive in Phase 5.</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 p-4">
          <div className="text-sm">
            <h2 className="font-medium text-red-800">Clear all data</h2>
            <p className="text-slate-600">
              Deletes all {count} items, scenarios, snapshots and settings from this browser.
            </p>
          </div>
          <button type="button" className="btn btn-danger" onClick={() => setConfirm('clear')}>
            Clear all data
          </button>
        </div>
      </div>

      {confirm === 'sample' && (
        <ConfirmDialog
          title="Replace your data with the sample?"
          confirmLabel="Load sample data"
          typeToConfirm={count > 0 ? 'replace' : undefined}
          onCancel={() => setConfirm(null)}
          onConfirm={async () => {
            await loadSampleData()
            setConfirm(null)
            setDone('Sample data loaded. Every figure is fictional.')
          }}
        >
          <p>
            {count > 0
              ? `This deletes your ${count} items, scenarios and snapshots and loads a fictional household. Display preferences are kept.`
              : 'This loads a fictional household dated from the current month.'}
          </p>
        </ConfirmDialog>
      )}
      {confirm === 'clear' && (
        <ConfirmDialog
          title="Clear all data?"
          confirmLabel="Clear everything"
          typeToConfirm="clear"
          onCancel={() => setConfirm(null)}
          onConfirm={async () => {
            await clearAllData()
            setConfirm(null)
            setDone('All data cleared.')
          }}
        >
          <p>This permanently deletes everything stored by this app in this browser. It cannot be undone.</p>
        </ConfirmDialog>
      )}
    </section>
  )
}
