# 5.1 Decisão do banco de dados

**Decisão: PostgreSQL 17 no Amazon RDS, com réplica síncrona em outra zona (Multi-AZ).** O motivo central é que o Rufus movimenta dinheiro, e cada movimentação precisa gravar várias linhas de várias tabelas juntas ou nada (RNF11). Essa é a decisão do ADR-006, detalhada aqui.

## O que os requisitos pedem do banco

| Requisito | O que exige do banco |
| --- | --- |
| RNF11, zero Pix duplicado e razão sem divergência | Transação ACID envolvendo `transacao`, `lancamento` (2 ou mais linhas) e `outbox_evento` ao mesmo tempo. Restrição única para a chave de idempotência |
| ADR-007, partidas dobradas | Gatilho que confere a soma dos lançamentos no fim da transação (`DEFERRABLE`) |
| ADR-008, outbox | Leitura concorrente da fila com `SELECT ... FOR UPDATE SKIP LOCKED` |
| RF005, 1 celular ativo | Índice único parcial (`WHERE ativo`) |
| RNF03, 99,9% | Réplica síncrona e failover automático |
| RNF12, RPO de 5 min e RTO de 1 h | Restauração a qualquer ponto no tempo |
| RNF07, LGPD | Chaves estrangeiras para apagar ou anonimizar em cascata sem deixar órfão. Comentário por coluna para marcar dado pessoal |
| RNF14, auditoria por 5 anos | Tabela só de inserção, protegida por gatilho |

## Comparação

| Critério | **PostgreSQL 17 (RDS Multi-AZ)** escolhido | MongoDB (Atlas ou DocumentDB) | Aurora PostgreSQL | DynamoDB |
| --- | --- | --- | --- | --- |
| Transação entre várias linhas e tabelas | Nativa, ACID completa | Existe desde a versão 4.0, mas com limites de tempo e custo maior; o modelo incentiva um documento por operação | Nativa (é PostgreSQL) | Até 100 itens por transação, sem junção |
| Integridade referencial (chave estrangeira) | Sim | Não existe. A aplicação garante sozinha | Sim | Não existe |
| CHECK, gatilho adiado, índice único parcial | Sim | Validação de esquema limitada, sem gatilho adiado | Sim | Não |
| Consultas do antifraude e da conciliação (somas, junções, janelas por período) | SQL completo | Pipeline de agregação, sem junção eficiente entre coleções | SQL completo | Exige modelar cada consulta antes, sem consulta livre |
| Failover entre zonas | Multi-AZ, automático | Sim (conjunto de réplicas) | Sim, mais rápido | Sim, gerenciado |
| Custo no volume do MVP (10.000 usuários) | US$ 284,40/mês em produção (Bloco 1, preço oficial, com snapshots mensais) | Não calculado: descartado pelos critérios acima | Na configuração padrão cobra também por operação de entrada e saída, além da instância e do armazenamento; o ganho (failover mais rápido, réplicas de leitura) não é necessário para 100 req/s | Barato em volume baixo, mas os critérios de integridade já descartam |
| Encaixe na stack (ADR-004, Kysely) | Direto | Outro driver e outro modelo mental | Direto | SDK próprio |
| **Resultado** | **Atende a todos** | Descartado: sem chave estrangeira e sem gatilho, a integridade do dinheiro ficaria só no código | Descartado por agora: mesmas vantagens a um custo maior; vira opção se a carga crescer muito | Descartado: sem junção e sem integridade referencial |

**Por que não MongoDB (pergunta provável da arguição).** O dado do Rufus é muito relacionado: cliente, conta, carteira, transação, lançamento, análise de risco, vínculo com responsável. O valor de um documento flexível não aparece aqui, e o que perderíamos (chave estrangeira, CHECK, gatilho que recusa lançamento desequilibrado) é justamente o que protege o dinheiro. No PostgreSQL, um lançamento desequilibrado é **recusado pelo banco**, como mostra o teste em [testes/resultado.txt](testes/resultado.txt).

## Normalização

O modelo está na **terceira forma normal (3FN)**:

- **1FN.** Todo campo é atômico. A única lista é `analise_risco.motivos` (`text[]`), que é um atributo descritivo da análise, nunca filtrado nem ligado a outra tabela. Ficar como array evita uma tabela só para códigos de motivo.
- **2FN.** Toda tabela com chave composta (`saldo_fechamento_diario`) tem os outros campos dependentes da chave inteira.
- **3FN.** Nenhum campo depende de outro campo que não seja a chave. Exemplo: o nome do titular não se repete na conta; a conta aponta para o cliente.

Por que 3FN e não menos: cada fato fica em um lugar só, então uma correção (o celular do cliente, por exemplo) não precisa ser feita em várias tabelas, e não existe o risco de duas cópias discordarem. Por que não mais (4FN, 5FN): não há dependências multivaloradas no domínio que justifiquem quebrar mais as tabelas.

## Onde desnormalizamos de propósito

| Onde | O que repete | Por quê |
| --- | --- | --- |
| `saldo_fechamento_diario` | O saldo, que poderia ser sempre calculado somando os lançamentos | Com anos de lançamentos, somar tudo a cada consulta ameaçaria o p95 de 300 ms (RNF01). Saldo atual = último fechamento + lançamentos depois dele. O fechamento é recalculável a qualquer momento a partir do razão, então não há risco de perda |
| `pix_envio.nome_recebedor`, `documento_recebedor_mascarado`, `banco_recebedor` | Dados que pertencem ao recebedor, que não é cliente do Rufus | É o retrato do que foi mostrado e falado ao cliente no momento da confirmação (RF009). Se o recebedor mudar de nome depois, o comprovante continua dizendo a verdade daquele momento |
| `transacao.tipo` repetido em cada subtipo | O tipo, que já está na transação base | Permite a chave estrangeira composta `(transacao_id, tipo)`, que impede o banco de aceitar um `pix_envio` apontando para uma transação de boleto. Testado em [testes/resultado.txt](testes/resultado.txt) |
