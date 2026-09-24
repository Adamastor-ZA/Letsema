// @vitest-environment jsdom
import 'fake-indexeddb/auto'
import { cleanup, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { evaluate } from '../../engine/evaluate'
import { clearAllData, getSettings, loadSampleData, readDataset } from '../../db/repo'
import { datasetToInputs } from '../../schema/dataset'
import { App } from '../App'

async function open(route: string) {
  window.location.hash = `#/${route}`
  render(<App />)
  await screen.findByRole('heading', { level: 1 })
}

const card = (label: string) => screen.getByRole('heading', { name: label, level: 3 }).closest('.card') as HTMLElement

beforeEach(async () => {
  await clearAllData()
  await loadSampleData('2026-09')
})
afterEach(() => cleanup())

describe('dashboard', () => {
  it('shows a getting-started prompt when there is no data', async () => {
    await clearAllData()
    await open('dashboard')
    expect(await screen.findByText('Start by describing your position')).toBeInTheDocument()
  })

  it('shows the engine metrics with their status', async () => {
    await open('dashboard')
    await screen.findByText('12-month coverage ratio')
    const m = evaluate(datasetToInputs(await readDataset())).metrics

    const coverage = card('12-month coverage ratio')
    expect(within(coverage).getByText(`${m.coverage.ratio!.toFixed(2)}×`)).toBeInTheDocument()
    expect(within(coverage).getByText('On track')).toBeInTheDocument()

    expect(within(card('First shortfall, base case')).getByText('None in horizon')).toBeInTheDocument()
    const allStops = card('Runway if all income stops')
    expect(within(allStops).getByText(`${m.runwayAllIncomeStops.months} months`)).toBeInTheDocument()
    expect(within(allStops).getByText('Watch')).toBeInTheDocument()
    expect(screen.getByText(/No shortfall before Aug 2036/)).toBeInTheDocument()
  })

  it('re-bands statuses when thresholds change, and validates them', async () => {
    const user = userEvent.setup()
    await open('dashboard')
    await screen.findByText('12-month coverage ratio')
    await user.click(screen.getByRole('button', { name: 'Status thresholds' }))
    const dialog = screen.getByRole('dialog')
    const green = within(dialog).getByLabelText('12-month coverage ratio, green threshold')
    const amber = within(dialog).getByLabelText('12-month coverage ratio, amber threshold')

    await user.clear(green)
    await user.type(green, '1')
    await user.clear(amber)
    await user.type(amber, '2')
    await user.click(within(dialog).getByRole('button', { name: 'Save thresholds' }))
    expect(within(dialog).getByText(/Green must be at least amber/)).toBeInTheDocument()

    await user.clear(green)
    await user.type(green, '3')
    await user.click(within(dialog).getByRole('button', { name: 'Save thresholds' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect((await getSettings()).thresholds.coverageRatio).toEqual({ green: 3, amber: 2 })
    await waitFor(() => expect(within(card('12-month coverage ratio')).getByText('Act')).toBeInTheDocument())
  })

  it('reports the first shortfall when there is one', async () => {
    const d = await readDataset()
    // Remove every income stream: the household runs short.
    const { db } = await import('../../db/db')
    await db.incomes.clear()
    const m = evaluate(datasetToInputs({ ...d, incomes: [] })).metrics
    await open('dashboard')
    const first = await screen.findByRole('heading', { name: 'First shortfall, base case', level: 3 })
    const month = m.firstShortfall.month!
    const [y, mm] = month.split('-')
    const label = `${['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][Number(mm) - 1]} ${y}`
    expect(within(first.closest('.card') as HTMLElement).getByText(label)).toBeInTheDocument()
    expect(screen.getByText(/Liquid assets run out in/)).toBeInTheDocument()
  })
})

describe('next 12 months', () => {
  it('lists twelve months and itemises a month on request', async () => {
    const user = userEvent.setup()
    await open('next12')
    const table = await screen.findByRole('table')
    const monthButtons = within(table).getAllByRole('button', { expanded: false })
    expect(monthButtons).toHaveLength(12)
    expect(monthButtons[0]).toHaveTextContent('Sep 2026')
    expect(monthButtons[11]).toHaveTextContent('Aug 2027')

    await user.click(within(table).getByRole('button', { name: /Jan 2027/ }))
    expect(within(table).getByRole('button', { name: /Jan 2027/ })).toHaveAttribute('aria-expanded', 'true')
    expect(within(table).getByText('School fees, two children (sample)')).toBeInTheDocument()
    // January (school fees) and June (renovation) draw on savings.
    expect(within(table).getAllByText(/Draws R/)).toHaveLength(2)
  })

  it('switches to real terms from the page', async () => {
    const user = userEvent.setup()
    await open('next12')
    await user.click(await screen.findByRole('button', { name: "Today's money" }))
    await waitFor(async () => expect((await getSettings()).display).toBe('real'))
  })
})

describe('projection', () => {
  it('offers a table view for each chart', async () => {
    const user = userEvent.setup()
    await open('projection')
    const netWorth = await screen.findByRole('region', { name: 'Net worth by tier' })
    await user.click(within(netWorth).getByRole('button', { name: 'table' }))
    const rows = within(within(netWorth).getByRole('table')).getAllByRole('row')
    // Header, "Now", then one row per year of a 10-year horizon.
    expect(rows).toHaveLength(12)
    expect(within(rows[1]!).getByRole('rowheader')).toHaveTextContent('Now')

    const liquid = screen.getByRole('region', { name: 'Liquid balance' })
    await user.click(within(liquid).getByRole('button', { name: 'table' }))
    expect(within(within(liquid).getByRole('table')).getAllByRole('row')).toHaveLength(121)
  })
})
