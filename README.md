# EduNotas

Aplicação simples para o professor cadastrar alunos e registrar duas avaliações por aluno. O projeto tem dois repositórios independentes: `backend/` e `frontend/`. A raiz do diretório local contém somente essas duas pastas.

## Rodar tudo em Docker

Com os diretórios `backend/` e `frontend/` lado a lado, rode da raiz do projeto:

```sh
Copy-Item backend/.env.docker.example backend/.env.docker
docker compose --env-file backend/.env.docker -f backend/compose.yaml up --build
```

Copie o exemplo só na primeira vez; se `backend/.env.docker` já existir, mantenha-o e edite as variáveis que quiser trocar. A interface abre em `http://localhost:5173`, a API em `http://localhost:3000/api` e o PostgreSQL na porta local `5433`. A primeira inicialização aplica as migrations e cria a professora e, por padrão, cinco alunos fictícios. Use `professora@edunotas.com` e `Edunotas-Local-2026!` para entrar. Esses valores são só para desenvolvimento local.

## Desenvolvimento com Bun

Requer Bun 1.4 ou posterior e Docker Desktop. Para rodar a API e a interface fora de containers, inicie somente o PostgreSQL a partir deste repositório:

```sh
docker compose up -d postgres
```

Copie `.env.example` para `.env` e prepare a API:

```sh
bun install
bun run db:migrate
bun run db:seed
bun run dev
```

Em outro terminal, dentro do repositório do frontend, rode `bun install` e `bun run dev`. A interface abre em `http://localhost:5173`; a API responde em `http://localhost:3000/api`. O usuário de exemplo é `professora@edunotas.com`; a senha de desenvolvimento está em `.env.example`.

## Funcionalidades

- Login de professor com senha armazenada em hash Argon2id e token JWT com expiração.
- Lista de alunos, busca por nome/matrícula/turma, cadastro e visualização do boletim.
- Edição das duas notas, limitadas de 0 a 10.
- Média aritmética calculada pela API e interface como `(nota1 + nota2) / 2`; o valor é derivado, não salvo.
- Relação professor–aluno no PostgreSQL e matrícula única por professor.
- Cinco registros de demonstração, todos fictícios; o seed não cria dados pessoais reais.

## Documentação

Os arquivos de projeto e os quatro documentos Word estão em `docs/`. Para refazer os `.docx`, use `scripts/build-documents.py` com o Python, Pillow e `python-docx`.

## Render

`Dockerfile` e `render.yaml` configuram a API e o PostgreSQL deste repositório. Ao criar/sincronizar o Blueprint do backend, preencha:

| Variável | O que informar |
|---|---|
| `TEACHER_NAME` | Nome da pessoa que administrará a conta inicial. |
| `TEACHER_EMAIL` | E-mail usado para entrar no sistema. |
| `TEACHER_PASSWORD` | Senha forte, com pelo menos 12 caracteres. |
| `DATABASE_URL` | Render conecta ao PostgreSQL criado pelo Blueprint. |
| `JWT_SECRET` | Render gera automaticamente. |
| `CORS_ORIGIN` | Já aponta para o site padrão `edunotas-web.onrender.com`; altere se usar outro domínio. |

O seed de produção cria somente a conta do professor; alunos fictícios ficam desativados. O repositório do frontend tem seu próprio Dockerfile e Blueprint; confira `VITE_API_URL` com o endereço da API terminado em `/api`. O Render publica cada serviço depois que os checks do GitHub Actions passam.

O banco gratuito do Render expira após 30 dias. Para manter registros de alunos, escolha um plano PostgreSQL pago antes de usar dados de uma escola; consulte as [limitações do plano gratuito do Render](https://render.com/docs/free).

## CI/CD

O GitHub Actions instala dependências travadas pelo `bun.lock`, verifica tipos, executa os testes, valida a API e constrói a imagem Docker. O workflow do backend usa PostgreSQL de teste e confirma login e seed. Conecte cada repositório ao Render; com `autoDeployTrigger: checksPass`, o Render publica o commit depois que a CI correspondente passar.

---

## API

API HTTP em Bun e Elysia, com Prisma e PostgreSQL. O servidor cuida do login do professor e das operações de leitura e escrita dos alunos e das notas.

## Preparar o banco

Copie `.env.example` para `.env` e inicie o PostgreSQL com `docker compose up -d`. Depois:

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
