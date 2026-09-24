import type { z } from 'zod'
import { formatMoneyInput, formatPercentInput, parseInteger, parseMoney, parsePercent, type Parsed } from '../lib/parse'

/** Raw form state: strings for typed inputs, arrays for month pickers, booleans for checkboxes. */
export type DraftValue = string | number[] | boolean
export type Draft = Record<string, DraftValue>

export type FieldKind =
  | 'text'
  | 'money'
  | 'percent'
  | 'integer'
  | 'month'
  | 'optionalMonth'
  | 'calendarMonth'
  | 'calendarMonths'
  | 'select'
  | 'checkbox'

export interface FieldDef {
  key: string
  label: string
  kind: FieldKind
  help?: string | ((draft: Draft) => string)
  options?: { value: string; label: string }[]
  allowNegative?: boolean
  placeholder?: string
  /** Hidden fields are not shown and are stored as `hiddenValue`. */
  visible?: (draft: Draft) => boolean
  hiddenValue?: unknown
  /** Form value used when the stored value is missing (e.g. a field revealed by changing tier). */
  defaultDraft?: DraftValue
  /** select only: store an empty choice as null. */
  emptyAsNull?: boolean
  /** calendarMonths only: pick exactly one month with a select instead of toggles. */
  single?: (draft: Draft) => boolean
  /** Takes a full row in the form grid. */
  wide?: boolean
  suffix?: string
}

export const MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
export const MONTH_SHORT = MONTH_NAMES.map((m) => m.slice(0, 3))

export function isVisible(field: FieldDef, draft: Draft): boolean {
  return field.visible ? field.visible(draft) : true
}

/** Stored value → form value. */
export function toDraftValue(field: FieldDef, value: unknown): DraftValue {
  if ((value === undefined || value === null) && field.defaultDraft !== undefined) return field.defaultDraft
  switch (field.kind) {
    case 'money':
      return typeof value === 'number' ? formatMoneyInput(value) : ''
    case 'percent':
      return typeof value === 'number' ? formatPercentInput(value) : ''
    case 'integer':
    case 'calendarMonth':
      return typeof value === 'number' ? String(value) : ''
    case 'optionalMonth':
      return typeof value === 'string' ? value : ''
    case 'calendarMonths':
      return Array.isArray(value) ? [...(value as number[])] : []
    case 'checkbox':
      return value === true
    default:
      return typeof value === 'string' ? value : ''
  }
}

/** Form value → stored value, or a field error. */
export function fromDraftValue(field: FieldDef, raw: DraftValue): Parsed<unknown> {
  const text = typeof raw === 'string' ? raw : ''
  switch (field.kind) {
    case 'money':
      return parseMoney(text, { allowNegative: field.allowNegative })
    case 'percent':
      return parsePercent(text, { allowNegative: field.allowNegative })
    case 'integer':
      return parseInteger(text)
    case 'calendarMonth':
      return { ok: true, value: Number(text) }
    case 'month':
      return { ok: true, value: text.trim() }
    case 'optionalMonth':
      return { ok: true, value: text.trim() === '' ? null : text.trim() }
    case 'calendarMonths':
      return { ok: true, value: [...(raw as number[])].sort((a, b) => a - b) }
    case 'checkbox':
      return { ok: true, value: raw === true }
    case 'select':
      return { ok: true, value: field.emptyAsNull && text === '' ? null : text }
    default:
      return { ok: true, value: text }
  }
}

export function recordToDraft(fields: FieldDef[], record: Record<string, unknown>): Draft {
  return Object.fromEntries(fields.map((f) => [f.key, toDraftValue(f, record[f.key])]))
}

export interface DraftResult<T> {
  value?: T
  fieldErrors: Record<string, string>
  formErrors: string[]
}

/**
 * Parse every visible field, substitute hidden values, then validate the
 * assembled record with the schema. Schema issues are mapped back to fields.
 */
export function draftToRecord<T>(fields: FieldDef[], draft: Draft, base: Record<string, unknown>, schema: z.ZodType<T>): DraftResult<T> {
  const fieldErrors: Record<string, string> = {}
  const candidate: Record<string, unknown> = { ...base }
  for (const f of fields) {
    if (!isVisible(f, draft)) {
      candidate[f.key] = f.hiddenValue
      continue
    }
    const parsed = fromDraftValue(f, draft[f.key] ?? toDraftValue(f, undefined))
    if (parsed.ok) candidate[f.key] = parsed.value
    else fieldErrors[f.key] = parsed.error
  }
  for (const key of Object.keys(candidate)) if (candidate[key] === undefined) delete candidate[key]

  // Validate even when some fields failed to parse, so every problem is reported at once.
  const result = schema.safeParse(candidate)
  if (result.success) {
    return Object.keys(fieldErrors).length > 0 ? { fieldErrors, formErrors: [] } : { value: result.data, fieldErrors, formErrors: [] }
  }
  const formErrors: string[] = []
  const visibleKeys = new Set(fields.filter((f) => isVisible(f, draft)).map((f) => f.key))
  for (const issue of result.error.issues) {
    const unparsed = fieldErrors[String(issue.path[0] ?? '')] !== undefined
    if (unparsed) continue
    const key = String(issue.path[0] ?? '')
    if (visibleKeys.has(key) && !fieldErrors[key]) fieldErrors[key] = issue.message
    else if (!visibleKeys.has(key)) formErrors.push(key ? `${key}: ${issue.message}` : issue.message)
  }
  return { fieldErrors, formErrors }
}
