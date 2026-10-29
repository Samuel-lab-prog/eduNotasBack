# EduNotas Entrega 4 Padrões da interface

**Data prevista:** 23/11/2026

Este documento registra as regras visuais que estão no frontend. A identidade usa verde-petróleo, fundo quente e tipografia sem serifa do sistema. A escolha evita depender de fontes externas.

## Cores em uso

| Nome | HEX | Uso |
|---|---|---|
| Verde-petróleo | `#315F62` | Botão principal, foco e indicadores. |
| Verde escuro | `#24494C` | Estado hover do botão. |
| Verde claro | `#E9EFED` | Fundo de ícones e destaques. |
| Texto | `#273536` | Títulos e conteúdo principal. |
| Texto secundário | `#687575` | Ajuda, contagem e descrição. |
| Fundo | `#F4F3EE` | Fundo geral e página de login. |
| Superfície | `#FFFFFF` | Formulários, tabelas e barra superior. |
| Borda | `#D8DEDB` | Divisores, campos e contorno de cartões. |
| Terracota | `#A66640` | Rótulos pequenos e indicadores de média abaixo de 7. |
| Sucesso | `#357457` | Mensagem de sucesso e média igual ou acima de 7. |
| Erro | `#A83F3F` | Erros de acesso e validação. |

## Tipografia e espaçamento

A interface usa Arial com fallback Helvetica e sans-serif. O tamanho base dos campos e tabela é 12 px; corpo auxiliar, 10–11 px; título de página, 25 px; título da Home, entre 34 e 48 px. Os valores são definidos em `frontend/src/styles/global.css`.

O espaçamento mais usado é 8, 10, 13, 15, 16, 18, 24 e 36 px. Campos têm 39 px de altura; botões, 10 px de preenchimento vertical; os cartões usam 16–24 px de preenchimento. Formas e contornos são simples, geralmente quadrados ou com cantos pouco arredondados.

## Componentes implementados

| Elemento | Aparência e uso |
|---|---|
| Botão principal | Fundo verde-petróleo, texto branco; escurece ao passar o cursor. Implementado com `Button` do Chakra UI. |
| Botão discreto | Fundo cinza quente e contorno; usado para cancelar. |
| Campo de formulário | Fundo branco, borda cinza; mostra contorno verde quando recebe foco. Implementado com `Input` do Chakra UI. |
| Tabela de alunos | Cabeçalho verde acinzentado, linhas separadas por divisor e ações para abrir ou editar notas. Em tela estreita rola dentro do contêiner. |
| Indicador de média | Verde para média igual ou acima de 7; terracota para média inferior a 7. Apresenta uma casa decimal. |
| Navegação | Menu lateral na área do professor; em tela estreita vira barra compacta. |
| Mensagem de sucesso | Faixa verde clara após cadastro ou edição. |
| Mensagem de erro | Fundo rosado e texto vermelho junto ao formulário. |
| Resumo da média | Faixa verde clara com borda lateral. A tela do aluno também mostra cada avaliação. |

## Telas estreitas e rótulos

Em 850 px o menu e as margens diminuem. Em 650 px o menu vira uma barra superior, os cartões empilham e a tabela usa rolagem horizontal própria. Inputs têm rótulos visíveis e mensagens de erro textuais. O login tem entrada de e-mail e senha; a interface não mostra dados da senha.

Fonte: `frontend/src/styles/global.css` e `frontend/src/app/App.tsx`.
