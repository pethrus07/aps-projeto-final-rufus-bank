# Módulo notificacao

Push, SMS, voz (Polly com cache), lembretes e a tabela outbox lida pelo worker (ADR-008).

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | Notificacao, OutboxEvento, LembreteConta |
| Requisitos | RF007, RF022, RF028 |
| Rotas | /falas, /lembretes |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
