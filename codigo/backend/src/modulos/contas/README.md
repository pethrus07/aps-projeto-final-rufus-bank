# Módulo contas

Conta, carteiras e razão contábil em partidas dobradas (ADR-007). Saldo é sempre soma de lançamentos.

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | Conta, Carteira, Lancamento |
| Requisitos | RF006, RF020 |
| Rotas | /contas |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
