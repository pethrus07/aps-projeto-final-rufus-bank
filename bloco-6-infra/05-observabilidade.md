# 6.5 Observabilidade

Três coisas: **log estruturado** para investigar, **métricas** técnicas e de negócio para acompanhar, e **alertas** com limiar ligado aos RNFs para avisar antes do cliente reclamar. Tudo no CloudWatch, já custeado no Bloco 1 (logs, 10 alarmes e 20 métricas de negócio).

## Log estruturado

Uma linha JSON por evento, gerada pelo pino (`codigo/backend/src/compartilhado/log.ts`). Exemplo real tirado do compose em 04/11/2026:

```json
{"level":30,"time":"2026-11-05T00:13:44.254Z","servico":"rufus-api","ambiente":"desenvolvimento","correlacaoId":"23ac0913-1d2a-4bf7-a357-b28a50b321e2","metodo":"GET","rota":"/health","status":200,"duracaoMs":2.336995,"msg":"requisicao"}
```

| Regra | Como |
| --- | --- |
| Identificador de correlação em 100% das requisições (RNF13) | O middleware usa o `X-Correlation-Id` recebido ou gera um, devolve na resposta e põe em toda linha. O app envia o mesmo id para o chamado do SAC, então o atendente acha o erro do cliente |
| Nenhum dado pessoal no log (LGPD) | CPF, senha, token, celular e o cabeçalho Authorization são apagados pela lista `redact` do pino, mesmo se alguém os passar por engano |
| Campos fixos | `servico`, `ambiente`, `correlacaoId`, `rota`, `status`, `duracaoMs` |
| Retenção | 90 dias no CloudWatch Logs. Auditoria de funcionário fica no banco por 5 anos (RNF14), não no log |

## Métricas

### Técnicas

| Métrica | Fonte | Para quê |
| --- | --- | --- |
| Latência p95 por rota | ALB (TargetResponseTime) e log da API | RNF01: abaixo de 300 ms |
| Taxa de erro 5xx | ALB | RNF13: alerta acima de 2% |
| Disponibilidade externa | Health check do Route 53 no `/health`, de fora da AWS (pendente de entrar no script de custo) | RNF03: 99,9% ao mês |
| CPU e memória por tarefa | ECS | Auto scaling e dimensionamento |
| Conexões e CPU do banco, espaço livre | RDS | Saber a hora de trocar a instância |
| Idade do evento mais antigo pendente no outbox | Consulta do worker publicada como métrica | Worker parado ou atrasado |
| Circuit breaker do parceiro aberto | API | Parceiro BaaS fora do ar |

### De negócio (as 20 métricas personalizadas do Bloco 1)

| Métrica | Por quê |
| --- | --- |
| Pix enviados, concluídos e recusados por minuto | Saúde do fluxo principal |
| Tempo do toque em "confirmar" até a resposta do Pix (p95) | RNF02: até 10 s |
| Pix retidos pelo antifraude e tempo até a decisão do analista | RF026 e RF027 |
| Uso do "bloquear tudo agora" por hora | Pico indica onda de golpe (R01) |
| Contas abertas por dia e cadastros abandonados por etapa | Adesão (R06) e telas difíceis (R03) |
| Uso do botão "Ouvir" por tela | Quais telas mais precisam de áudio (RNF09) |
| Diferença na conciliação diária com o parceiro | RNF11: tem de ser zero |
| Pedidos de aprovação do responsável sem resposta em 24 h | Fluxo da Camila (RF016) |

## Alertas

Os 10 alarmes do custo do Bloco 1. Cada um tem o limiar tirado de um RNF e vai para o canal de plantão (e-mail e push do celular do responsável da semana).

| # | Alarme | Limiar | Janela | RNF |
| --- | --- | --- | --- | --- |
| 1 | API fora do ar | `/health` externo falhando 2 vezes seguidas | 2 min | RNF03 |
| 2 | Taxa de erro alta | 5xx acima de 2% das requisições | 5 min | RNF13 |
| 3 | API lenta | p95 acima de 300 ms nas rotas de leitura | 10 min | RNF01 |
| 4 | Pix lento | p95 do Pix acima de 10 s | 10 min | RNF02 |
| 5 | Parceiro BaaS fora | Circuit breaker aberto | 2 min | RNF02 |
| 6 | Outbox atrasado | Evento pendente mais antigo com mais de 5 min | 5 min | ADR-008 |
| 7 | Banco no limite | CPU acima de 80% ou espaço livre abaixo de 10 GB | 15 min | RNF04 |
| 8 | Divergência na conciliação | Qualquer diferença diferente de zero | diário | RNF11 |
| 9 | Onda de golpe | "Bloquear tudo agora" ou Pix retidos 3 vezes acima da média da mesma hora na semana anterior | 30 min | R01 |
| 10 | Custo | Fatura projetada acima de 80% do orçamento do mês (AWS Budgets) | diário | R05 |

Os alarmes 1 a 6 acordam o plantão a qualquer hora. Os outros abrem tarefa para o próximo dia útil, menos o 9, que avisa também a equipe antifraude.
