# Módulo identidade

Cadastro, login, aparelho vinculado, consentimentos e direitos do titular.

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | Cliente, Dispositivo, Credencial, SessaoRenovacao, Consentimento |
| Requisitos | RF001 a RF005, RF029 |
| Rotas | /onboarding, /auth, /dispositivos, /titular |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
