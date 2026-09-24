import { describe, expect, it } from 'vitest'
import { ragFor } from '../rag'

describe('ragFor', () => {
  const band = { green: 1.5, amber: 1 }
  it('bands inclusively at each threshold', () => {
    expect(ragFor(1.5, band)).toBe('green')
    expect(ragFor(1.49, band)).toBe('amber')
    expect(ragFor(1, band)).toBe('amber')
    expect(ragFor(0.99, band)).toBe('red')
  })
  it('treats a metric that never bites as green', () => {
    expect(ragFor(null, band)).toBe('green')
  })
  it('handles equal green and amber thresholds', () => {
    expect(ragFor(12, { green: 12, amber: 12 })).toBe('green')
    expect(ragFor(11, { green: 12, amber: 12 })).toBe('red')
  })
})

describe('moneyCompact', () => {
  it('keeps neighbouring ticks distinct and drops trailing zeros', async () => {
    const { makeFormatter } = await import('../format')
    const f = makeFormatter('ZAR', 'en-ZA')
    expect(f.moneyCompact(125_000_000)).toBe('R 1.25m')
    expect(f.moneyCompact(130_000_000)).toBe('R 1.3m')
    expect(f.moneyCompact(100_000_000)).toBe('R 1m')
    expect(f.moneyCompact(1_550_000_000)).toBe('R 15.5m')
    expect(f.moneyCompact(85_000_000)).toBe('R 850k')
    expect(f.moneyCompact(-4_250_000)).toBe('-R 42.5k')
    expect(f.moneyCompact(0)).toBe('R 0')
  })
})
