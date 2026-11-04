# 3.4 Padrões de design

Quais padrões o Rufus aplica, onde e por quê. No fim, os padrões que avaliamos e **não** aplicamos, também com o motivo.

## Aplicados

| Padrão | Onde | Por quê |
| --- | --- | --- |
| Monolito modular | Estrutura da API: módulos `identidade`, `contas`, `pagamentos`, `familia`, `antifraude`, `atendimento`, `notificacao`, `backoffice` | Fronteiras claras sem o custo de microsserviços (ADR-001) |
| Portas e Adaptadores (hexagonal) | `PortaBancaria`, `PortaVoz`, `PortaNotificacao`, `PortaIdentidade`, cada uma com adaptador real e falso | Trocar de parceiro BaaS sem tocar no domínio (R04, ADR-002) e rodar tudo no localhost |
| Adapter (camada anticorrupção) | `AdaptadorBaasHttp` traduz o modelo do parceiro para `Transacao` e `Conta` | O modelo do fornecedor não vaza para o domínio |
| Repository | Um repositório por agregado: `ContaRepository`, `TransacaoRepository`, `ChamadoRepository` | O domínio não conhece SQL. Nos testes de unidade o repositório é trocado por um em memória |
| Unit of Work | `UnidadeDeTrabalho` abre a transação do banco e passa os repositórios para o caso de uso | Pix, lançamentos e evento do outbox gravados juntos ou nada (RNF11) |
| Transactional Outbox | Tabela `outbox_evento` gravada na mesma transação, lida pelo worker | Evento nunca perdido nem enviado sem o dado gravado (ADR-008) |
| Saga orquestrada | Envio de Pix: reservar saldo, enviar ao parceiro, confirmar ou compensar (estorno da reserva) | A operação envolve um sistema externo que pode falhar no meio. A compensação devolve o dinheiro ao cliente (diagrama de sequência do erro crítico, Bloco 4) |
| Idempotency Key | Cabeçalho `Idempotency-Key` em `POST /v1/pix/envios` e `POST /v1/boletos/pagamentos`, com restrição única no banco | Zero Pix duplicado (RNF11, US07) |
| State | Ciclo de vida de `Transacao`: PENDENTE, RETIDA, ENVIADA, CONCLUIDA, RECUSADA, ESTORNADA | Cada estado define quais transições são válidas. Impede, por exemplo, estornar um Pix já recusado |
| Strategy | Regras do antifraude (`RegraDestinatarioNovo`, `RegraHorarioNoturno`, `RegraValorForaDoPadrao`) implementam `RegraRisco` | Regra nova entra sem mexer no motor. Cada regra é testada sozinha |
| Factory | `FabricaDeConta` cria conta de titular ou de menor, já com limites e vínculo corretos | Conta de menor tem regras diferentes (RF014, RF015) e não pode nascer sem vínculo |
| Domain Events (Observer) | `PixConcluido`, `ContaBloqueada`, `PedidoAprovacaoCriado` publicados no outbox | Notificação, contato de confiança e responsável reagem sem que o módulo de pagamentos conheça cada um |
| Circuit Breaker com nova tentativa | Chamadas ao parceiro BaaS e ao Polly | Se o parceiro cair, a API para de insistir por 30 s, responde rápido ao cliente e não esgota as conexões (RNF02) |

## Avaliados e não aplicados

| Padrão | Por que não agora |
| --- | --- |
| CQRS com banco de leitura separado | A leitura (saldo e extrato) cabe no p95 de 300 ms com índice e saldo de fechamento diário. Um segundo banco aumentaria custo e criaria atraso entre escrita e leitura, ruim para quem confere o saldo logo depois do Pix |
| Event Sourcing completo | O razão com partidas dobradas (ADR-007) já guarda o histórico do dinheiro. Reconstruir todo o estado a partir de eventos traria complexidade sem requisito que peça |
| Saga coreografada | Com um fluxo central (Pix) e poucos participantes, a saga orquestrada deixa o passo a passo visível num lugar só, mais fácil de testar e de explicar |
