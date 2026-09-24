import { useState, type ReactNode } from 'react'
import { Modal } from './Modal'

interface ConfirmDialogProps {
  title: string
  children: ReactNode
  confirmLabel: string
  onConfirm: () => void | Promise<void>
  onCancel: () => void
  /** Require the user to type this word before confirming. */
  typeToConfirm?: string
  danger?: boolean
}

export function ConfirmDialog({ title, children, confirmLabel, onConfirm, onCancel, typeToConfirm, danger = true }: ConfirmDialogProps) {
  const [typed, setTyped] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const ready = !typeToConfirm || typed.trim().toLowerCase() === typeToConfirm.toLowerCase()

  const confirm = async () => {
    setBusy(true)
    setError(null)
    try {
      await onConfirm()
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e))
      setBusy(false)
    }
  }

  return (
    <Modal
      title={title}
      onClose={onCancel}
      footer={
        <>
          <button type="button" className="btn" onClick={onCancel}>
            Cancel
          </button>
          <button type="button" className={`btn ${danger ? 'btn-danger' : 'btn-primary'}`} disabled={!ready || busy} onClick={confirm}>
            {confirmLabel}
          </button>
        </>
      }
    >
      <div className="space-y-3 text-sm text-slate-700">
        {children}
        {typeToConfirm && (
          <label className="block">
            <span className="mb-1 block text-slate-600">
              Type <strong className="font-mono">{typeToConfirm}</strong> to confirm
            </span>
            <input className="input" value={typed} onChange={(e) => setTyped(e.target.value)} autoComplete="off" />
          </label>
        )}
        {error && <p className="text-red-700">{error}</p>}
      </div>
    </Modal>
  )
}
