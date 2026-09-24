import { useSyncExternalStore } from 'react'

export type RouteId =
  | 'dashboard'
  | 'projection'
  | 'next12'
  | 'scenarios'
  | 'checkin'
  | 'assets'
  | 'debts'
  | 'obligations'
  | 'incomes'
  | 'events'
  | 'assumptions'
  | 'data'

export interface NavItem {
  id: RouteId
  label: string
  /** Build phase that delivers the screen, while it is still a placeholder. */
  phase?: number
}

export const NAV: { heading: string; items: NavItem[] }[] = [
  {
    heading: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard' },
      { id: 'projection', label: 'Projection' },
      { id: 'next12', label: 'Next 12 months' },
      { id: 'scenarios', label: 'Scenarios' },
      { id: 'checkin', label: 'Monthly check-in', phase: 5 },
    ],
  },
  {
    heading: 'Your data',
    items: [
      { id: 'assets', label: 'Assets' },
      { id: 'debts', label: 'Debts' },
      { id: 'obligations', label: 'Obligations' },
      { id: 'incomes', label: 'Income' },
      { id: 'events', label: 'One-off events' },
    ],
  },
  {
    heading: 'Settings',
    items: [
      { id: 'assumptions', label: 'Assumptions' },
      { id: 'data', label: 'Data' },
    ],
  },
]

const ALL = new Set<string>(NAV.flatMap((g) => g.items.map((i) => i.id)))

function read(): RouteId {
  const id = window.location.hash.replace(/^#\/?/, '')
  return (ALL.has(id) ? id : 'dashboard') as RouteId
}

function subscribe(cb: () => void) {
  window.addEventListener('hashchange', cb)
  return () => window.removeEventListener('hashchange', cb)
}

export function useRoute(): RouteId {
  return useSyncExternalStore(subscribe, read, () => 'dashboard')
}

export const href = (id: RouteId) => `#/${id}`
