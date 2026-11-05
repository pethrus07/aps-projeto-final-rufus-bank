# Módulo familia

Conta de menor, vínculo com responsável, limites, pedidos de aprovação e contato de confiança.

| | |
| --- | --- |
| Entidades (só este módulo escreve nelas) | VinculoResponsavel, PedidoAprovacao, ContatoConfianca |
| Requisitos | RF014 a RF016, RF018 |
| Rotas | /familia, /contatos-confianca |

Camadas:

- `dominio/`: entidades, regras e interfaces (portas). Não importa NestJS nem banco.
- `aplicacao/`: casos de uso. Abrem a `UnidadeDeTrabalho` e chamam o domínio.
- `infraestrutura/`: repositórios (Kysely) e adaptadores externos.
- `http/`: controllers e DTOs com validação.

Outro módulo só pode usar o que `index.ts` exporta (regra de lint, ADR-001).
Modelo completo em `bloco-3-arquitetura/05-modelo-de-dominio.md`.
