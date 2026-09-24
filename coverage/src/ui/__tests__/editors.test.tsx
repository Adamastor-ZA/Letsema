// @vitest-environment jsdom
import 'fake-indexeddb/auto'
import { cleanup, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { db } from '../../db/db'
import { clearAllData, getSettings, loadSampleData, readDataset, updateSettings } from '../../db/repo'
import { App } from '../App'

async function open(route: string) {
  window.location.hash = `#/${route}`
  render(<App />)
  await screen.findByRole('heading', { level: 1 })
}

const dialog = () => screen.getByRole('dialog')

beforeEach(async () => {
  await clearAllData()
  await updateSettings({ asOfMonth: '2026-09' })
})

afterEach(() => cleanup())

describe('asset editor', () => {
  it('adds an asset after fixing validation errors', async () => {
    const user = userEvent.setup()
    await open('assets')
    await user.click(screen.getByRole('button', { name: '+ Add asset' }))

    await user.click(within(dialog()).getByRole('button', { name: 'Add asset' }))
    expect(within(dialog()).getByText('Give it a name')).toBeInTheDocument()
    expect(within(dialog()).getByText('Enter an amount')).toBeInTheDocument()

    await user.type(within(dialog()).getByLabelText('Name'), 'Money market')
    await user.type(within(dialog()).getByLabelText('Current value'), '180 000,50')
    await user.clear(within(dialog()).getByLabelText('Expected annual growth'))
    await user.type(within(dialog()).getByLabelText('Expected annual growth'), '7.5')
    await user.click(within(dialog()).getByRole('button', { name: 'Add asset' }))

    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    const [asset] = (await readDataset()).assets
    expect(asset).toMatchObject({ name: 'Money market', tier: 'T1', valueCents: 18_000_050, growthBps: 750, sortOrder: 0 })
    expect(asset!.haircutBps).toBeUndefined()
    expect(await screen.findByText('Money market')).toBeInTheDocument()
  })

  it('reveals tier-specific fields and stores them', async () => {
    const user = userEvent.setup()
    await open('assets')
    await user.click(screen.getByRole('button', { name: '+ Add asset' }))
    expect(within(dialog()).queryByLabelText('Accessible amount')).not.toBeInTheDocument()

    await user.selectOptions(within(dialog()).getByLabelText('Liquidity tier'), 'T3')
    await user.type(within(dialog()).getByLabelText('Name'), 'Retirement annuity')
    await user.type(within(dialog()).getByLabelText('Current value'), '1000')
    await user.clear(within(dialog()).getByLabelText('Accessible amount'))
    await user.type(within(dialog()).getByLabelText('Accessible amount'), '2000')
    await user.click(within(dialog()).getByRole('button', { name: 'Add asset' }))
    expect(within(dialog()).getByText('Cannot exceed the current value')).toBeInTheDocument()

    await user.clear(within(dialog()).getByLabelText('Accessible amount'))
    await user.type(within(dialog()).getByLabelText('Accessible amount'), '500')
    await user.clear(within(dialog()).getByLabelText('Haircut on liquidation'))
    await user.type(within(dialog()).getByLabelText('Haircut on liquidation'), '30')
    await user.click(within(dialog()).getByRole('button', { name: 'Add asset' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect((await readDataset()).assets[0]).toMatchObject({ tier: 'T3', valueCents: 100_000, accessibleCents: 50_000, haircutBps: 3_000 })
  })

  it('edits, reorders and deletes', async () => {
    const user = userEvent.setup()
    await loadSampleData('2026-09')
    await open('assets')

    await user.click(await screen.findByRole('button', { name: 'Edit Everyday account (sample)' }))
    const name = within(dialog()).getByLabelText('Name')
    await user.clear(name)
    await user.type(name, 'Cheque account')
    await user.click(within(dialog()).getByRole('button', { name: 'Save changes' }))
    expect(await screen.findByText('Cheque account')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Move Money market fund (sample) up' }))
    await waitFor(async () => expect((await readDataset()).assets.slice(0, 2).map((a) => a.name)).toEqual(['Money market fund (sample)', 'Cheque account']))

    await user.click(screen.getByRole('button', { name: 'Delete Money market fund (sample)' }))
    await user.click(within(dialog()).getByRole('button', { name: 'Delete' }))
    await waitFor(async () => expect((await readDataset()).assets.some((a) => a.name.startsWith('Money market'))).toBe(false))
    // It was the sweep target.
    expect((await getSettings()).sweepAssetId).toBeNull()
  })

  it('closes the form on Escape without saving', async () => {
    const user = userEvent.setup()
    await open('assets')
    await user.click(screen.getByRole('button', { name: '+ Add asset' }))
    await user.type(within(dialog()).getByLabelText('Name'), 'Draft')
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(await db.assets.count()).toBe(0)
  })
})

describe('debt editor', () => {
  it('warns about a balloon while editing and hides the fixed rate for variable debt', async () => {
    const user = userEvent.setup()
    await open('debts')
    await user.click(screen.getByRole('button', { name: '+ Add debt' }))
    expect(within(dialog()).queryByLabelText('Interest rate')).not.toBeInTheDocument()
    expect(within(dialog()).getByText(/Prime is 10.5%/)).toBeInTheDocument()

    await user.selectOptions(within(dialog()).getByLabelText('Rate type'), 'fixed')
    await user.type(within(dialog()).getByLabelText('Name'), 'Car')
    await user.type(within(dialog()).getByLabelText('Outstanding balance'), '100000')
    await user.type(within(dialog()).getByLabelText('Monthly instalment'), '1000')
    await user.clear(within(dialog()).getByLabelText('Interest rate'))
    await user.type(within(dialog()).getByLabelText('Interest rate'), '0')
    // Default final month is 60 months out. After 60 payments of R1 000, the final month's payment is R40 000:
    // the R1 000 instalment plus a R39 000 balloon.
    expect(within(dialog()).getByText(/Balloon of R\s?39\s?000 due in Sep 2031/)).toBeInTheDocument()
    await user.click(within(dialog()).getByRole('button', { name: 'Add debt' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect((await readDataset()).debts[0]).toMatchObject({ rateType: 'fixed', fixedRateBps: 0, primeMarginBps: 0, endMonth: '2031-09' })
  })
})

describe('income editor', () => {
  it('uses a single month for annual income and toggles for irregular income', async () => {
    const user = userEvent.setup()
    await open('incomes')
    await user.click(screen.getByRole('button', { name: '+ Add income stream' }))
    await user.type(within(dialog()).getByLabelText('Name'), 'Bonus')
    await user.type(within(dialog()).getByLabelText('Amount per payment, after tax'), '50000')
    await user.selectOptions(within(dialog()).getByLabelText('Confidence'), 'variable')

    await user.selectOptions(within(dialog()).getByLabelText('Frequency'), 'annual')
    await user.click(within(dialog()).getByRole('button', { name: 'Add income stream' }))
    expect(within(dialog()).getByText('Choose the one month it is paid')).toBeInTheDocument()
    await user.selectOptions(within(dialog()).getByLabelText('Paid in'), '3')
    await user.click(within(dialog()).getByRole('button', { name: 'Add income stream' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect((await readDataset()).incomes[0]).toMatchObject({ frequency: 'annual', months: [3], confidence: 'variable', amountCents: 5_000_000 })

    await user.click(screen.getByRole('button', { name: '+ Add income stream' }))
    await user.type(within(dialog()).getByLabelText('Name'), 'Consulting')
    await user.type(within(dialog()).getByLabelText('Amount per payment, after tax'), '10000')
    await user.selectOptions(within(dialog()).getByLabelText('Frequency'), 'irregular')
    for (const m of ['Oct', 'Apr', 'Jul']) await user.click(within(dialog()).getByRole('button', { name: m }))
    await user.click(within(dialog()).getByRole('button', { name: 'Add income stream' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect((await readDataset()).incomes[1]).toMatchObject({ frequency: 'irregular', months: [4, 7, 10] })
  })
})

describe('obligation editor', () => {
  it('rejects an end month before the start month', async () => {
    const user = userEvent.setup()
    await open('obligations')
    await user.click(screen.getByRole('button', { name: '+ Add obligation' }))
    await user.type(within(dialog()).getByLabelText('Name'), 'Fees')
    await user.type(within(dialog()).getByLabelText('Amount'), '1000')
    const end = within(dialog()).getByLabelText(/Ends/)
    await user.type(end, '2025-01')
    await user.click(within(dialog()).getByRole('button', { name: 'Add obligation' }))
    expect(within(dialog()).getByText('End month is before the start month')).toBeInTheDocument()
  })
})

describe('assumptions and data', () => {
  it('saves assumptions and validates the horizon', async () => {
    const user = userEvent.setup()
    await loadSampleData('2026-09')
    await open('assumptions')
    const horizon = screen.getByLabelText('Projection horizon')
    await user.clear(horizon)
    await user.type(horizon, '31')
    await user.click(screen.getByRole('button', { name: 'Save assumptions' }))
    expect(screen.getByText('At most 30 years')).toBeInTheDocument()

    await user.clear(horizon)
    await user.type(horizon, '20')
    await user.selectOptions(screen.getByLabelText('Sweep surpluses into'), '')
    await user.click(screen.getByRole('button', { name: 'Save assumptions' }))
    expect(await screen.findByText('Assumptions saved.')).toBeInTheDocument()
    expect(await getSettings()).toMatchObject({ horizonYears: 20, sweepAssetId: null })
  })

  it('loads sample data and clears everything behind a typed confirmation', async () => {
    const user = userEvent.setup()
    await open('data')
    await user.click(screen.getByRole('button', { name: 'Load sample data' }))
    await user.click(within(dialog()).getByRole('button', { name: 'Load sample data' }))
    expect(await screen.findByText(/Sample data loaded/)).toBeInTheDocument()
    expect((await readDataset()).assets.length).toBeGreaterThan(0)

    await user.click(screen.getByRole('button', { name: 'Clear all data' }))
    const confirm = within(dialog()).getByRole('button', { name: 'Clear everything' })
    expect(confirm).toBeDisabled()
    await user.type(within(dialog()).getByRole('textbox'), 'clear')
    await user.click(confirm)
    expect(await screen.findByText('All data cleared.')).toBeInTheDocument()
    expect((await readDataset()).assets).toEqual([])
  })
})
