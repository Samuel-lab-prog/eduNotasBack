import { db } from './db'

const name = process.env.TEACHER_NAME?.trim()
const email = process.env.TEACHER_EMAIL?.trim().toLowerCase()
const password = process.env.TEACHER_PASSWORD

if (!name || !email || !password || password.length < 12) {
  throw new Error('Configure TEACHER_NAME, TEACHER_EMAIL e TEACHER_PASSWORD (mínimo 12 caracteres) antes de criar a conta.')
}

const passwordHash = await Bun.password.hash(password)
const teacher = await db.teacher.upsert({
  where: { email },
  update: { name, passwordHash },
  create: { name, email, passwordHash },
})

if (process.env.SEED_SAMPLE_STUDENTS === 'true') {
  const sampleStudents = [
    ['Ana Clara Souza', '2026001', '9º Ano A', 8.5, 9],
    ['Bruno Martins', '2026002', '9º Ano A', 7, 8],
    ['Camila Oliveira', '2026003', '9º Ano B', 9.5, 9],
    ['Daniel Ferreira', '2026004', '9º Ano B', 6.5, 7.5],
    ['Ester Almeida', '2026005', '8º Ano A', 8, 8.5],
  ] as const
  for (const [studentName, registration, classroom, grade1, grade2] of sampleStudents) {
    await db.student.upsert({
      where: { teacherId_registration: { teacherId: teacher.id, registration } },
      update: {},
      create: { name: studentName, registration, classroom, grade1, grade2, teacherId: teacher.id },
    })
  }
}

console.log(`Conta de professor pronta: ${email}`)
await db.$disconnect()
