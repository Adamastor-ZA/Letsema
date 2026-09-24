import { describe, expect, it } from 'vitest'
import { assetSchema, debtSchema, eventSchema, incomeSchema, obligationSchema } from '../entities'
import { settingsSchema, defaultSettings } from '../settings'

const issues = (r: { success: boolean; error?: { issues: { path: PropertyKey[]; message: string }[] } }) =>
  r.success ? [] : r.error!.issues.map((i) => `${i.path.join('.')}: ${i.message}`)

describe('entity schemas', () => {
  it('rejects a T3 accessible amount above the value', () => {
    const r = assetSchema.safeParse({ id: 'ra', name: 'RA', tier: 'T3', valueCents: 100, growthBps: 0, accessibleCents: 101, sortOrder: 0 })
    expect(issues(r)).toEqual(['accessibleCents: Cannot exceed the current value'])
  })

  it('rejects out-of-range haircuts and malformed months', () => {
    expect(assetSchema.safeParse({ id: 'a', name: 'a', tier: 'T2', valueCents: 1, growthBps: 0, haircutBps: 10_001, sortOrder: 0 }).success).toBe(false)
    const debt = { id: 'd', name: 'd', balanceCents: 1, rateType: 'fixed', fixedRateBps: 1000, primeMarginBps: 0, instalmentCents: 1, sortOrder: 0 }
    expect(debtSchema.safeParse({ ...debt, endMonth: '2030-13' }).success).toBe(false)
    expect(debtSchema.safeParse({ ...debt, endMonth: '9999-01' }).success).toBe(false)
    expect(debtSchema.safeParse({ ...debt, endMonth: '2030-12' }).success).toBe(true)
  })

  it('requires the end month not to precede the start month', () => {
    const o = { id: 'o', name: 'o', amountCents: 1, frequency: 'monthly', paymentMonth: 1, escalationBps: 0, escalationMonth: 1, sortOrder: 0 }
    expect(issues(obligationSchema.safeParse({ ...o, startMonth: '2027-01', endMonth: '2026-12' }))).toEqual([
      'endMonth: End month is before the start month',
    ])
    expect(obligationSchema.safeParse({ ...o, startMonth: '2027-01', endMonth: null }).success).toBe(true)
  })

  it('checks income months against the frequency', () => {
    const i = {
      id: 'i', name: 'i', amountCents: 1, growthBps: 0, growthMonth: 1, startMonth: '2026-01', endMonth: null, confidence: 'variable', sortOrder: 0,
    }
    expect(issues(incomeSchema.safeParse({ ...i, frequency: 'annual', months: [3, 4] }))).toEqual(['months: Choose the one month it is paid'])
    expect(issues(incomeSchema.safeParse({ ...i, frequency: 'irregular', months: [] }))).toEqual(['months: Choose at least one month'])
    expect(issues(incomeSchema.safeParse({ ...i, frequency: 'irregular', months: [4, 4] }))).toEqual(['months: Months must not repeat'])
    expect(incomeSchema.safeParse({ ...i, frequency: 'monthly', months: [] }).success).toBe(true)
  })

  it('requires positive one-off amounts and a name', () => {
    expect(issues(eventSchema.safeParse({ id: 'e', name: ' ', month: '2027-01', amountCents: 0, direction: 'inflow', sortOrder: 0 }))).toEqual([
      'name: Give it a name',
      'amountCents: Must be more than zero',
    ])
  })
})

describe('settings schema', () => {
  it('accepts defaults and enforces the 1–30 year horizon', () => {
    const s = defaultSettings('2026-09')
    expect(settingsSchema.safeParse(s).success).toBe(true)
    expect(settingsSchema.safeParse({ ...s, horizonYears: 0 }).success).toBe(false)
    expect(settingsSchema.safeParse({ ...s, horizonYears: 31 }).success).toBe(false)
  })

  it('requires green thresholds at or above amber', () => {
    const s = defaultSettings('2026-09')
    const bad = { ...s, thresholds: { ...s.thresholds, coverageRatio: { green: 0.9, amber: 1 } } }
    expect(issues(settingsSchema.safeParse(bad))).toEqual(['thresholds.coverageRatio.green: Green must be at least amber'])
  })
})
