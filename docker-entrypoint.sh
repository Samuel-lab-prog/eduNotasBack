#!/bin/sh
set -eu

bunx prisma migrate deploy

if [ "${SEED_ON_START:-false}" = "true" ]; then
  bun run db:seed
fi

exec bun src/server.ts
