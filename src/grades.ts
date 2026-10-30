import { Prisma } from '@prisma/client'

export function calculateAverage(grade1: Prisma.Decimal, grade2: Prisma.Decimal): number {
  return grade1
    .plus(grade2)
    .div(2)
    .toDecimalPlaces(2, Prisma.Decimal.ROUND_HALF_UP)
    .toNumber()
}
