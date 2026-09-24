// @vitest-environment jsdom
import 'fake-indexeddb/auto'
import { cleanup, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { buildExport } from '../../db/backup'
import { clearAllData, getSettings, loadSampleData, readDataset, updateSettings } from '../../db/repo'
import { App } from '../App'

async function open(route: string) {
  window.location.hash = `#/${route}`
  render(<App />)
  await screen.findByRole('heading', { level: 1 })
}

beforeEach(async () => {
  await clearAllData()
  await loadSampleData('2026-09')
})
afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})

describe('monthly check-in', () => {
  it('records balances, moves the model forward and starts the history', async () => {
    const user = userEvent.setup()
    await open('checkin')
    expect(screen.getByText(/No check-ins yet/)).toBeInTheDocument()

    await user.clear(screen.getByLabelText('Check-in month'))
    await user.type(screen.getByLabelText('Check-in month'), '2027-02')
    await user.click(screen.getByRole('button', { name: 'Fill with projected values' }))
    const cheque = screen.getByLabelText('Everyday account (sample)')
    await user.clear(cheque)
    await user.type(cheque, '12 345,67')
    // Medical aid's January increase is rolled forward.
    expect(await screen.findByText(/Medical aid \(sample\): R\s?7[\s,]800 to R\s?8[\s,]502/)).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Review and save check-in' }))
    const dialog = screen.getByRole('dialog')
    expect(within(dialog).getByText(/moves from Sep 2026 to Feb 2027/)).toBeInTheDocument()
    await user.click(within(dialog).getByRole('button', { name: 'Save check-in' }))
    expect(await screen.findByText('Checked in for Feb 2027.')).toBeInTheDocument()

    const d = await readDataset()
    expect(d.settings.asOfMonth).toBe('2027-02')
    expect(d.assets.find((a) => a.id === 'sample-cheque')!.valueCents).toBe(1_234_567)
    expect(d.snapshots.map((s) => s.month)).toEqual(['2027-02'])
    expect(screen.getByRole('heading', { name: 'History' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'Liquid balance: actual against projected' })).toBeInTheDocument()
  })

  it('refuses a month before the model and flags bad amounts', async () => {
    const user = userEvent.setup()
    await open('checkin')
    await user.clear(screen.getByLabelText('Check-in month'))
    await user.type(screen.getByLabelText('Check-in month'), '2026-08')
    expect(screen.getByText('Must be Sep 2026 or later')).toBeInTheDocument()
    await user.clear(screen.getByLabelText('Check-in month'))
    await user.type(screen.getByLabelText('Check-in month'), '2026-09')
    const cheque = screen.getByLabelText('Everyday account (sample)')
    await user.clear(cheque)
    await user.type(cheque, 'lots')
    await user.click(screen.getByRole('button', { name: 'Review and save check-in' }))
    expect(screen.getByText('Fix the highlighted values.')).toBeInTheDocument()
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('deletes a check-in from the history without touching balances', async () => {
    const user = userEvent.setup()
    await open('checkin')
    await user.click(screen.getByRole('button', { name: 'Review and save check-in' }))
    await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Save check-in' }))
    await user.click(await screen.findByRole('button', { name: 'Delete check-in for Sep 2026' }))
    await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Delete' }))
    await waitFor(async () => expect((await readDataset()).snapshots).toEqual([]))
    expect((await readDataset()).settings.asOfMonth).toBe('2026-09')
  })
})

describe('backup and restore', () => {
  it('exports a JSON backup and records the date', async () => {
    const user = userEvent.setup()
    let saved: Blob | null = null
    const createObjectURL = vi.fn((b: Blob) => {
      saved = b
      return 'blob:test'
    })
    Object.assign(URL, { createObjectURL, revokeObjectURL: vi.fn() })
    const click = vi.spyOn(HTMLAnchorElement.prototype, 'click').mockImplementation(() => {})
    await open('data')
    expect(screen.getByText(/Last backup: never/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Export JSON' }))
    expect(await screen.findByText(/Backup saved to your downloads/)).toBeInTheDocument()
    expect(click).toHaveBeenCalled()
    const file = JSON.parse(await saved!.text())
    expect(file).toMatchObject({ format: 'letsema-coverage', schemaVersion: 1 })
    expect(file.data.assets).toHaveLength(7)
    expect((await getSettings()).lastExportAt).not.toBeNull()
  })

  it('restores a backup after confirmation, replacing current data', async () => {
    const user = userEvent.setup()
    const backup = await readDataset()
    const text = buildExport({ ...backup, assets: backup.assets.slice(0, 2) }, '2026-09-01T10:00:00.000Z')
    await updateSettings({ currency: 'USD' })
    await open('data')
    await user.upload(screen.getByLabelText('Import backup…'), new File([text], 'backup.json', { type: 'application/json' }))
    const dialog = await screen.findByRole('dialog')
    expect(within(dialog).getByText(/holds 19 items, 4 scenarios and 0 check-ins, as of Sep 2026/)).toBeInTheDocument()
    await user.type(within(dialog).getByRole('textbox'), 'replace')
    await user.click(within(dialog).getByRole('button', { name: 'Replace and restore' }))
    expect(await screen.findByText('Backup restored.')).toBeInTheDocument()
    const d = await readDataset()
    expect(d.assets).toHaveLength(2)
    expect(d.settings.currency).toBe('ZAR')
  })

  it('explains why a file cannot be imported', async () => {
    const user = userEvent.setup()
    await open('data')
    await user.upload(screen.getByLabelText('Import backup…'), new File(['{"hello":1}'], 'x.json', { type: 'application/json' }))
    expect(await screen.findByText('This is not a Coverage backup.')).toBeInTheDocument()
    expect((await readDataset()).assets).toHaveLength(7)
  })
})

describe('dashboard reminders', () => {
  it('prompts for a backup when there has never been one', async () => {
    await open('dashboard')
    expect(await screen.findByText(/You have not backed up yet/)).toBeInTheDocument()
    await updateSettings({ lastExportAt: new Date().toISOString() })
    await waitFor(() => expect(screen.queryByText(/You have not backed up yet/)).not.toBeInTheDocument())
  })
})
