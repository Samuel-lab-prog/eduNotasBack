# EduNotas Backend

API HTTP em Bun e Elysia, com Prisma e PostgreSQL. O servidor cuida do login do professor e das operações de leitura e escrita dos alunos e das notas.

## Preparar o banco

Copie `.env.example` para `.env`. Na raiz do projeto, inicie o PostgreSQL local com `docker compose -f backend/compose.yaml up -d`. Depois:

```sh
bun install
bun run db:migrate
bun run db:seed
bun run dev
```

`db:seed` cria ou atualiza a conta definida nas variáveis `TEACHER_NAME`, `TEACHER_EMAIL` e `TEACHER_PASSWORD`. O script inclui cinco alunos fictícios somente quando `SEED_SAMPLE_STUDENTS=true`. Para produção, deixe essa opção desativada e use uma senha que não seja a conta de demonstração.

## Rotas

| Método | Caminho | Uso |
|---|---|---|
| `GET` | `/api/health` | Verifica servidor e conexão com PostgreSQL. |
| `POST` | `/api/auth/login` | Valida e-mail e senha e devolve JWT de oito horas. |
| `GET` | `/api/auth/me` | Retorna o professor da sessão. |
| `GET` | `/api/students` | Lista os alunos do professor autenticado. |
| `POST` | `/api/students` | Cadastra nome, matrícula e turma. |
| `GET` | `/api/students/:id` | Consulta dados e notas de um aluno do professor. |
| `PUT` | `/api/students/:id/grades` | Atualiza as duas notas de 0 a 10. |

As rotas dos alunos conferem o professor dono do registro. A API calcula a média em cada resposta; não há coluna `average` no banco. Senhas usam Argon2id via Bun. `JWT_SECRET` deve ser um segredo aleatório com pelo menos 32 caracteres.

## Variáveis de ambiente

Use `.env.example` para desenvolvimento. No Render, configure `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGIN` e as três variáveis de criação do professor como secrets. Migrations são executadas antes do início do serviço e o seed inicial cria somente o professor definido no Blueprint.
