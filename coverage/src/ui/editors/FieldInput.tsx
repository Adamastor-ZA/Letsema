import { useId } from 'react'
import { MONTH_NAMES, MONTH_SHORT, type Draft, type DraftValue, type FieldDef } from './fields'

interface FieldInputProps {
  field: FieldDef
  draft: Draft
  value: DraftValue
  error?: string
  onChange: (value: DraftValue) => void
}

export function FieldInput({ field, draft, value, error, onChange }: FieldInputProps) {
  const id = useId()
  const help = typeof field.help === 'function' ? field.help(draft) : field.help
  const helpId = `${id}-help`
  const errorId = `${id}-error`
  const describedBy = [help ? helpId : null, error ? errorId : null].filter(Boolean).join(' ') || undefined
  const common = { id, 'aria-invalid': error ? true : undefined, 'aria-describedby': describedBy } as const
  const text = typeof value === 'string' ? value : ''

  let control
  switch (field.kind) {
    case 'select':
    case 'calendarMonth':
      control = (
        <select {...common} className="input" value={text} onChange={(e) => onChange(e.target.value)}>
          {(field.kind === 'select' ? field.options ?? [] : MONTH_NAMES.map((label, i) => ({ value: String(i + 1), label }))).map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
      )
      break
    case 'calendarMonths': {
      const months = Array.isArray(value) ? value : []
      if (field.single?.(draft)) {
        control = (
          <select {...common} className="input" value={String(months[0] ?? '')} onChange={(e) => onChange(e.target.value ? [Number(e.target.value)] : [])}>
            <option value="">Choose a month</option>
            {MONTH_NAMES.map((label, i) => (
              <option key={label} value={String(i + 1)}>
                {label}
              </option>
            ))}
          </select>
        )
      } else {
        control = (
          <div role="group" aria-labelledby={`${id}-label`} aria-describedby={describedBy} className="grid grid-cols-6 gap-1">
            {MONTH_SHORT.map((label, i) => {
              const m = i + 1
              const on = months.includes(m)
              return (
                <button
                  key={label}
                  type="button"
                  aria-pressed={on}
                  className={`rounded border px-1 py-1 text-xs ${on ? 'border-brand-700 bg-brand-700 text-white' : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'}`}
                  onClick={() => onChange(on ? months.filter((x) => x !== m) : [...months, m])}
                >
                  {label}
                </button>
              )
            })}
          </div>
        )
      }
      break
    }
    case 'checkbox':
      return (
        <div className={field.wide ? 'sm:col-span-2' : undefined}>
          <label className="flex items-start gap-2 text-sm">
            <input
              {...common}
              type="checkbox"
              className="mt-0.5 size-4 accent-brand-700"
              checked={value === true}
              onChange={(e) => onChange(e.target.checked)}
            />
            <span>
              <span className="font-medium text-slate-800">{field.label}</span>
              {help && (
                <span id={helpId} className="block text-xs text-slate-500">
                  {help}
                </span>
              )}
            </span>
          </label>
        </div>
      )
    case 'month':
    case 'optionalMonth':
      control = (
        <input
          {...common}
          type="month"
          className="input"
          placeholder="YYYY-MM"
          value={text}
          min="1900-01"
          max="2150-12"
          onChange={(e) => onChange(e.target.value)}
        />
      )
      break
    default: {
      const numeric = field.kind === 'money' || field.kind === 'percent' || field.kind === 'integer'
      control = (
        <div className="relative">
          <input
            {...common}
            type="text"
            className={`input ${numeric ? 'tabular-nums' : ''} ${field.suffix ? 'pr-10' : ''}`}
            inputMode={numeric ? (field.allowNegative ? 'text' : 'decimal') : undefined}
            autoComplete="off"
            placeholder={field.placeholder}
            value={text}
            onChange={(e) => onChange(e.target.value)}
          />
          {field.suffix && <span className="pointer-events-none absolute inset-y-0 right-2.5 flex items-center text-sm text-slate-400">{field.suffix}</span>}
        </div>
      )
    }
  }

  return (
    <div className={field.wide ? 'sm:col-span-2' : undefined}>
      <label id={`${id}-label`} htmlFor={id} className="mb-1 block text-sm font-medium text-slate-800">
        {field.label}
        {field.kind === 'optionalMonth' && <span className="font-normal text-slate-500"> (optional)</span>}
      </label>
      {control}
      {help && (
        <p id={helpId} className="mt-1 text-xs text-slate-500">
          {help}
        </p>
      )}
      {error && (
        <p id={errorId} className="mt-1 text-xs font-medium text-red-700">
          {error}
        </p>
      )}
    </div>
  )
}
