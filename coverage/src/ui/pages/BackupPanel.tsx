import { useRef, useState } from 'react'
import { backupFilename, buildEncryptedExport, buildExport, ImportError, openEncryptedBackup, parseBackup } from '../../db/backup'
import { DecryptError, MIN_PASSPHRASE_LENGTH, type EncryptedEnvelope } from '../../db/crypto'
import { readDataset, replaceDataset, updateSettings } from '../../db/repo'
import type { Dataset } from '../../schema/dataset'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { Modal } from '../components/Modal'
import { Notice } from '../components/Notice'
import type { Formatter } from '../lib/format'
import { downloadText, todayIso } from '../lib/download'

type Status = { tone: 'info' | 'error'; text: string } | null

function EncryptDialog({ onClose, onDone }: { onClose: () => void; onDone: (text: string) => void }) {
  const [pass, setPass] = useState('')
  const [again, setAgain] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (pass.length < MIN_PASSPHRASE_LENGTH) return setError(`Use at least ${MIN_PASSPHRASE_LENGTH} characters. A few unrelated words works well.`)
    if (pass !== again) return setError('The passphrases do not match.')
    setBusy(true)
    try {
      const now = new Date()
      const text = await buildEncryptedExport(await readDataset(), now.toISOString(), pass)
      downloadText(backupFilename(todayIso(now), true), text)
      await updateSettings({ lastExportAt: now.toISOString() })
      onDone('Encrypted backup saved to your downloads.')
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
      setBusy(false)
    }
  }
  return (
    <Modal
      title="Encrypted backup"
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" form="encrypt-form" className="btn btn-primary" disabled={busy}>
            {busy ? 'Encrypting…' : 'Encrypt and save'}
          </button>
        </>
      }
    >
      <form id="encrypt-form" noValidate onSubmit={submit} className="space-y-3 text-sm">
        <p className="text-slate-600">
          The file is encrypted in this browser with AES-256-GCM, using a key derived from your passphrase. Without the passphrase the backup cannot
          be opened by anyone, including you.
        </p>
        <label className="block">
          <span className="mb-1 block font-medium">Passphrase</span>
          <input className="input" type="password" autoComplete="new-password" value={pass} onChange={(e) => setPass(e.target.value)} />
        </label>
        <label className="block">
          <span className="mb-1 block font-medium">Repeat passphrase</span>
          <input className="input" type="password" autoComplete="new-password" value={again} onChange={(e) => setAgain(e.target.value)} />
        </label>
        {error && <Notice tone="error">{error}</Notice>}
      </form>
    </Modal>
  )
}

function DecryptDialog({ envelope, onClose, onOpened }: { envelope: EncryptedEnvelope; onClose: () => void; onOpened: (d: Dataset, exportedAt: string) => void }) {
  const [pass, setPass] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setBusy(true)
    setError(null)
    try {
      const opened = await openEncryptedBackup(envelope, pass)
      onOpened(opened.dataset, opened.exportedAt)
    } catch (err) {
      setError(err instanceof DecryptError || err instanceof ImportError ? err.message : String(err))
      setBusy(false)
    }
  }
  return (
    <Modal
      title="Open encrypted backup"
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" form="decrypt-form" className="btn btn-primary" disabled={busy || pass === ''}>
            {busy ? 'Decrypting…' : 'Decrypt'}
          </button>
        </>
      }
    >
      <form id="decrypt-form" noValidate onSubmit={submit} className="space-y-3 text-sm">
        <label className="block">
          <span className="mb-1 block font-medium">Passphrase</span>
          <input className="input" type="password" autoComplete="current-password" value={pass} onChange={(e) => setPass(e.target.value)} />
        </label>
        {error && <Notice tone="error">{error}</Notice>}
      </form>
    </Modal>
  )
}

export function BackupPanel({ lastExportAt, fmt }: { lastExportAt: string | null; fmt: Formatter }) {
  const fileInput = useRef<HTMLInputElement>(null)
  const [status, setStatus] = useState<Status>(null)
  const [encrypting, setEncrypting] = useState(false)
  const [envelope, setEnvelope] = useState<EncryptedEnvelope | null>(null)
  const [pending, setPending] = useState<{ dataset: Dataset; exportedAt: string } | null>(null)

  const exportPlain = async () => {
    const now = new Date()
    downloadText(backupFilename(todayIso(now), false), buildExport(await readDataset(), now.toISOString()))
    await updateSettings({ lastExportAt: now.toISOString() })
    setStatus({ tone: 'info', text: 'Backup saved to your downloads. It is not encrypted: store it somewhere private.' })
  }

  const chooseFile = async (file: File | undefined) => {
    if (!file) return
    setStatus(null)
    try {
      const parsed = parseBackup(await file.text())
      if (parsed.kind === 'encrypted') setEnvelope(parsed.envelope)
      else setPending({ dataset: parsed.dataset, exportedAt: parsed.exportedAt })
    } catch (err) {
      setStatus({ tone: 'error', text: err instanceof ImportError ? err.message : `Could not read the file: ${String(err)}` })
    } finally {
      if (fileInput.current) fileInput.current.value = ''
    }
  }

  const count = (d: Dataset) => d.assets.length + d.debts.length + d.obligations.length + d.incomes.length + d.events.length

  return (
    <>
      <div className="flex flex-wrap items-center justify-between gap-3 p-4">
        <div className="text-sm">
          <h2 className="font-medium">Back up</h2>
          <p className="text-slate-600">
            Save everything as a JSON file, plain or encrypted with a passphrase. Last backup:{' '}
            {lastExportAt ? new Date(lastExportAt).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' }) : 'never'}.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button type="button" className="btn" onClick={exportPlain}>
            Export JSON
          </button>
          <button type="button" className="btn btn-primary" onClick={() => setEncrypting(true)}>
            Export encrypted
          </button>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3 p-4">
        <div className="text-sm">
          <h2 className="font-medium">Restore</h2>
          <p className="text-slate-600">Import a backup made by this app. It replaces everything currently stored.</p>
        </div>
        <label className="btn cursor-pointer">
          Import backup…
          <input ref={fileInput} type="file" accept="application/json,.json" className="sr-only" onChange={(e) => chooseFile(e.target.files?.[0])} />
        </label>
      </div>
      {status && (
        <div className="px-4 pb-4">
          <Notice tone={status.tone}>{status.text}</Notice>
        </div>
      )}

      {encrypting && (
        <EncryptDialog
          onClose={() => setEncrypting(false)}
          onDone={(text) => {
            setEncrypting(false)
            setStatus({ tone: 'info', text })
          }}
        />
      )}
      {envelope && (
        <DecryptDialog
          envelope={envelope}
          onClose={() => setEnvelope(null)}
          onOpened={(dataset, exportedAt) => {
            setEnvelope(null)
            setPending({ dataset, exportedAt })
          }}
        />
      )}
      {pending && (
        <ConfirmDialog
          title="Replace your data with this backup?"
          confirmLabel="Replace and restore"
          typeToConfirm="replace"
          onCancel={() => setPending(null)}
          onConfirm={async () => {
            await replaceDataset(pending.dataset)
            setPending(null)
            setStatus({ tone: 'info', text: 'Backup restored.' })
          }}
        >
          <p>
            The backup was made on {new Date(pending.exportedAt).toLocaleString('en-GB')} and holds {count(pending.dataset)} items,{' '}
            {pending.dataset.scenarios.length} scenarios and {pending.dataset.snapshots.length} check-ins, as of{' '}
            {fmt.month(pending.dataset.settings.asOfMonth)}.
          </p>
          <p>Everything currently stored in this browser is deleted and replaced.</p>
        </ConfirmDialog>
      )}
    </>
  )
}
