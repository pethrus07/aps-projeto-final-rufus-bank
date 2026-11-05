# 8.3 Guia de padrões de código

Regras que valem para todo código do Rufus. As que uma ferramenta consegue checar são checadas no CI (etapa 1, lint); as outras são conferidas na revisão do pull request.

## Linguagem e nomes

| Regra | Exemplo | Checado por |
| --- | --- | --- |
| Domínio em português, igual ao modelo de domínio (`bloco-3-arquitetura/05-modelo-de-dominio.md`) | `Transacao`, `valorCentavos`, `ServicoEnvioPix` | Revisão |
| Termos técnicos consagrados ficam em inglês | `Controller`, `Repository`, `middleware` | Revisão |
| Classe e tipo em PascalCase, função e variável em camelCase, constante em MAIUSCULAS | `MotorAntifraude`, `processarLote`, `HORAS` | ESLint |
| Banco em snake_case, com os mesmos nomes do domínio | `valor_centavos`, `chave_idempotencia` | Revisão |
| Arquivo em kebab-case com o tipo no fim | `envio-pix.servico.ts`, `conta.repositorio.ts`, `pix.controller.ts` | Revisão |
| Código de erro em MAIUSCULAS_COM_SUBLINHADO, estável | `LIMITE_DESTINATARIO_NOVO` | Contrato OpenAPI |

## TypeScript

- Modo estrito ligado (`strict`, `noUncheckedIndexedAccess`). Proibido `any` (regra de lint como erro).
- **Dinheiro sempre em centavos inteiros.** Nunca `number` com casas decimais para valor. No banco, `bigint`. Na API, inteiro (ADR-004).
- Data e hora sempre em UTC (`timestamptz`). Conversão para o horário de Brasília só na tela.
- Sem `console.log`: use o `log` do pino (regra de lint como erro).
- Entrada da API validada por DTO antes de chegar ao caso de uso.

## Arquitetura no código

| Regra | Por quê |
| --- | --- |
| Cada módulo tem `dominio/`, `aplicacao/`, `infraestrutura/` e `http/` | Mesma estrutura em todo lugar (ADR-001) |
| Outro módulo só pelo `index.ts` público | Fronteira do monolito modular. **O lint bloqueia** import de camada interna de outro módulo |
| `dominio/` não importa NestJS, Kysely nem SDK de fornecedor | O domínio é testado sem banco e sem rede (ADR-002) |
| Tudo que é externo passa por uma porta (`PortaBancaria`, `PortaVoz`...) | Trocar de fornecedor é escrever outro adaptador |
| Um módulo só escreve nas tabelas que são dele | Tabela de dono em `05-modelo-de-dominio.md` |
| Operação que move dinheiro: `UnidadeDeTrabalho` + chave de idempotência + evento no outbox, na mesma transação | RNF11 e ADR-008 |
| Saldo nunca é atualizado: é soma de lançamentos | ADR-007 |
| Consulta SQL com parâmetros, nunca texto concatenado | OWASP A03 |

## Mensagens para o cliente

Toda mensagem que o cliente vê também é falada, então segue a régua de linguagem simples do produto (RNF08):

- Frase com até 15 palavras, na ordem direta.
- Dizer o que aconteceu e o que fazer: "A foto ficou escura, tente perto da janela."
- Sem jargão: "dinheiro que você tem" no lugar de "saldo disponível", "código" no lugar de "token".
- Erro de dinheiro diz se o dinheiro saiu ou não: "Seu dinheiro não saiu."

## Log

- Uma linha JSON por evento, com `correlacaoId`.
- Nunca logar CPF, nome, celular, senha ou token. O `redact` do pino apaga esses campos, mas a regra é não mandá-los.
- Nível `error` só para o que alguém precisa olhar. Regra de negócio recusada (saldo, limite) é `info`.

## Testes

- Todo caso de uso tem teste de unidade com repositório em memória.
- Razão, outbox e idempotência têm teste de integração contra PostgreSQL real.
- Nome do teste em português, descrevendo o comportamento: `it('não cria um segundo Pix com a mesma chave de idempotência')`.
- Cobertura mínima de 80% de linhas no CI. Metas por módulo no Bloco 9.

## Formatação

ESLint com as regras de `codigo/backend/eslint.config.mjs`. Indentação de 2 espaços, aspas simples, ponto e vírgula, linha de até 120 caracteres. O editor formata ao salvar; o CI recusa o que o lint recusa.
