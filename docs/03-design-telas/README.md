# EduNotas Entrega 3 Telas implementadas

**Data prevista:** 16/11/2026  
**Capturas:** Playwright · 1440 × 1000 px

As imagens mostram o frontend conectado à API local. Os registros da tabela são exemplos fictícios criados pelo seed do banco. Os formulários e notas são os dados retornados e enviados pela API.

## Página inicial

![Página inicial do EduNotas](./screenshots/01-home.png)

## Login do professor

![Login do professor](./screenshots/02-login.png)

## Lista de alunos

![Lista de alunos](./screenshots/03-listagem.png)

## Cadastro de aluno

![Formulário de cadastro](./screenshots/04-cadastro.png)

## Boletim

![Notas de um aluno](./screenshots/05-notas.png)

## Edição de notas

![Formulário de edição de notas](./screenshots/06-edicao.png)

As capturas correspondem às rotas `/`, `/login`, `/alunos`, `/alunos/novo`, `/alunos/:id` e `/alunos/:id/editar`. O arquivo Playwright que percorre essas páginas também testa o envio do cadastro e da edição.
