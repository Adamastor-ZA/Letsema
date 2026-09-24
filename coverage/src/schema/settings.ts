import { z } from 'zod'
import { rateBps, yearMonth } from './entities'

/** Thresholds are "higher is better": green at or above `green`, amber at or above `amber`, otherwise red. */
const band = z
  .object({ green: z.number().min(0), amber: z.number().min(0) })
  .refine((b) => b.green >= b.amber, { error: 'Green must be at least amber', path: ['green'] })

export const thresholdsSchema = z.object({
  coverageRatio: band,
  runwayVariableMonths: band,
  runwayAllMonths: band,
  /** Months until the first base-case shortfall; no shortfall in the horizon is always green. */
  firstShortfallMonths: band,
})
export type Thresholds = z.output<typeof thresholdsSchema>

export const CURRENCIES = ['ZAR', 'USD', 'EUR', 'GBP', 'AUD', 'NZD', 'CAD', 'CHF', 'BWP', 'NAD', 'KES', 'NGN'] as const

export const settingsSchema = z.object({
  id: z.literal('settings'),
  currency: z.string().regex(/^[A-Z]{3}$/, { error: 'Use a three-letter currency code' }),
  locale: z.string().min(2),
  asOfMonth: yearMonth,
  horizonYears: z.number().int().min(1, { error: 'At least 1 year' }).max(30, { error: 'At most 30 years' }),
  cpiBps: rateBps(-2_000, 5_000),
  primeBps: rateBps(0, 5_000),
  display: z.enum(['nominal', 'real']),
  sweepAssetId: z.string().nullable(),
  includeT3InDrawdown: z.boolean(),
  overdraftBps: rateBps(0, 10_000),
  thresholds: thresholdsSchema,
  lastExportAt: z.string().nullable(),
})
export type Settings = z.output<typeof settingsSchema>

export const DEFAULT_THRESHOLDS: Thresholds = {
  coverageRatio: { green: 1.5, amber: 1.0 },
  runwayVariableMonths: { green: 24, amber: 12 },
  runwayAllMonths: { green: 12, amber: 6 },
  firstShortfallMonths: { green: 60, amber: 24 },
}

export function defaultSettings(asOfMonth: string): Settings {
  return {
    id: 'settings',
    currency: 'ZAR',
    locale: 'en-ZA',
    asOfMonth,
    horizonYears: 10,
    cpiBps: 450,
    primeBps: 1050,
    display: 'nominal',
    sweepAssetId: null,
    includeT3InDrawdown: false,
    overdraftBps: 0,
    thresholds: DEFAULT_THRESHOLDS,
    lastExportAt: null,
  }
}
