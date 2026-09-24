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
