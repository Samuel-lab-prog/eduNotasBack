# EduNotas Entrega 1 Modelagem do sistema

**Data prevista:** 02/11/2026  
**Trabalho de análise de sistemas**

## Quadro de visão do produto

| Tópico | Descrição |
|---|---|
| Problema | O professor registra notas em mais de um lugar e precisa calcular médias manualmente. Isso dificulta encontrar o boletim atualizado de cada aluno. |
| Objetivo | Manter os dados dos alunos e as duas avaliações em uma aplicação acessível ao professor. A média é calculada pelo sistema. |
| Público-alvo | Professor que acompanha uma ou mais turmas de uma escola ou curso. |
| Funcionalidades | Entrar como professor; consultar alunos; cadastrar aluno; abrir boletim; registrar ou editar duas notas; consultar a média aritmética. |
| Benefícios | Lista de alunos centralizada, notas persistidas no banco e cálculo feito de forma consistente. |
| Restrições | O trabalho trata de um perfil de professor, sem recuperação de senha, cadastro público de contas ou outros perfis. A tela de login não substitui uma política de segurança escolar. |
| Escopo | Home, login, resumo do professor, lista, cadastro, boletim e edição de notas. Não inclui frequência, mensagens, atividades, calendário ou exclusão de alunos. |

## Ator e casos de uso

O **Professor** é o ator principal. Ele acessa o sistema, entra com sua conta, consulta e cadastra alunos e consulta ou edita as notas. A aplicação calcula a média durante a consulta e após a edição; o professor não inicia um caso de uso separado para esse cálculo.

Diagrama UML: [`casos-de-uso.puml`](casos-de-uso.puml). A imagem correspondente será incluída nesta entrega.

## Especificações expandidas

### UC01 — Acessar sistema

- **Ator:** Professor.
- **Pré-condição:** nenhuma; o professor está na página inicial.
- **Fluxo principal:** (1) O professor seleciona “Entrar”. (2) O sistema abre o formulário de acesso.
- **Alternativas:** uma rota inexistente retorna à página inicial.
- **Pós-condição:** formulário de login disponível.

### UC02 — Entrar como professor

- **Ator:** Professor.
- **Pré-condição:** conta criada pelo seed ou por procedimento administrativo e formulário aberto.
- **Fluxo principal:** (1) O professor informa e-mail e senha. (2) O frontend envia os dados à API. (3) A API localiza o professor pelo e-mail e compara a senha com o hash Argon2id guardado no banco. (4) Se os dados forem válidos, a API retorna um JWT com validade de oito horas. (5) O frontend mantém o token na sessão do navegador e abre o resumo.
- **Alternativas:** campos inválidos são rejeitados; e-mail ou senha incorretos retornam erro de autenticação; token expirado encerra o acesso e direciona ao login.
- **Pós-condição:** sessão autenticada disponível no navegador.
- **Limite:** a criação de contas acontece por configuração e seed. Não há cadastro público nem recuperação de senha.

### UC03 — Consultar alunos

- **Ator:** Professor.
- **Pré-condição:** token válido.
- **Fluxo principal:** (1) O professor abre a lista. (2) A API retorna somente alunos ligados ao professor autenticado, ordenados por nome. (3) O sistema mostra nome, matrícula, turma, média e ações. (4) O professor pode filtrar a lista por nome, matrícula ou turma.
- **Alternativas:** lista vazia apresenta a ação de cadastrar; token inválido retorna ao login; filtro sem resultado mostra lista vazia.
- **Pós-condição:** dados consultados; nenhuma alteração é feita.

### UC04 — Cadastrar aluno

- **Ator:** Professor.
- **Pré-condição:** token válido e formulário aberto.
- **Fluxo principal:** (1) O professor informa nome, matrícula e turma. (2) O sistema verifica os campos obrigatórios. (3) A API grava o aluno associado ao professor e inicia as duas notas em zero. (4) O sistema retorna à lista e mostra o novo registro.
- **Alternativas:** campo vazio ou dados inválidos impedem a gravação; matrícula repetida para o mesmo professor retorna conflito e mantém o professor no formulário.
- **Pós-condição:** novo aluno persistido em PostgreSQL.

### UC05 — Consultar notas do aluno

- **Ator:** Professor.
- **Pré-condição:** token válido e aluno pertencente ao professor.
- **Fluxo principal:** (1) O professor abre o boletim pela lista. (2) A API confirma a propriedade do registro e retorna os dados, nota 1, nota 2 e média `(nota1 + nota2) / 2`. (3) O sistema apresenta o boletim.
- **Alternativas:** id inexistente ou aluno de outro professor retorna não encontrado; token inválido retorna ao login.
- **Pós-condição:** boletim consultado. A média não é persistida como campo separado.

### UC06 — Editar notas do aluno

- **Ator:** Professor.
- **Pré-condição:** token válido, aluno existente e tela de edição aberta.
- **Fluxo principal:** (1) O professor informa duas notas entre 0 e 10. (2) A tela pré-visualiza a média. (3) A API valida faixa e propriedade do registro. (4) O sistema grava as notas no PostgreSQL e retorna o aluno com a média recalculada. (5) O boletim atualizado é mostrado.
- **Alternativas:** nota ausente ou fora do intervalo é rejeitada; aluno não encontrado retorna erro; cancelar volta ao boletim sem enviar mudanças.
- **Pós-condição:** notas atualizadas no banco e média recalculada.

## Diagrama expandido

O diagrama mostra as validações e a persistência envolvidas no cadastro e na edição. A média é incluída na consulta e no retorno da edição.

Fonte editável: [`casos-de-uso-expandido.puml`](casos-de-uso-expandido.puml).

## Diagrama de classes

O backend persiste `Teacher` e `Student`. Cada aluno tem uma chave estrangeira para o professor responsável; matrícula é única por professor. `passwordHash` é mantido no banco e nunca enviado pela API. A média é um valor derivado, sem coluna própria.

Fonte editável: [`classes.puml`](classes.puml).

## Rastreabilidade

O frontend usa React, TypeScript, Vite e Chakra UI. A API usa Bun, Elysia e Prisma; os dados ficam no PostgreSQL. As rotas visuais são `/`, `/login`, `/notas`, `/alunos`, `/alunos/novo`, `/alunos/:id` e `/alunos/:id/editar`. As rotas HTTP estão listadas no README do backend.
