# Módulo antifraude

Motor de risco com regras Strategy. Pix com nota 70 ou mais fica RETIDA para o analista.

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | AnaliseRisco |
| Requisitos | RF026, RF027 |
| Rotas | /admin/analises |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
