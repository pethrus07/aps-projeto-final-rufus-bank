# Módulo backoffice

Funcionários, papéis (RBAC), login com TOTP e registro de auditoria.

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | Funcionario, RegistroAuditoria |
| Requisitos | RF030, RNF14 |
| Rotas | /admin/auth, /admin/funcionarios |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
