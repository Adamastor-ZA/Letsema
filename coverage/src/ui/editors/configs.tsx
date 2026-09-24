import { debtOutlook } from '../../engine/diagnostics'
import { debtRateBps } from '../../engine/debt'
import { applyBps } from '../../engine/money'
import { addMonths, toIndex } from '../../engine/month'
import type { Tier } from '../../engine/types'
import type { AssetRecord, IncomeRecord, ObligationRecord } from '../../schema/entities'
import { Badge } from '../components/Notice'
import { MONTH_SHORT, type Draft, type FieldDef } from './fields'
import type { EditorContext, EntityConfig, Warning } from './types'

export const TIER_LABELS: Record<Tier, string> = {
  T1: 'T1 Cash',
  T2: 'T2 Investments',
  T3: 'T3 Retirement',
  T4: 'T4 Property / illiquid',
}

const TIER_HELP: Record<Tier, string> = {
  T1: 'Available immediately. Drawn first to cover a shortfall.',
  T2: 'Available within weeks, net of the haircut. Drawn after T1.',
  T3: 'Locked, except for an accessible amount you specify.',
  T4: 'Counts toward net worth, never toward coverage.',
}

const tierTone: Record<Tier, 'green' | 'brand' | 'amber' | 'slate'> = { T1: 'green', T2: 'brand', T3: 'amber', T4: 'slate' }

const is = (key: string, ...values: string[]) => (d: Draft) => values.includes(String(d[key]))
const monthName = (m: number) => MONTH_SHORT[m - 1] ?? String(m)

function horizonEnd(ctx: EditorContext): string {
  return addMonths(ctx.dataset.settings.asOfMonth, ctx.dataset.settings.horizonYears * 12 - 1)
}

/** Items outside the projection window have no effect; say so. */
function windowWarnings(start: string, end: string | null, ctx: EditorContext): Warning[] {
  const asOf = ctx.dataset.settings.asOfMonth
  if (end !== null && toIndex(end) < toIndex(asOf)) return [{ tone: 'warn', text: `Ended before the as-of month (${ctx.fmt.month(asOf)}), so it has no effect.` }]
  if (toIndex(start) > toIndex(horizonEnd(ctx))) return [{ tone: 'warn', text: 'Starts after the projection horizon, so it has no effect.' }]
  return []
}

function period(start: string, end: string | null, ctx: EditorContext): string {
  const asOf = ctx.dataset.settings.asOfMonth
  const from = toIndex(start) <= toIndex(asOf) ? 'Now' : ctx.fmt.month(start)
  return `${from} to ${end ? ctx.fmt.month(end) : 'horizon'}`
}

const todayMoneyHelp = "In today's money. Escalation applies from the as-of month, even if it starts later."

/** Monthly equivalent of an obligation or income stream at its current amount. */
function monthlyEquivalent(r: ObligationRecord | IncomeRecord): number {
  if (r.frequency === 'monthly') return r.amountCents
  if ('months' in r && r.frequency === 'irregular') return Math.round((r.amountCents * r.months.length) / 12)
  return Math.round(r.amountCents / 12)
}

function isActiveAt(r: { startMonth: string; endMonth: string | null }, month: string): boolean {
  return toIndex(r.startMonth) <= toIndex(month) && (r.endMonth === null || toIndex(r.endMonth) >= toIndex(month))
}

function Stat({ label, value, hint }: { label: string; value: string; hint?: string }) {
  return (
    <div className="card px-3 py-2">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="text-base font-semibold tabular-nums">{value}</div>
      {hint && <div className="text-xs text-slate-500">{hint}</div>}
    </div>
  )
}

function StatRow({ children }: { children: React.ReactNode }) {
  return <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">{children}</div>
}

export const assetsConfig: EntityConfig<'assets'> = {
  kind: 'assets',
  title: 'Assets',
  singular: 'asset',
  intro: 'What you own, by how quickly it can be turned into cash. Update the values each month.',
  fields: () => [
    { key: 'name', label: 'Name', kind: 'text', wide: true, placeholder: 'e.g. Money market fund' },
    {
      key: 'tier',
      label: 'Liquidity tier',
      kind: 'select',
      options: (Object.keys(TIER_LABELS) as Tier[]).map((t) => ({ value: t, label: TIER_LABELS[t] })),
      help: (d) => TIER_HELP[d.tier as Tier] ?? '',
      wide: true,
    },
    { key: 'valueCents', label: 'Current value', kind: 'money' },
    {
      key: 'growthBps',
      label: 'Expected annual growth',
      kind: 'percent',
      allowNegative: true,
      suffix: '%',
      help: 'Interest on cash, expected return on investments, negative for a depreciating asset.',
    },
    {
      key: 'haircutBps',
      label: 'Haircut on liquidation',
      kind: 'percent',
      suffix: '%',
      help: 'Tax or penalty lost when you sell or withdraw.',
      visible: is('tier', 'T2', 'T3'),
      defaultDraft: '0',
    },
    {
      key: 'accessibleCents',
      label: 'Accessible amount',
      kind: 'money',
      help: 'The portion you could withdraw, e.g. a two-pot savings component. Held fixed in the projection.',
      visible: is('tier', 'T3'),
      defaultDraft: '0',
    },
  ],
  defaults: () => ({ tier: 'T1', growthBps: 0 }),
  columns: [
    {
      label: 'Name',
      render: (r, ctx) => (
        <span className="font-medium">
          {r.name} {ctx.dataset.settings.sweepAssetId === r.id && <Badge tone="brand">Surplus sweep</Badge>}
        </span>
      ),
    },
    { label: 'Tier', render: (r) => <Badge tone={tierTone[r.tier]}>{TIER_LABELS[r.tier]}</Badge> },
    { label: 'Value', numeric: true, render: (r, ctx) => ctx.fmt.money(r.valueCents) },
    { label: 'Growth', numeric: true, secondary: true, render: (r, ctx) => ctx.fmt.percent(r.growthBps) },
    {
      label: 'Liquidity',
      secondary: true,
      render: (r, ctx) =>
        r.tier === 'T2'
          ? `${ctx.fmt.percent(r.haircutBps ?? 0)} haircut`
          : r.tier === 'T3'
            ? `${ctx.fmt.money(r.accessibleCents ?? 0)} accessible, ${ctx.fmt.percent(r.haircutBps ?? 0)} haircut`
            : r.tier === 'T1'
              ? 'Immediate'
              : 'Not available',
    },
  ],
  summary: (records, ctx) => {
    const tier = (t: Tier) => records.filter((r) => r.tier === t)
    const total = (rs: AssetRecord[]) => rs.reduce((s, r) => s + r.valueCents, 0)
    const t2Net = tier('T2').reduce((s, r) => s + r.valueCents - applyBps(r.valueCents, r.haircutBps ?? 0), 0)
    return (
      <StatRow>
        <Stat label="T1 Cash" value={ctx.fmt.money(total(tier('T1')))} />
        <Stat label="T2 Investments" value={ctx.fmt.money(total(tier('T2')))} hint={`${ctx.fmt.money(t2Net)} after haircut`} />
        <Stat label="T3 Retirement" value={ctx.fmt.money(total(tier('T3')))} />
        <Stat label="T4 Property / illiquid" value={ctx.fmt.money(total(tier('T4')))} />
      </StatRow>
    )
  },
  warnings: (r) => (r.tier === 'T3' && (r.accessibleCents ?? 0) === 0 ? [{ tone: 'info', text: 'Fully locked: counts toward net worth only.' }] : []),
  reorder: 'Shortfalls draw on T1 assets in this order, then T2 assets in this order.',
}

export const debtsConfig: EntityConfig<'debts'> = {
  kind: 'debts',
  title: 'Debts',
  singular: 'debt',
  intro: 'Loans and credit, amortised monthly. Variable-rate debt follows the prime rate in your assumptions.',
  fields: (ctx) => [
    { key: 'name', label: 'Name', kind: 'text', wide: true, placeholder: 'e.g. Home loan' },
    { key: 'balanceCents', label: 'Outstanding balance', kind: 'money' },
    { key: 'instalmentCents', label: 'Monthly instalment', kind: 'money' },
    {
      key: 'rateType',
      label: 'Rate type',
      kind: 'select',
      options: [
        { value: 'variable', label: 'Variable (linked to prime)' },
        { value: 'fixed', label: 'Fixed' },
      ],
    },
    { key: 'fixedRateBps', label: 'Interest rate', kind: 'percent', suffix: '%', visible: is('rateType', 'fixed'), hiddenValue: 0 },
    {
      key: 'primeMarginBps',
      label: 'Margin over prime',
      kind: 'percent',
      suffix: '%',
      allowNegative: true,
      help: `Prime is ${ctx.fmt.percent(ctx.dataset.settings.primeBps)}. Enter -0.5 for prime less 0.5%.`,
      visible: is('rateType', 'variable'),
      hiddenValue: 0,
    },
    {
      key: 'endMonth',
      label: 'Final payment month',
      kind: 'month',
      help: 'Any balance still outstanding in this month is paid as a balloon.',
    },
  ],
  defaults: (ctx) => ({ rateType: 'variable', primeMarginBps: 0, fixedRateBps: 0, endMonth: addMonths(ctx.dataset.settings.asOfMonth, 60) }),
  columns: [
    { label: 'Name', render: (r) => <span className="font-medium">{r.name}</span> },
    { label: 'Balance', numeric: true, render: (r, ctx) => ctx.fmt.money(r.balanceCents) },
    {
      label: 'Rate',
      numeric: true,
      render: (r, ctx) => {
        const rate = ctx.fmt.percent(debtRateBps(r, ctx.dataset.settings.primeBps))
        if (r.rateType === 'fixed') return `${rate} fixed`
        const m = r.primeMarginBps
        const margin = m === 0 ? 'prime' : `prime ${m > 0 ? '+' : '\u2212'} ${ctx.fmt.percent(Math.abs(m))}`
        return (
          <span>
            {rate} <span className="text-xs text-slate-500">({margin})</span>
          </span>
        )
      },
    },
    { label: 'Instalment', numeric: true, render: (r, ctx) => ctx.fmt.money(r.instalmentCents) },
    { label: 'Final month', secondary: true, render: (r, ctx) => ctx.fmt.month(r.endMonth) },
  ],
  warnings: (r, ctx) => {
    const s = ctx.dataset.settings
    const o = debtOutlook(r, s.primeBps, s.asOfMonth)
    const out: Warning[] = []
    if (o.overdue) out.push({ tone: 'warn', text: 'The final month has passed; the projection settles the balance in the first month.' })
    if (o.negativeAmortisation)
      out.push({
        tone: 'warn',
        text: `The instalment is below the first month's interest (${ctx.fmt.money(o.firstInterestCents)}), so the balance grows.`,
      })
    if (!o.overdue && o.balloonCents > 100) out.push({ tone: 'info', text: `Balloon of ${ctx.fmt.money(o.balloonCents)} due in ${ctx.fmt.month(r.endMonth)}.` })
    if (o.earlyPayoffMonth) out.push({ tone: 'info', text: `Paid off in ${ctx.fmt.month(o.earlyPayoffMonth)}, before the final month.` })
    return out
  },
  summary: (records, ctx) => (
    <StatRow>
      <Stat label="Total outstanding" value={ctx.fmt.money(records.reduce((s, r) => s + r.balanceCents, 0))} />
      <Stat label="Monthly instalments" value={ctx.fmt.money(records.reduce((s, r) => s + r.instalmentCents, 0))} />
    </StatRow>
  ),
}

export const obligationsConfig: EntityConfig<'obligations'> = {
  kind: 'obligations',
  title: 'Obligations',
  singular: 'obligation',
  intro: 'Recurring costs you are committed to: living costs, school fees, medical aid, insurance premiums.',
  fields: () => [
    { key: 'name', label: 'Name', kind: 'text', wide: true, placeholder: 'e.g. Medical aid' },
    {
      key: 'frequency',
      label: 'Frequency',
      kind: 'select',
      options: [
        { value: 'monthly', label: 'Monthly' },
        { value: 'annual', label: 'Annual lump sum' },
      ],
    },
    { key: 'paymentMonth', label: 'Paid in', kind: 'calendarMonth', visible: is('frequency', 'annual'), hiddenValue: 1 },
    { key: 'amountCents', label: 'Amount', kind: 'money', help: todayMoneyHelp, wide: true },
    { key: 'escalationBps', label: 'Annual escalation', kind: 'percent', suffix: '%', allowNegative: true },
    { key: 'escalationMonth', label: 'Escalates in', kind: 'calendarMonth' },
    { key: 'startMonth', label: 'Starts', kind: 'month' },
    { key: 'endMonth', label: 'Ends', kind: 'optionalMonth', help: 'Leave blank if it runs past the horizon.' },
  ],
  defaults: (ctx) => ({
    frequency: 'monthly',
    paymentMonth: 1,
    escalationBps: ctx.dataset.settings.cpiBps,
    escalationMonth: 1,
    startMonth: ctx.dataset.settings.asOfMonth,
    endMonth: null,
  }),
  columns: [
    { label: 'Name', render: (r) => <span className="font-medium">{r.name}</span> },
    {
      label: 'Amount',
      numeric: true,
      render: (r, ctx) => (
        <span>
          {ctx.fmt.money(r.amountCents)}{' '}
          <span className="text-xs text-slate-500">{r.frequency === 'monthly' ? '/ month' : `/ year, ${monthName(r.paymentMonth)}`}</span>
        </span>
      ),
    },
    { label: 'Escalation', secondary: true, render: (r, ctx) => `${ctx.fmt.percent(r.escalationBps)} each ${monthName(r.escalationMonth)}` },
    { label: 'Period', secondary: true, render: (r, ctx) => period(r.startMonth, r.endMonth, ctx) },
  ],
  warnings: (r, ctx) => windowWarnings(r.startMonth, r.endMonth, ctx),
  summary: (records, ctx) => {
    const asOf = ctx.dataset.settings.asOfMonth
    const active = records.filter((r) => isActiveAt(r, asOf))
    return (
      <StatRow>
        <Stat label="Monthly equivalent now" value={ctx.fmt.money(active.reduce((s, r) => s + monthlyEquivalent(r), 0))} hint="Annual items spread over 12 months" />
      </StatRow>
    )
  },
}

export const incomesConfig: EntityConfig<'incomes'> = {
  kind: 'incomes',
  title: 'Income',
  singular: 'income stream',
  intro: 'Money coming in, after tax. Committed income counts toward the coverage ratio; variable income is excluded from it and stress-tested.',
  fields: () => [
    { key: 'name', label: 'Name', kind: 'text', wide: true, placeholder: 'e.g. Salary (net)' },
    {
      key: 'confidence',
      label: 'Confidence',
      kind: 'select',
      options: [
        { value: 'committed', label: 'Committed: contractual or highly reliable' },
        { value: 'variable', label: 'Variable: bonuses, commission, freelance' },
      ],
    },
    {
      key: 'frequency',
      label: 'Frequency',
      kind: 'select',
      options: [
        { value: 'monthly', label: 'Monthly' },
        { value: 'annual', label: 'Annual' },
        { value: 'irregular', label: 'Irregular (specific months)' },
      ],
    },
    {
      key: 'months',
      label: 'Paid in',
      kind: 'calendarMonths',
      visible: is('frequency', 'annual', 'irregular'),
      single: is('frequency', 'annual'),
      hiddenValue: [],
      wide: true,
    },
    { key: 'amountCents', label: 'Amount per payment, after tax', kind: 'money', help: todayMoneyHelp, wide: true },
    { key: 'growthBps', label: 'Annual growth', kind: 'percent', suffix: '%', allowNegative: true },
    { key: 'growthMonth', label: 'Increases in', kind: 'calendarMonth' },
    { key: 'startMonth', label: 'Starts', kind: 'month' },
    { key: 'endMonth', label: 'Ends', kind: 'optionalMonth', help: 'Leave blank if it runs past the horizon.' },
  ],
  defaults: (ctx) => ({
    frequency: 'monthly',
    months: [],
    confidence: 'committed',
    growthBps: ctx.dataset.settings.cpiBps,
    growthMonth: 3,
    startMonth: ctx.dataset.settings.asOfMonth,
    endMonth: null,
  }),
  columns: [
    { label: 'Name', render: (r) => <span className="font-medium">{r.name}</span> },
    {
      label: 'Amount',
      numeric: true,
      render: (r, ctx) => (
        <span>
          {ctx.fmt.money(r.amountCents)}{' '}
          <span className="text-xs text-slate-500">{r.frequency === 'monthly' ? '/ month' : `in ${r.months.map(monthName).join(', ')}`}</span>
        </span>
      ),
    },
    {
      label: 'Confidence',
      render: (r) => <Badge tone={r.confidence === 'committed' ? 'green' : 'amber'}>{r.confidence === 'committed' ? 'Committed' : 'Variable'}</Badge>,
    },
    { label: 'Growth', secondary: true, render: (r, ctx) => `${ctx.fmt.percent(r.growthBps)} each ${monthName(r.growthMonth)}` },
    { label: 'Period', secondary: true, render: (r, ctx) => period(r.startMonth, r.endMonth, ctx) },
  ],
  warnings: (r, ctx) => windowWarnings(r.startMonth, r.endMonth, ctx),
  summary: (records, ctx) => {
    const asOf = ctx.dataset.settings.asOfMonth
    const active = records.filter((r) => isActiveAt(r, asOf))
    const sum = (c: IncomeRecord['confidence']) => active.filter((r) => r.confidence === c).reduce((s, r) => s + monthlyEquivalent(r), 0)
    return (
      <StatRow>
        <Stat label="Committed, monthly equivalent" value={ctx.fmt.money(sum('committed'))} />
        <Stat label="Variable, monthly equivalent" value={ctx.fmt.money(sum('variable'))} />
      </StatRow>
    )
  },
}

export const eventsConfig: EntityConfig<'events'> = {
  kind: 'events',
  title: 'One-off events',
  singular: 'one-off event',
  intro: 'Single known inflows or outflows: a car replacement, a renovation, a policy maturing.',
  fields: () => [
    { key: 'name', label: 'Name', kind: 'text', wide: true, placeholder: 'e.g. Replace car' },
    {
      key: 'direction',
      label: 'Direction',
      kind: 'select',
      options: [
        { value: 'outflow', label: 'Outflow (money out)' },
        { value: 'inflow', label: 'Inflow (money in)' },
      ],
    },
    { key: 'month', label: 'Month', kind: 'month' },
    { key: 'amountCents', label: 'Amount', kind: 'money', help: 'The amount expected in that month, not escalated.' },
  ] satisfies FieldDef[],
  defaults: (ctx) => ({ direction: 'outflow', month: addMonths(ctx.dataset.settings.asOfMonth, 12) }),
  columns: [
    { label: 'Name', render: (r) => <span className="font-medium">{r.name}</span> },
    { label: 'Month', render: (r, ctx) => ctx.fmt.month(r.month) },
    { label: 'Direction', render: (r) => <Badge tone={r.direction === 'inflow' ? 'green' : 'red'}>{r.direction === 'inflow' ? 'Inflow' : 'Outflow'}</Badge> },
    { label: 'Amount', numeric: true, render: (r, ctx) => ctx.fmt.money(r.amountCents) },
  ],
  warnings: (r, ctx) => {
    if (toIndex(r.month) < toIndex(ctx.dataset.settings.asOfMonth)) return [{ tone: 'warn', text: 'Before the as-of month, so it has no effect.' }]
    if (toIndex(r.month) > toIndex(horizonEnd(ctx))) return [{ tone: 'warn', text: 'After the projection horizon, so it has no effect.' }]
    return []
  },
  sort: (a, b) => a.month.localeCompare(b.month) || a.sortOrder - b.sortOrder,
}
