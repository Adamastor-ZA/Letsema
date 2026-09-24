import type { ReactNode } from 'react'

const tones = {
  info: 'border-sky-200 bg-sky-50 text-sky-900',
  warn: 'border-amber-200 bg-amber-50 text-amber-900',
  error: 'border-red-200 bg-red-50 text-red-900',
}

export function Notice({ tone = 'info', children }: { tone?: keyof typeof tones; children: ReactNode }) {
  return <div className={`rounded-md border px-3 py-2 text-sm ${tones[tone]}`}>{children}</div>
}

export function Badge({ children, tone = 'slate' }: { children: ReactNode; tone?: 'slate' | 'brand' | 'amber' | 'red' | 'green' }) {
  const cls = {
    slate: 'bg-slate-100 text-slate-700',
    brand: 'bg-brand-100 text-brand-800',
    amber: 'bg-amber-100 text-amber-800',
    red: 'bg-red-100 text-red-800',
    green: 'bg-emerald-100 text-emerald-800',
  }[tone]
  return <span className={`inline-flex items-center rounded px-1.5 py-0.5 text-xs font-medium whitespace-nowrap ${cls}`}>{children}</span>
}
