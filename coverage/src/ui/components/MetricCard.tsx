import type { ReactNode } from 'react'
import { RAG_LABEL, type Rag } from '../lib/rag'

const STATUS_STYLE: Record<Rag, { border: string; pill: string; icon: string }> = {
  green: { border: 'border-l-[#0ca30c]', pill: 'bg-emerald-50 text-emerald-800 ring-emerald-200', icon: '✓' },
  amber: { border: 'border-l-[#fab219]', pill: 'bg-amber-50 text-amber-900 ring-amber-200', icon: '!' },
  red: { border: 'border-l-[#d03b3b]', pill: 'bg-red-50 text-red-800 ring-red-200', icon: '✕' },
}

/** Status is carried by icon and label as well as colour, never colour alone. */
export function StatusPill({ status }: { status: Rag }) {
  const s = STATUS_STYLE[status]
  return (
    <span className={`inline-flex shrink-0 items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium whitespace-nowrap ring-1 ${s.pill}`}>
      <span aria-hidden="true">{s.icon}</span>
      {RAG_LABEL[status]}
    </span>
  )
}

interface MetricCardProps {
  label: string
  value: string
  detail?: ReactNode
  status?: Rag
  threshold?: string
  hero?: boolean
}

export function MetricCard({ label, value, detail, status, threshold, hero }: MetricCardProps) {
  return (
    <div className={`card flex flex-col gap-1 p-4 ${status ? `border-l-4 ${STATUS_STYLE[status].border}` : ''}`}>
      <div className="flex items-start justify-between gap-2">
        <h3 className="text-sm text-slate-600">{label}</h3>
        {status && <StatusPill status={status} />}
      </div>
      <div className={`font-semibold text-slate-900 ${hero ? 'text-5xl' : 'text-2xl'}`}>{value}</div>
      {detail && <div className="text-sm text-slate-600">{detail}</div>}
      {threshold && <div className="mt-auto pt-1 text-xs text-slate-400">{threshold}</div>}
    </div>
  )
}
