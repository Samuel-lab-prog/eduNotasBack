import { Elysia, t } from 'elysia'
import { cors } from '@elysiajs/cors'
import { jwt } from '@elysiajs/jwt'
import { db } from './db'
import { config } from './config'
import { studentsRoutes } from './students'

const app = new Elysia()
  .use(cors({ origin: config.corsOrigin.split(',').map((origin) => origin.trim()), allowedHeaders: ['Content-Type', 'Authorization'], methods: ['GET', 'POST', 'PUT', 'OPTIONS'] }))
  .use(jwt({ name: 'jwt', secret: config.jwtSecret, exp: '8h' }))
  .get('/api/health', async () => {
    await db.$queryRaw`SELECT 1`
    return { status: 'ok', database: 'connected' }
  })
  .post('/api/auth/login', async ({ body, jwt, set }) => {
    const teacher = await db.teacher.findUnique({ where: { email: body.email.trim().toLowerCase() } })
    if (!teacher || !await Bun.password.verify(body.password, teacher.passwordHash)) {
      set.status = 401
      return { error: 'E-mail ou senha incorretos.' }
    }
    const token = await jwt.sign({ sub: teacher.id })
    return { token, teacher: { id: teacher.id, name: teacher.name, email: teacher.email } }
  }, { body: t.Object({ email: t.String({ format: 'email', maxLength: 254 }), password: t.String({ minLength: 1, maxLength: 200 }) }) })
  .derive(({ request, jwt }) => ({
    async currentTeacherId() {
      const authorization = request.headers.get('authorization')
      if (!authorization?.startsWith('Bearer ')) return null
      const payload = await jwt.verify(authorization.slice(7))
      return typeof payload === 'object' && typeof payload.sub === 'string' ? payload.sub : null
    },
  }))
  .get('/api/auth/me', async ({ currentTeacherId, set }) => {
    const teacherId = await currentTeacherId()
    if (!teacherId) { set.status = 401; return { error: 'Sessão expirada. Entre novamente.' } }
    const teacher = await db.teacher.findUnique({ where: { id: teacherId }, select: { id: true, name: true, email: true } })
    if (!teacher) { set.status = 401; return { error: 'Conta não encontrada.' } }
    return { teacher }
  })
  .use(studentsRoutes)
  .onError(({ code, error, set }) => {
    console.error(error)
    if (code === 'VALIDATION') { set.status = 422; return { error: 'Confira os dados informados.' } }
    set.status = 500
    return { error: 'Ocorreu um erro ao processar a solicitação.' }
  })

app.listen({ hostname: '0.0.0.0', port: config.port })
console.log(`EduNotas API escutando em ${app.server?.url}`)

for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, async () => { await db.$disconnect(); process.exit(0) })
}
