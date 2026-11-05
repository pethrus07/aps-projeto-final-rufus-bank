# 5.6 Estratégia: backup, LGPD e migrações

## Backup

O objetivo vem do RNF12: perder no máximo **5 minutos** de dados (RPO) e voltar ao ar em até **1 hora** (RTO).

| Camada | Frequência | Retenção | Para quê | Custo |
| --- | --- | --- | --- | --- |
| Réplica síncrona Multi-AZ | Contínua (cada transação confirmada nas 2 zonas) | Não é backup, é cópia viva | Falha de máquina ou de zona: failover automático, sem perda de dado | Já no preço da instância Multi-AZ (Bloco 1) |
| Backup automático do RDS com log de transações | Snapshot diário + log contínuo enviado a cada 5 minutos | **35 dias** (o máximo do RDS) | Restaurar a **qualquer ponto** dos últimos 35 dias. Erro humano ou de software que apagou ou corrompeu dados | 50 GB além da cota grátis já custeados no Bloco 1 (US$ 4,75/mês) |
| Snapshot manual mensal, copiado para uma conta AWS separada (cofre de backup com bloqueio contra exclusão) na mesma região | Todo dia 1º, às 3h | **12 meses** | Comparar com meses anteriores, responder auditoria fora da janela de 35 dias e ter uma cópia que um invasor da conta principal não consegue apagar | Custeado no item 4.4 do Bloco 1: 12 x 50 GB a US$ 0,095 por GB-mês, US$ 57,00 por mês |

**Por que não copiar para outra região.** A única região da AWS no Brasil é São Paulo. Copiar o backup para os EUA seria transferência internacional de dados pessoais (LGPD, art. 33), o que o ADR-013 evita. A proteção contra desastre fica nas 3 zonas de disponibilidade da região e na conta separada. Se um dia for exigida uma cópia fora de São Paulo, ela entra como decisão nova, com as salvaguardas do art. 33.

**Teste de restauração a cada 3 meses** (RNF12): restaurar o backup de um ponto no tempo em uma instância temporária, rodar `bloco-5-banco/testes/testar-schema.sh` adaptado para a cópia e conferir a soma de lançamentos por carteira contra o saldo de fechamento. O tempo medido do início ao fim precisa ficar abaixo de 1 hora. O resultado é registrado; se passar de 1 hora, vira item de sprint.

**O que não é backup:** os registros que a lei manda guardar por 5 anos (lançamentos, transações, auditoria) **não** dependem do backup. Eles ficam no próprio banco, protegidos contra alteração por gatilho (`tg_lancamento_imutavel`, `tg_auditoria_imutavel`).

## LGPD

### Quais campos são dado pessoal

O dicionário de dados marca **26 colunas** com tratamento LGPD (22 de dado pessoal e 4 de segredo; uma coluna pode ter mais de uma marcação), todas tiradas do `COMMENT ON` do SQL. Resumo:

| Marcação | Quantidade | Exemplos | Tratamento |
| --- | --- | --- | --- |
| PII | 22 (inclui as 2 cifradas do cliente) | `cliente.nome_completo`, `cliente.celular`, `pix_envio.nome_recebedor`, `contato_confianca.celular`, `registro_auditoria.ip` | Acesso só pelo módulo dono. Nunca vai para log (o logger mascara esses nomes de campo). Entra na exportação do titular (RF029) |
| CIFRADO | 3 | `cliente.cpf_cifrado`, `cliente.data_nascimento_cifrada`, `funcionario.segredo_totp_cifrado` | Cifrado pela aplicação antes de gravar (abaixo) |
| SEGREDO | 4 | `credencial.hash_senha`, `funcionario.hash_senha`, `sessao_renovacao.hash_token`, `funcionario.segredo_totp_cifrado` | Só hash (Argon2id ou SHA-256). Nunca devolvido pela API, nunca exportado |
| PII-SENSIVEL | 0 | | **Nenhum dado sensível é guardado.** A biometria fica no celular (ADR-010) e a selfie do cadastro vai direto para o parceiro de validação de identidade, sem ser gravada pelo Rufus |

A tabela completa está no começo do [dicionário de dados](04-dicionario-de-dados.md).

### Como o CPF e a data de nascimento são cifrados

1. A aplicação pede ao **AWS KMS** uma chave de dados (envelope encryption). A chave mestra nunca sai do KMS.
2. Cifra o valor com **AES-256-GCM** e grava o resultado em `cpf_cifrado` (`bytea`), junto com o vetor de inicialização.
3. Para buscar um cliente pelo CPF sem decifrar a base inteira, grava também `cpf_hash`: **HMAC-SHA256** do CPF com uma chave secreta guardada no Secrets Manager. O HMAC (e não um SHA-256 puro) impede descobrir o CPF testando todos os 10^11 CPFs possíveis, porque sem a chave o atacante não consegue calcular o hash.
4. `cpf_hash` é `UNIQUE`: o banco recusa CPF repetido mesmo sem enxergar o CPF.
5. Quem vazar o banco sem a chave do KMS e a do HMAC não lê CPF nem data de nascimento.

Por que só esses dois: são os campos que, junto com o nome, permitem abrir conta ou crédito em nome da pessoa em outro lugar. Cifrar tudo impediria as buscas e o extrato sem ganho proporcional; os demais PII ficam protegidos pela criptografia do disco do RDS (ativada por padrão com KMS), pela rede privada e pelo controle de acesso.

### Encerramento de conta e anonimização (RF029, US17)

Quando o titular encerra a conta com saldo zero:

| Dado | O que acontece | Por quê |
| --- | --- | --- |
| `cliente.nome_completo`, `celular`, `email` | Substituídos por `ANONIMIZADO` e valores nulos | Não há mais finalidade (LGPD art. 16) |
| `cliente.cpf_cifrado`, `data_nascimento_cifrada` | **Mantidos cifrados por 5 anos** e depois apagados | A prevenção à lavagem de dinheiro (Lei 9.613/1998) exige identificar o titular das movimentações por 5 anos. Base legal: cumprimento de obrigação legal (LGPD art. 16, I) |
| `transacao`, `lancamento`, subtipos | Mantidos 5 anos | Mesma obrigação legal. O razão não pode ser alterado |
| `contato_confianca`, `lembrete_conta`, `dispositivo`, `sessao_renovacao`, `credencial` | Apagados (ON DELETE CASCADE ou exclusão direta) | Sem obrigação de guarda |
| `chamado`, `mensagem_chamado` | Texto anonimizado depois de 5 anos | Prova de atendimento em caso de reclamação |
| `outbox_evento.payload` | Apagado 90 dias depois de processado, para todos os clientes | O evento já cumpriu a função |
| `registro_auditoria` | Mantido 5 anos (RNF14) | Obrigação legal |

Um job mensal apaga o que passou dos 5 anos. Pedido de exportação ou de informação do titular é respondido em até **15 dias** (RNF07, LGPD art. 19).

## Migrações sem parar o sistema

As migrações são arquivos SQL versionados (`node-pg-migrate`, Bloco 3), revisados em pull request e aplicados pelo pipeline antes de trocar as tarefas da API. Como as tarefas antigas e as novas rodam juntas por alguns minutos durante o deploy, **toda migração precisa funcionar com as duas versões do código ao mesmo tempo**. Para isso usamos o padrão **expandir e contrair**.

### Regras

1. Nunca renomear nem apagar coluna no mesmo deploy que muda o código.
2. Coluna nova entra **nula ou com valor padrão constante** (no PostgreSQL isso é só metadado, sem reescrever a tabela).
3. Índice em tabela grande sempre com `CREATE INDEX CONCURRENTLY` (não trava escrita). Essa migração roda fora de transação.
4. Restrição nova em tabela grande: `ADD CONSTRAINT ... NOT VALID` e depois `VALIDATE CONSTRAINT` em outro passo (valida sem travar escrita).
5. Toda migração tem tempo limite: `SET lock_timeout = '5s'`. Se não conseguir a trava, falha e o pipeline para, em vez de travar o banco.

### Exemplo concreto: separar o celular do contato de confiança em DDD e número

Pedido hipotético: o SMS do provedor passa a exigir DDD separado.

| Passo | Deploy | Banco | Código |
| --- | --- | --- | --- |
| 1. Expandir | v1.5 | `ALTER TABLE contato_confianca ADD COLUMN ddd char(2), ADD COLUMN numero text;` (nulas, instantâneo) | Grava nas **duas** formas (`celular` e `ddd` + `numero`), lê da antiga |
| 2. Migrar dados | job | `UPDATE contato_confianca SET ddd = substr(celular, 4, 2), numero = substr(celular, 6) WHERE ddd IS NULL` em lotes de 1.000 linhas | Sem mudança |
| 3. Trocar a leitura | v1.6 | `ALTER TABLE contato_confianca ADD CONSTRAINT ck_ddd CHECK (ddd IS NOT NULL) NOT VALID;` e depois `VALIDATE CONSTRAINT ck_ddd;` | Lê de `ddd` + `numero`, ainda grava nas duas |
| 4. Contrair | v1.7 | `ALTER TABLE contato_confianca DROP COLUMN celular;` | Para de gravar em `celular` |

Em nenhum momento uma versão do código encontra o banco num formato que ela não entende, e cada passo pode ser revertido voltando só o código.
