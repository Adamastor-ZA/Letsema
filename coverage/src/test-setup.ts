import '@testing-library/jest-dom/vitest'

// jsdom has no ResizeObserver; Recharts' ResponsiveContainer needs one.
if (typeof window !== 'undefined' && !('ResizeObserver' in window)) {
  class ResizeObserverStub {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  Object.assign(window, { ResizeObserver: ResizeObserverStub })
}
