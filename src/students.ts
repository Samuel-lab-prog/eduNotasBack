import { Elysia, t } from 'elysia'
import { jwt } from '@elysiajs/jwt'
import { Prisma } from '@prisma/client'
import { config } from './config'
import { db } from './db'

const studentFields = {
  name: t.String({ minLength: 1, maxLength: 120 }),
  registration: t.String({ minLength: 1, maxLength: 40 }),
  classroom: t.String({ minLength: 1, maxLength: 40 }),
}

function present(student: { id: string; name: string; registration: string; classroom: string; grade1: Prisma.Decimal; grade2: Prisma.Decimal }) {
  const grade1 = Number(student.grade1)
  const grade2 = Number(student.grade2)
  return { ...student, grade1, grade2, average: Math.round(((grade1 + grade2) / 2) * 100) / 100 }
}

export const studentsRoutes = new Elysia({ prefix: '/api/students' })
  .use(jwt({ name: 'jwt', secret: config.jwtSecret, exp: '8h' }))
  .derive(({ request, jwt }) => ({
    async teacherId() {
      const authorization = request.headers.get('authorization')
      if (!authorization?.startsWith('Bearer ')) return null
      const payload = await jwt.verify(authorization.slice(7))
      return typeof payload === 'object' && typeof payload.sub === 'string' ? payload.sub : null
    },
  }))
  .get('/', async ({ teacherId, set }) => {
    const ownerId = await teacherId()
    if (!ownerId) { set.status = 401; return { error: 'Entre para consultar os alunos.' } }
    const records = await db.student.findMany({ where: { teacherId: ownerId }, orderBy: { name: 'asc' } })
    return { students: records.map(present) }
  })
  .post('/', async ({ body, teacherId, set }) => {
    const ownerId = await teacherId()
    if (!ownerId) { set.status = 401; return { error: 'Entre para cadastrar alunos.' } }
    const input = { name: body.name.trim(), registration: body.registration.trim(), classroom: body.classroom.trim() }
    if (!input.name || !input.registration || !input.classroom) { set.status = 400; return { error: 'Preencha nome, matrícula e turma.' } }
    try {
      const student = await db.student.create({ data: { ...input, teacherId: ownerId } })
      set.status = 201
      return { student: present(student) }
    } catch (error) {
      if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === 'P2002') {
        set.status = 409
        return { error: 'Já existe um aluno com essa matrícula.' }
      }
      throw error
    }
  }, { body: t.Object(studentFields) })
  .get('/:id', async ({ params, teacherId, set }) => {
    const ownerId = await teacherId()
    if (!ownerId) { set.status = 401; return { error: 'Entre para consultar as notas.' } }
    const student = await db.student.findFirst({ where: { id: params.id, teacherId: ownerId } })
    if (!student) { set.status = 404; return { error: 'Aluno não encontrado.' } }
    return { student: present(student) }
  })
  .put('/:id/grades', async ({ params, body, teacherId, set }) => {
    const ownerId = await teacherId()
    if (!ownerId) { set.status = 401; return { error: 'Entre para editar as notas.' } }
    const existing = await db.student.findFirst({ where: { id: params.id, teacherId: ownerId }, select: { id: true } })
    if (!existing) { set.status = 404; return { error: 'Aluno não encontrado.' } }
    const student = await db.student.update({
      where: { id: existing.id },
      data: { grade1: body.grade1, grade2: body.grade2 },
    })
    return { student: present(student) }
  }, { body: t.Object({ grade1: t.Number({ minimum: 0, maximum: 10 }), grade2: t.Number({ minimum: 0, maximum: 10 }) }) })
