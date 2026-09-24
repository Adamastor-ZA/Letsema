import { describe, expect, it } from 'vitest'
import { project } from '../project'
import { incomeDue, obligationDue } from '../schedules'
import { toIndex } from '../month'
import { income, inputs, obligation } from './helpers'

const asOf = toIndex('2026-09')
const at = (ym: string) => toIndex(ym)

describe('obligation escalation timing', () => {
  const medical = obligation('medical', 100_000, { escalationBps: 1000, escalationMonth: 1 })

  it('escalates only in the configured month, compounding each year', () => {
    expect(obligationDue(medical, asOf, at('2026-09'))).toBe(100_000)
    expect(obligationDue(medical, asOf, at('2026-12'))).toBe(100_000)
    expect(obligationDue(medical, asOf, at('2027-01'))).toBe(110_000)
    expect(obligationDue(medical, asOf, at('2027-12'))).toBe(110_000)
    expect(obligationDue(medical, asOf, at('2028-01'))).toBe(121_000)
  })

  it('treats the as-of amount as already escalated when the escalation month is the as-of month', () => {
    const o = obligation('rates', 100_000, { escalationBps: 1000, escalationMonth: 9 })
    expect(obligationDue(o, asOf, at('2026-09'))).toBe(100_000)
    expect(obligationDue(o, asOf, at('2027-08'))).toBe(100_000)
    expect(obligationDue(o, asOf, at('2027-09'))).toBe(110_000)
  })

  it('pays annual obligations as a lump in the payment month only', () => {
    const school = obligation('school', 5_000_000, { frequency: 'annual', paymentMonth: 1, escalationBps: 800, escalationMonth: 1 })
    expect(obligationDue(school, asOf, at('2026-12'))).toBe(0)
    expect(obligationDue(school, asOf, at('2027-01'))).toBe(5_400_000)
    expect(obligationDue(school, asOf, at('2027-02'))).toBe(0)
  })

  it('escalates future-starting obligations from the as-of month', () => {
    const uni = obligation('uni', 1_000_000, { startMonth: '2029-02', escalationBps: 1000, escalationMonth: 1 })
    expect(obligationDue(uni, asOf, at('2029-01'))).toBe(0)
    expect(obligationDue(uni, asOf, at('2029-02'))).toBe(1_331_000)
  })

  it('respects start and end months inclusively', () => {
    const o = obligation('o', 1_000, { startMonth: '2026-10', endMonth: '2026-12' })
    expect([9, 10, 11, 12].map((m) => obligationDue(o, asOf, at(`2026-${String(m).padStart(2, '0')}`)))).toEqual([0, 1_000, 1_000, 1_000])
    expect(obligationDue(o, asOf, at('2027-01'))).toBe(0)
  })

  it('applies escalation inside a projection', () => {
    const result = project(
      inputs({ asOfMonth: '2026-01', horizonMonths: 4, obligations: [obligation('o', 1_000, { escalationBps: 1000, escalationMonth: 3 })] }),
    )
    expect(result.rows.map((r) => r.obligationsCents)).toEqual([1_000, 1_000, 1_100, 1_100])
  })
})

describe('income schedules', () => {
  it('pays monthly income with an annual increase in the growth month', () => {
    const salary = income('salary', 1_000_000, { growthBps: 500, growthMonth: 3 })
    expect(incomeDue(salary, asOf, at('2027-02'))).toBe(1_000_000)
    expect(incomeDue(salary, asOf, at('2027-03'))).toBe(1_050_000)
  })

  it('pays annual and irregular income only in their months', () => {
    const bonus = income('bonus', 500_000, { frequency: 'annual', months: [3] })
    const consulting = income('consulting', 100_000, { frequency: 'irregular', months: [4, 7, 10] })
    const months = ['2026-10', '2026-11', '2027-03', '2027-04', '2027-07']
    expect(months.map((m) => incomeDue(bonus, asOf, at(m)))).toEqual([0, 0, 500_000, 0, 0])
    expect(months.map((m) => incomeDue(consulting, asOf, at(m)))).toEqual([100_000, 0, 0, 100_000, 100_000])
  })

  it('stops income after its end month', () => {
    const result = project(inputs({ horizonMonths: 5, incomes: [income('contract', 10_000, { endMonth: '2026-03' })] }))
    expect(result.rows.map((r) => r.incomeCents)).toEqual([10_000, 10_000, 10_000, 0, 0])
  })

  it('splits income by confidence', () => {
    const result = project(
      inputs({ horizonMonths: 1, incomes: [income('a', 700, { confidence: 'committed' }), income('b', 300, { confidence: 'variable' })] }),
    )
    expect(result.rows[0]).toMatchObject({ incomeCents: 1_000, committedIncomeCents: 700, variableIncomeCents: 300 })
  })
})
