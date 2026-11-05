# 9.3 Metas de cobertura de código

A meta é maior onde o erro mexe com dinheiro ou com acesso à conta. Cobertura mede **linhas e ramos** executados pelos testes de unidade e de integração juntos.

| Módulo | Linhas | Ramos | Por que esse número |
| --- | --- | --- | --- |
| identidade | 90% | 85% | Login, troca de aparelho e sessão são a principal barreira contra golpe (ADR-010, R01) |
| contas | 90% | 85% | Razão contábil e saldo. Erro aqui é dinheiro errado (RNF11) |
| pagamentos | 90% | 85% | Pix, boleto, idempotência e saga com estorno |
| antifraude | 85% | 80% | Cada regra de risco é uma Strategy pequena e fácil de testar |
| familia | 80% | 75% | Limites e aprovações. Mexe com dinheiro, mas sempre passa pelo módulo de pagamentos |
| atendimento | 70% | 60% | Fluxo de chamado, pouca regra de negócio |
| notificacao | 70% | 60% | Envio é idempotente e testado na integração do outbox |
| backoffice | 70% | 60% | Cadastro de funcionário e auditoria |
| app mobile (lógica, fora das telas) | 70% | 60% | Estados de tela e chamadas à API. As telas são cobertas pelo E2E e pelos testes com usuários |
| **Projeto inteiro (mínimo)** | **80%** | **70%** | Média ponderada esperada com as metas acima |

## Como o pipeline cobra

1. O Jest roda com `--coverage` e um `coverageThreshold` **por pasta de módulo** com os números acima.
2. Se qualquer módulo ficar abaixo da meta, o job de testes falha e o pull request **não pode ser mesclado** (regra de proteção da branch `main`).
3. Pull request que **diminui** a cobertura de identidade, contas ou pagamentos é bloqueado mesmo se continuar acima da meta.
4. O relatório de cobertura fica anexado a cada execução do pipeline.

## O que não conta

- Código gerado (cliente do OpenAPI, migrações) fica fora da medição.
- Cobertura alta não substitui o teste de integração com o banco real: o gatilho do razão e o outbox só são aceitos com teste de integração (DoD).
