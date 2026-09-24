// @vitest-environment jsdom
import 'fake-indexeddb/auto'
import { cleanup, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { evaluate } from '../../engine/evaluate'
import { resolveOverrides } from '../../engine/scenarios'
import { clearAllData, loadSampleData, readDataset } from '../../db/repo'
import { datasetToInputs } from '../../schema/dataset'
import { App } from '../App'

async function open(route: string) {
  window.location.hash = `#/${route}`
  render(<App />)
  await screen.findByRole('heading', { level: 1 })
}

const comparison = () => screen.getByRole('table', { name: /Headline metrics for the base case/ })
const columnHeaders = () => within(comparison()).getAllByRole('columnheader').map((h) => h.textContent)

beforeEach(async () => {
  await clearAllData()
  await loadSampleData('2026-09')
})
afterEach(() => cleanup())

describe('scenarios page', () => {
  it('compares the default scenarios side by side with base', async () => {
    await open('scenarios')
    await screen.findByRole('heading', { name: 'Side by side' })
    expect(columnHeaders()).toEqual(['Metric', 'Base case', 'Rate shock', 'Variable income down 40%', 'Cost escalation', 'Combined stress'])

    const d = await readDataset()
    const inputs = datasetToInputs(d)
    const combined = evaluate(inputs, resolveOverrides(d.scenarios.find((s) => s.name === 'Combined stress')!)).metrics
    const coverageRow = within(comparison()).getByRole('rowheader', { name: '12-month coverage ratio' }).closest('tr')!
    const cells = within(coverageRow).getAllByRole('cell')
    expect(cells[4]).toHaveTextContent(`${combined.coverage.ratio!.toFixed(2)}×`)
    expect(cells[0]).not.toHaveTextContent('▼')
    expect(cells[4]).toHaveTextContent('▼')
  })

  it('drops a scenario from the comparison when unticked', async () => {
    const user = userEvent.setup()
    await open('scenarios')
    await screen.findByRole('heading', { name: 'Side by side' })
    await user.click(screen.getByRole('checkbox', { name: 'Compare Rate shock' }))
    await waitFor(() => expect(columnHeaders()).not.toContain('Rate shock'))
    expect((await readDataset()).scenarios.find((s) => s.name === 'Rate shock')?.active).toBe(false)
  })

  it('creates a custom scenario with adjustments, exclusions and an extra event', async () => {
    const user = userEvent.setup()
    await open('scenarios')
    await user.click(await screen.findByRole('button', { name: '+ New scenario' }))
    const dialog = screen.getByRole('dialog')

    await user.click(within(dialog).getByRole('button', { name: 'Create scenario' }))
    expect(within(dialog).getByText('Give the scenario a name')).toBeInTheDocument()
    expect(within(dialog).getByText(/changes nothing yet/)).toBeInTheDocument()

    await user.type(within(dialog).getByRole('textbox', { name: 'Name' }), 'Retrenched')
    await user.type(within(dialog).getByRole('textbox', { name: 'Committed income (%)' }), '-100')
    await user.type(within(dialog).getByRole('textbox', { name: 'Prime rate (points)' }), '1.5')
    await user.type(within(dialog).getByRole('textbox', { name: 'Haircuts (points)' }), 'lots')
    await user.click(within(dialog).getByRole('checkbox', { name: 'Flatlet rental (sample)' }))
    await user.click(within(dialog).getByRole('checkbox', { name: /^Rate shock/ }))
    await user.click(within(dialog).getByRole('button', { name: '+ Add event' }))
    await user.type(within(dialog).getByRole('textbox', { name: 'Event 1 name' }), 'Severance')
    await user.type(within(dialog).getByRole('textbox', { name: 'Event 1 amount' }), '150000')
    await user.selectOptions(within(dialog).getByRole('combobox', { name: 'Event 1 direction' }), 'inflow')

    await user.click(within(dialog).getByRole('button', { name: 'Create scenario' }))
    expect(within(dialog).getByText('Enter a percentage, e.g. 7.5')).toBeInTheDocument()
    await user.clear(within(dialog).getByRole('textbox', { name: 'Haircuts (points)' }))
    await user.click(within(dialog).getByRole('button', { name: 'Create scenario' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())

    const saved = (await readDataset()).scenarios.find((s) => s.name === 'Retrenched')!
    expect(saved).toMatchObject({
      presets: ['rateShock'],
      active: true,
      slot: 5,
      custom: { committedIncomeFactor: 0, primeDeltaBps: 150, excludedIds: ['sample-rental'] },
    })
    expect(saved.custom.extraEvents).toEqual([
      expect.objectContaining({ name: 'Severance', month: '2026-09', amountCents: 15_000_000, direction: 'inflow' }),
    ])
    // The rate-shock preset (+2) and the custom +1.5 combine.
    expect(await screen.findByText(/^Prime \+3.5 points, variable-rate instalments recalculated\. No committed income\. Leaves out Flatlet rental \(sample\)\. Adds Severance/)).toBeInTheDocument()
    await waitFor(() => expect(columnHeaders()).toContain('Retrenched'))
  })

  it('edits an existing scenario, keeping its colour slot', async () => {
    const user = userEvent.setup()
    await open('scenarios')
    await user.click(await screen.findByRole('button', { name: 'Edit Cost escalation' }))
    const dialog = screen.getByRole('dialog')
    const input = within(dialog).getByRole('textbox', { name: 'Obligation escalation (points a year)' })
    await user.type(input, '2')
    await user.click(within(dialog).getByRole('button', { name: 'Save scenario' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    const saved = (await readDataset()).scenarios.find((s) => s.name === 'Cost escalation')!
    expect(saved).toMatchObject({ slot: 3, presets: ['costEscalation'], custom: { obligationEscalationDeltaBps: 200 } })
    expect(screen.getByText('Obligations escalate +5 points a year.')).toBeInTheDocument()
  })

  it('deletes a scenario and restores the standard ones', async () => {
    const user = userEvent.setup()
    await open('scenarios')
    await user.click(await screen.findByRole('button', { name: 'Delete Rate shock' }))
    await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Delete' }))
    await waitFor(async () => expect((await readDataset()).scenarios).toHaveLength(3))
    await user.click(await screen.findByRole('button', { name: 'Restore the standard stress scenarios' }))
    expect(await screen.findByText('Restored 1 standard scenario.')).toBeInTheDocument()
    expect((await readDataset()).scenarios.map((s) => s.name)).toContain('Rate shock')
  })
})

describe('dashboard stress tests', () => {
  it('lists the base case and each compared scenario', async () => {
    await open('dashboard')
    const card = await screen.findByRole('region', { name: 'Stress tests' })
    const names = within(card)
      .getAllByRole('rowheader')
      .map((r) => r.textContent)
    expect(names).toEqual(['Base case', 'Rate shock', 'Variable income down 40%', 'Cost escalation', 'Combined stress'])
  })
})
