function required(name: string, fallback?: string) {
  const value = process.env[name]?.trim() || fallback
  if (!value) throw new Error(`A variável ${name} precisa ser configurada.`)
  return value
}

export const config = {
  port: Number(process.env.PORT || 3000),
  databaseUrl: required('DATABASE_URL'),
  jwtSecret: required('JWT_SECRET'),
  corsOrigin: required('CORS_ORIGIN', 'http://localhost:5173'),
}

if (!Number.isInteger(config.port) || config.port < 1 || config.port > 65535) {
  throw new Error('PORT deve ser um número entre 1 e 65535.')
}
if (config.jwtSecret.length < 32) throw new Error('JWT_SECRET precisa ter ao menos 32 caracteres.')
