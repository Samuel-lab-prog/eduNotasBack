FROM oven/bun:1.4.0 AS build

WORKDIR /app
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY prisma ./prisma
RUN DATABASE_URL=postgresql://postgres:postgres@localhost:5432/edunotas?schema=public bunx prisma generate
COPY src ./src
COPY tsconfig.json ./
RUN bun run build

FROM oven/bun:1.4.0 AS runtime

WORKDIR /app
ENV NODE_ENV=production
COPY package.json bun.lock ./
RUN bun install --production --frozen-lockfile

COPY prisma ./prisma
COPY src ./src
COPY --from=build /app/node_modules/.prisma ./node_modules/.prisma
COPY docker-entrypoint.sh ./
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 3000
CMD ["/app/docker-entrypoint.sh"]
