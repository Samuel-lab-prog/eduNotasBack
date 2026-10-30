import { describe, expect, test } from 'bun:test'
import { Prisma } from '@prisma/client'
import { calculateAverage } from './grades'

describe('calculateAverage', () => {
  test('calculates an exact two-decimal average', () => {
    expect(calculateAverage(new Prisma.Decimal('8.50'), new Prisma.Decimal('9.00'))).toBe(8.75)
  })

  test('rounds half cents correctly without JavaScript float error', () => {
    expect(calculateAverage(new Prisma.Decimal('10.00'), new Prisma.Decimal('9.99'))).toBe(10)
  })

  test('preserves zero grades', () => {
    expect(calculateAverage(new Prisma.Decimal('0.00'), new Prisma.Decimal('0.00'))).toBe(0)
  })
})
