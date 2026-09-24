/**
 * Chart tokens. Categorical slots follow the validated reference order
 * (blue, orange, aqua, yellow); validated on the white surface: adjacent CVD
 * ΔE ≥ 9.1, normal-vision ΔE ≥ 22.9. Aqua and yellow sit below 3:1 contrast,
 * so every chart carries a legend and a table view.
 */
export const SERIES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100'] as const

/**
 * The full validated eight-slot order (adjacent CVD ΔE ≥ 9.1, normal-vision ΔE ≥ 19.6 on white).
 * The base case takes slot 0; each scenario keeps the slot stored with it, so its colour never
 * depends on which other scenarios are shown.
 */
export const PALETTE = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#4a3aa7', '#e34948'] as const
export const BASE_COLOR = PALETTE[0]
export const scenarioColor = (slot: number): string => PALETTE[slot] ?? PALETTE[PALETTE.length - 1]!

export const INK = {
  primary: '#0f172a',
  secondary: '#52514e',
  muted: '#898781',
  grid: '#e7e5e4',
  axis: '#c3c2b7',
  surface: '#ffffff',
}

/** Neutral for liabilities: not an identity hue, so it never competes with the tiers. */
export const DEBT_FILL = '#a8a29e'

export const STATUS = { good: '#0ca30c', warning: '#fab219', critical: '#d03b3b' }

export const AXIS_TICK = { fill: INK.muted, fontSize: 12 }
