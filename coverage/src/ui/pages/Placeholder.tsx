import { href, type NavItem } from '../routes'
import type { EditorContext } from '../editors/types'

export function Placeholder({ item, ctx }: { item: NavItem; ctx: EditorContext }) {
  const d = ctx.dataset
  const empty = d.assets.length + d.debts.length + d.obligations.length + d.incomes.length + d.events.length === 0
  return (
    <section className="max-w-2xl space-y-4">
      <h1 className="text-xl font-semibold">{item.label}</h1>
      <div className="card space-y-3 p-5 text-sm text-slate-700">
        <p>This screen arrives in Phase {item.phase}.</p>
        {empty ? (
          <p>
            Start by adding your <a className="text-brand-700 underline" href={href('assets')}>assets</a>, or load the fictional{' '}
            <a className="text-brand-700 underline" href={href('data')}>sample data</a> to explore.
          </p>
        ) : (
          <p>
            The model holds {d.assets.length} assets, {d.debts.length} debts, {d.obligations.length} obligations, {d.incomes.length} income streams
            and {d.events.length} one-off events, as of {ctx.fmt.month(d.settings.asOfMonth)}.
          </p>
        )}
      </div>
    </section>
  )
}
