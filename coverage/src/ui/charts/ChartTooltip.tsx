export interface TooltipRow {
  key: string
  label: string
  value: string
  color: string
  shape: 'line' | 'rect'
}

/** Values lead, labels follow; series keyed by a short stroke (lines) or swatch (bars). */
export function ChartTooltipBox({ title, rows, note }: { title: string; rows: TooltipRow[]; note?: string }) {
  return (
    <div className="min-w-44 rounded-md border border-slate-200 bg-white px-3 py-2 text-xs shadow-md">
      <div className="mb-1 font-medium text-slate-500">{title}</div>
      <table>
        <tbody>
          {rows.map((r) => (
            <tr key={r.key}>
              <td className="pr-2 align-middle">
                {r.shape === 'line' ? (
                  <span className="block h-0.5 w-3 rounded" style={{ background: r.color }} />
                ) : (
                  <span className="block size-2.5 rounded-sm" style={{ background: r.color }} />
                )}
              </td>
              <td className="pr-3 text-right font-semibold text-slate-900 tabular-nums">{r.value}</td>
              <td className="text-slate-600">{r.label}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {note && <div className="mt-1 text-slate-500">{note}</div>}
    </div>
  )
}
