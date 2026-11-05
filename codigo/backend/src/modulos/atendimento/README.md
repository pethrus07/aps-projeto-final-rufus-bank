# Módulo atendimento

Chamados abertos dentro do app e painel do SAC.

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | Chamado, MensagemChamado |
| Requisitos | RF024, RF025 |
| Rotas | /chamados, /admin/chamados, /admin/clientes |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
