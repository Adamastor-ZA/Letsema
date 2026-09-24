import { useMemo, useState } from 'react'
import type { z } from 'zod'
import { saveEntity } from '../../db/repo'
import { entitySchemas, type EntityKind, type EntityRecords } from '../../schema/entities'
import { Modal } from '../components/Modal'
import { Notice } from '../components/Notice'
import { draftToRecord, isVisible, recordToDraft, type Draft, type DraftValue } from './fields'
import { FieldInput } from './FieldInput'
import type { EditorContext, EntityConfig } from './types'

interface EntityFormProps<K extends EntityKind> {
  config: EntityConfig<K>
  ctx: EditorContext
  /** The stored record, or a new record's id, sort order and defaults. */
  initial: Partial<EntityRecords[K]> & { id: string; sortOrder: number }
  isNew: boolean
  onClose: () => void
}

export function EntityForm<K extends EntityKind>({ config, ctx, initial, isNew, onClose }: EntityFormProps<K>) {
  const fields = useMemo(() => config.fields(ctx), [config, ctx])
  const [draft, setDraft] = useState<Draft>(() => recordToDraft(fields, initial as Record<string, unknown>))
  const [showErrors, setShowErrors] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const schema = entitySchemas[config.kind] as unknown as z.ZodType<EntityRecords[K]>
  const base = { id: initial.id, sortOrder: initial.sortOrder }
  const result = draftToRecord(fields, draft, base, schema)
  const warnings = result.value && config.warnings ? config.warnings(result.value, ctx) : []

  const set = (key: string, value: DraftValue) => setDraft((d) => ({ ...d, [key]: value }))

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setShowErrors(true)
    if (!result.value) return
    setSaving(true)
    try {
      await saveEntity(config.kind, result.value)
      onClose()
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : String(err))
      setSaving(false)
    }
  }

  const title = `${isNew ? 'Add' : 'Edit'} ${config.singular}`
  return (
    <Modal
      title={title}
      onClose={onClose}
      size="lg"
      footer={
        <>
          <button type="button" className="btn" onClick={onClose}>
            Cancel
          </button>
          <button type="submit" form="entity-form" className="btn btn-primary" disabled={saving}>
            {isNew ? `Add ${config.singular}` : 'Save changes'}
          </button>
        </>
      }
    >
      <form id="entity-form" noValidate onSubmit={submit} className="space-y-4">
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
                onChange={(v) => set(f.key, v)}
              />
            ))}
        </div>
        {showErrors && result.formErrors.length > 0 && <Notice tone="error">{result.formErrors.join('. ')}</Notice>}
        {saveError && <Notice tone="error">{saveError}</Notice>}
        {warnings.length > 0 && (
          <div className="space-y-2">
            {warnings.map((w) => (
              <Notice key={w.text} tone={w.tone}>
                {w.text}
              </Notice>
            ))}
          </div>
        )}
      </form>
    </Modal>
  )
}
