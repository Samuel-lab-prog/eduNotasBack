# EduNotas Entrega 2 Wireframes e referências visuais

**Data prevista:** 09/11/2026  
**Trabalho de análise de sistemas**

## Referências e direção visual

O EduNotas usa uma organização simples de sistema escolar: menu lateral na área do professor, formulários com rótulos diretos e tabela de consulta. A paleta verde-petróleo e o fundo quente diferenciam a interface do AGIAS. Não há ilustrações de gráficos, gradientes decorativos ou cartões flutuantes.

| Item | Escolha |
|---|---|
| Cor principal | Verde-petróleo `#315F62`, usado nos botões e nos indicadores. |
| Fundo | Cinza quente `#F4F3EE`; cartões brancos; divisores `#D8DEDB`. |
| Cor de apoio | Terracota `#A66640` para pequenos rótulos; verde `#357457` para sucesso; vermelho `#A83F3F` para erro. |
| Tipografia | Arial/Helvetica do sistema. Títulos e corpo usam a mesma família, com tamanhos e pesos diferentes. |
| Componentes | Botões retangulares, campos com contorno fino, tabelas sem sombra e cartões com cantos discretos. |
| Imagens | Não são necessárias para esse sistema. A hierarquia vem do texto, menu e tabelas. |

## Wireframes de baixa fidelidade

### 1. Página inicial

```text
+------------------------------------------------------+
| [EduNotas]                                  [Entrar] |
|                                                      |
| Sistema de notas para professores                   |
| Notas da turma, organizadas num só lugar.            |
| Texto breve sobre alunos, avaliações e médias.      |
| [Acessar área do professor]     [O que você encontra]|
|                                01 Lista de alunos    |
|                                02 Duas avaliações    |
|                                03 Média automática   |
+------------------------------------------------------+
| EduNotas · Projeto acadêmico                        |
+------------------------------------------------------+
```

### 2. Login

```text
+----------------------------------------+
| ← Início                               |
| [EduNotas]                             |
| Acesso do professor                    |
| E-mail [___________________________]   |
| Senha  [___________________________]   |
| [Entrar]                               |
+----------------------------------------+
```

### 3. Lista de alunos

```text
+--------------+---------------------------------------+
| EduNotas     | Registro de avaliações                |
| Resumo       | Lista de alunos      [Cadastrar aluno]|
| Alunos       | [Buscar nome, matrícula ou turma]      |
|              | Nome | Matrícula | Turma | Média | Ações|
|              | linhas ordenadas por nome              |
+--------------+---------------------------------------+
```

### 4. Cadastro de aluno

```text
| ← Voltar para alunos                       |
| Cadastrar aluno                            |
| Nome completo [_______________________]    |
| Matrícula     [_______________________]    |
| Turma         [_______________________]    |
|                   [Cancelar] [Cadastrar]  |
```

### 5. Boletim

```text
| ← Voltar para alunos            [Editar notas]|
| Nome do aluno · Matrícula · Turma             |
| MÉDIA ARITMÉTICA                              |
| 8,8 / 10                                      |
| Avaliação 1 8,5/10    Avaliação 2 9,0/10     |
```

### 6. Edição de notas

```text
| ← Voltar para o boletim                     |
| Editar notas · Nome e turma                 |
| Avaliação 1 [ 8,5 ] de 10                  |
| Avaliação 2 [ 9,0 ] de 10                  |
| Média calculada                     8,8     |
|                      [Cancelar] [Salvar]    |
```

Em telas menores o menu vira uma barra compacta, o conteúdo empilha e a tabela rola dentro do próprio quadro. Os wireframes definem os campos e a ordem de leitura; não representam a tela final em escala.
