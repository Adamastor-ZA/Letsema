import { updateSettings } from '../../db/repo'
import type { Settings } from '../../schema/settings'

/** Switch between nominal and real (CPI-deflated) amounts; stored with the assumptions. */
export function DisplayToggle({ settings }: { settings: Settings }) {
  return (
    <div role="group" aria-label="Amounts in" className="inline-flex rounded-md border border-slate-300 bg-white p-0.5 text-xs">
      {(
        [
          ['nominal', 'Nominal'],
          ['real', "Today's money"],
        ] as const
      ).map(([mode, label]) => (
        <button
          key={mode}
          type="button"
          aria-pressed={settings.display === mode}
          className={`rounded px-2 py-1 ${settings.display === mode ? 'bg-slate-800 text-white' : 'text-slate-600 hover:bg-slate-100'}`}
          onClick={() => updateSettings({ display: mode })}
        >
          {label}
        </button>
      ))}
    </div>
  )
}
