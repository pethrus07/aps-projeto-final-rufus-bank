# 5.5 Dicionário de dados

> Arquivo **gerado** por `bloco-5-banco/ferramentas/gerar_dicionario.py` a partir do catálogo de um PostgreSQL 17.11 real com o `sql/001_schema.sql` aplicado. Não editar à mão: mude o SQL (inclusive os `COMMENT ON`) e rode o script de novo.

27 tabelas, 170 colunas, **26 colunas com marcação LGPD**.

Legenda da coluna LGPD: **PII** = dado pessoal (LGPD art. 5º, I) · **PII-SENSIVEL** = dado pessoal sensível (art. 5º, II) · **CIFRADO** = guardado cifrado pela aplicação · **SEGREDO** = credencial, nunca sai do banco nem vai para log · **-** = sem tratamento especial.

## Campos com tratamento LGPD

| Tabela | Campo | Marcação |
| --- | --- | --- |
| chamado | assunto | PII |
| chave_pix | valor | PII |
| cliente | nome_completo | PII |
| cliente | cpf_cifrado | PII, CIFRADO |
| cliente | cpf_hash | PII |
| cliente | data_nascimento_cifrada | PII, CIFRADO |
| cliente | celular | PII |
| cliente | email | PII |
| conta | numero | PII |
| contato_confianca | nome | PII |
| contato_confianca | celular | PII |
| credencial | hash_senha | SEGREDO |
| funcionario | nome | PII |
| funcionario | email | PII |
| funcionario | hash_senha | SEGREDO |
| funcionario | segredo_totp_cifrado | SEGREDO, CIFRADO |
| mensagem_chamado | texto | PII |
| mensagem_chamado | audio_url | PII |
| notificacao | conteudo | PII |
| outbox_evento | payload | PII |
| pix_envio | chave_destino | PII |
| pix_envio | nome_recebedor | PII |
| pix_envio | documento_recebedor_mascarado | PII |
| pix_recebimento | nome_pagador | PII |
| registro_auditoria | ip | PII |
| sessao_renovacao | hash_token | SEGREDO |

## Módulo identidade

### cliente

Pessoa física com conta no Rufus: titular adulto ou menor de 16 e 17 anos.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador interno do cliente. | - |
| `nome_completo` | text | não | - | (length(TRIM(BOTH FROM nome_completo)) >= 3) | Nome civil completo, como no documento. | PII |
| `cpf_cifrado` | bytea | não | - | - | CPF cifrado pela aplicação. Só é decifrado para envio ao parceiro BaaS. | PII, CIFRADO |
| `cpf_hash` | character(64) | não | - | cpf_hash ~ '^[0-9a-f]{64}$'<br>UNIQUE | HMAC-SHA256 do CPF com chave secreta, em hexadecimal. Permite buscar e garantir CPF único sem decifrar. | PII |
| `data_nascimento_cifrada` | bytea | não | - | - | Data de nascimento cifrada. Usada para checar a idade do menor. | PII, CIFRADO |
| `celular` | text | não | - | celular ~ '^\+55[0-9]{10,11}$' | Celular no formato +55DDNNNNNNNNN. Recebe SMS e convites. | PII |
| `email` | text | sim | - | (email IS NULL) OR (email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$') | E-mail opcional. | PII |
| `tipo` | text | não | - | (tipo IN ('TITULAR', 'MENOR')) | TITULAR (adulto) ou MENOR (16 e 17 anos, exige vínculo com responsável). | - |
| `status` | text | não | 'EM_ANALISE'::text | (status IN ('EM_ANALISE', 'ATIVO', 'BLOQUEADO', 'ENCERRADO')) | Situação do cadastro: EM_ANALISE, ATIVO, BLOQUEADO ou ENCERRADO. | - |
| `criado_em` | timestamp with time zone | não | now() | - | Momento do início do cadastro. | - |

Índices:

- `CREATE UNIQUE INDEX cliente_cpf_hash_key ON cliente USING btree (cpf_hash)`

### dispositivo

Celular vinculado à conta. Só um ativo por cliente (RF005).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do vínculo do aparelho. | - |
| `cliente_id` | uuid | não | - | FK → cliente<br>UNIQUE parcial (ativo) | Cliente dono do aparelho. | - |
| `modelo` | text | não | - | - | Modelo informado pelo aparelho, para o cliente reconhecer na lista. | - |
| `chave_publica` | text | não | - | UNIQUE | Chave pública do par gerado no Keystore ou Keychain. Confere a assinatura do login (ADR-010). | - |
| `ativo` | boolean | não | true | - | Verdadeiro para o aparelho em uso. A troca desativa o anterior. | - |
| `vinculado_em` | timestamp with time zone | não | now() | - | Momento do vínculo. | - |

Índices:

- `CREATE UNIQUE INDEX dispositivo_chave_publica_key ON dispositivo USING btree (chave_publica)`
- `CREATE UNIQUE INDEX ux_dispositivo_um_ativo_por_cliente ON dispositivo USING btree (cliente_id) WHERE ativo`

### credencial

Senha de 6 números do cliente e controle de tentativas (RF003, RF004).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `cliente_id` | uuid | não | - | PK<br>FK → cliente | Cliente dono da senha. | - |
| `hash_senha` | text | não | - | hash_senha ~~ '$argon2id$%' | Hash Argon2id da senha (RNF05). A senha nunca é guardada. | SEGREDO |
| `tentativas_erradas` | integer | não | 0 | (tentativas_erradas >= 0) AND (tentativas_erradas <= 5) | Senhas erradas seguidas. Na 5ª o acesso é bloqueado por 30 minutos. | - |
| `bloqueada_ate` | timestamp with time zone | sim | - | - | Fim do bloqueio por tentativas, quando houver. | - |

### sessao_renovacao

Token de renovação de 30 dias, trocado a cada uso (RNF05).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da sessão. | - |
| `dispositivo_id` | uuid | não | - | FK → dispositivo | Aparelho que recebeu o token. | - |
| `hash_token` | character(64) | não | - | UNIQUE | SHA-256 do token de renovação. O token em si só existe no celular. | SEGREDO |
| `expira_em` | timestamp with time zone | não | - | - | Fim da validade (30 dias após a emissão). | - |
| `revogada_em` | timestamp with time zone | sim | - | - | Momento em que o token foi trocado, usado no logout ou revogado na troca de aparelho. | - |

Regras entre colunas:

- `(revogada_em IS NULL) OR (revogada_em <= (expira_em + '30 days'))`

Índices:

- `CREATE UNIQUE INDEX sessao_renovacao_hash_token_key ON sessao_renovacao USING btree (hash_token)`
- `CREATE INDEX ix_sessao_dispositivo_validas ON sessao_renovacao USING btree (dispositivo_id) WHERE (revogada_em IS NULL)`

### consentimento

Registro de cada aceite de termo, com versão e quem aceitou (LGPD art. 8º e 14, risco R08).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do aceite. | - |
| `cliente_id` | uuid | não | - | UNIQUE (cliente_id, tipo, versao_termo)<br>FK → cliente | Titular a quem o consentimento se refere. | - |
| `tipo` | text | não | - | (tipo IN ('TERMOS_DE_USO', 'PRIVACIDADE', 'BIOMETRIA', 'RESPONSAVEL_LEGAL'))<br>UNIQUE (cliente_id, tipo, versao_termo) | Termo aceito: TERMOS_DE_USO, PRIVACIDADE, BIOMETRIA ou RESPONSAVEL_LEGAL. | - |
| `versao_termo` | text | não | - | UNIQUE (cliente_id, tipo, versao_termo) | Versão do texto aceito. Termo novo exige novo aceite. | - |
| `aceito_em` | timestamp with time zone | não | now() | - | Momento do aceite. | - |
| `aceito_por_cliente_id` | uuid | não | - | FK → cliente | Quem aceitou: o próprio titular ou, no caso do menor, o responsável. | - |

Índices:

- `CREATE UNIQUE INDEX consentimento_cliente_id_tipo_versao_termo_key ON consentimento USING btree (cliente_id, tipo, versao_termo)`

## Módulo contas

### conta

Conta de pagamento do cliente, mantida no parceiro BaaS. Uma por cliente no MVP.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador interno da conta. | - |
| `cliente_id` | uuid | não | - | UNIQUE<br>FK → cliente | Cliente dono da conta. Único: uma conta por cliente. | - |
| `agencia` | text | não | - | agencia ~ '^[0-9]{4}$' | Agência no parceiro (4 dígitos). | - |
| `numero` | text | não | - | numero ~ '^[0-9]{5,12}-[0-9X]$'<br>UNIQUE | Número da conta com dígito, por exemplo 123456-7. | PII |
| `id_conta_parceiro` | text | não | - | UNIQUE | Identificador da conta no parceiro BaaS, usado na conciliação. | - |
| `status` | text | não | 'ATIVA'::text | (status IN ('ATIVA', 'BLOQUEADA_TOTAL', 'ENCERRADA')) | ATIVA, BLOQUEADA_TOTAL (botão bloquear tudo, RF020) ou ENCERRADA. | - |
| `bloqueada_em` | timestamp with time zone | sim | - | - | Momento do bloqueio total. Preenchido se e somente se o status é BLOQUEADA_TOTAL. | - |
| `criada_em` | timestamp with time zone | não | now() | - | Momento da abertura. | - |

Regras entre colunas:

- `(status = 'BLOQUEADA_TOTAL') = (bloqueada_em IS NOT NULL)`

Índices:

- `CREATE UNIQUE INDEX conta_cliente_id_key ON conta USING btree (cliente_id)`
- `CREATE UNIQUE INDEX conta_numero_key ON conta USING btree (numero)`
- `CREATE UNIQUE INDEX conta_id_conta_parceiro_key ON conta USING btree (id_conta_parceiro)`

### carteira

Divisão contábil do dinheiro: principal, meta ou carteira técnica de liquidação com o parceiro (ADR-007).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da carteira. | - |
| `conta_id` | uuid | sim | - | FK → conta<br>UNIQUE parcial ((tipo = 'PRINCIPAL'::text)) | Conta dona. Vazio nas carteiras técnicas de liquidação. | - |
| `tipo` | text | não | - | (tipo IN ('PRINCIPAL', 'META', 'LIQUIDACAO_PIX', 'LIQUIDACAO_BOLETO'))<br>UNIQUE parcial ((conta_id IS NULL)) | PRINCIPAL (1 por conta), META (1 por meta), LIQUIDACAO_PIX ou LIQUIDACAO_BOLETO (do sistema). | - |

Regras entre colunas:

- `(tipo ~~ 'LIQUIDACAO_%') = (conta_id IS NULL)`

Índices:

- `CREATE UNIQUE INDEX ux_carteira_principal_por_conta ON carteira USING btree (conta_id) WHERE (tipo = 'PRINCIPAL'::text)`
- `CREATE UNIQUE INDEX ux_carteira_tecnica_unica ON carteira USING btree (tipo) WHERE (conta_id IS NULL)`
- `CREATE INDEX ix_carteira_conta ON carteira USING btree (conta_id)`

### lancamento

Razão contábil em partidas dobradas: a soma dos lançamentos de uma transação é zero (ADR-007). Só inserção.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do lançamento. | - |
| `transacao_id` | uuid | não | - | FK → transacao | Transação que originou o lançamento. | - |
| `carteira_id` | uuid | não | - | FK → carteira | Carteira afetada. | - |
| `valor_centavos` | bigint | não | - | valor_centavos <> 0 | Positivo é crédito, negativo é débito. Nunca zero. | - |
| `criado_em` | timestamp with time zone | não | now() | - | Momento do lançamento. | - |

Índices:

- `CREATE INDEX ix_lancamento_carteira ON lancamento USING btree (carteira_id, criado_em)`
- `CREATE INDEX ix_lancamento_transacao ON lancamento USING btree (transacao_id)`

### saldo_fechamento_diario

Saldo de fechamento por carteira e dia, calculado pelo worker. Desnormalização para o RNF01.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `carteira_id` | uuid | não | - | PK<br>FK → carteira | Carteira fechada. | - |
| `data` | date | não | - | PK | Dia do fechamento (horário de Brasília). | - |
| `saldo_centavos` | bigint | não | - | - | Soma de todos os lançamentos da carteira até o fim do dia. Pode ser negativo só em carteira técnica. | - |

## Módulo pagamentos

### transacao

Toda movimentação de dinheiro. Classe base dos subtipos pix_envio, pix_recebimento, pagamento_boleto e movimento_meta.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | UNIQUE (id, tipo)<br>PK | Identificador da transação. | - |
| `conta_id` | uuid | não | - | FK → conta<br>UNIQUE (conta_id, chave_idempotencia) | Conta do cliente que fez ou recebeu a transação. | - |
| `tipo` | text | não | - | UNIQUE (id, tipo)<br>(tipo IN ('PIX_ENVIO', 'PIX_RECEBIMENTO', 'BOLETO', 'META_GUARDAR', 'META_RESGATAR')) | PIX_ENVIO, PIX_RECEBIMENTO, BOLETO, META_GUARDAR ou META_RESGATAR. Define qual subtipo existe. | - |
| `valor_centavos` | bigint | não | - | valor_centavos > 0 | Valor em centavos, sempre maior que zero. O sentido do dinheiro está nos lançamentos. | - |
| `status` | text | não | 'PENDENTE'::text | (status IN ('PENDENTE', 'RETIDA', 'ENVIADA', 'CONCLUIDA', 'RECUSADA', 'ESTORNADA')) | Estado (padrão State): PENDENTE, RETIDA, ENVIADA, CONCLUIDA, RECUSADA ou ESTORNADA. | - |
| `chave_idempotencia` | text | não | - | (length(chave_idempotencia) >= 8) AND (length(chave_idempotencia) <= 128)<br>UNIQUE (conta_id, chave_idempotencia) | Valor do cabeçalho Idempotency-Key. Único por conta (RNF11). | - |
| `id_parceiro` | text | sim | - | UNIQUE | Identificador fim a fim no parceiro BaaS. Preenchido quando o parceiro aceita. | - |
| `criada_em` | timestamp with time zone | não | now() | - | Momento do pedido. | - |
| `concluida_em` | timestamp with time zone | sim | - | - | Momento do estado final (concluída, recusada ou estornada). | - |

Regras entre colunas:

- `(concluida_em IS NULL) OR (status IN ('CONCLUIDA', 'RECUSADA', 'ESTORNADA'))`

Índices:

- `CREATE UNIQUE INDEX transacao_id_parceiro_key ON transacao USING btree (id_parceiro)`
- `CREATE UNIQUE INDEX ux_transacao_idempotencia ON transacao USING btree (conta_id, chave_idempotencia)`
- `CREATE UNIQUE INDEX ux_transacao_id_tipo ON transacao USING btree (id, tipo)`
- `CREATE INDEX ix_transacao_extrato ON transacao USING btree (conta_id, criada_em DESC, id DESC)`
- `CREATE INDEX ix_transacao_pendentes ON transacao USING btree (status, criada_em) WHERE (status = ANY (ARRAY['PENDENTE'::text, 'RETIDA'::text, 'ENVIADA'::text]))`

### pix_envio

Subtipo de transação: Pix enviado. A chave (transacao_id, tipo) garante que a transação base é PIX_ENVIO.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `transacao_id` | uuid | não | - | PK<br>FK → transacao (transacao_id, tipo) | Transação base. | - |
| `tipo` | text | não | 'PIX_ENVIO'::text | tipo = 'PIX_ENVIO'<br>FK → transacao (transacao_id, tipo) | Sempre PIX_ENVIO. Existe para a chave estrangeira composta. | - |
| `chave_destino` | text | não | - | - | Chave Pix de quem recebe. | PII |
| `nome_recebedor` | text | não | - | - | Nome do recebedor devolvido pelo parceiro, falado antes da confirmação (RF009). | PII |
| `documento_recebedor_mascarado` | text | não | - | documento_recebedor_mascarado ~ '^[*0-9./-]+$' | CPF ou CNPJ do recebedor com dígitos ocultos, por exemplo ***.456.789-**. | PII |
| `banco_recebedor` | text | não | - | - | Nome da instituição do recebedor. | - |
| `destinatario_novo` | boolean | não | - | - | Verdadeiro se a conta nunca enviou Pix para essa chave. Aciona limite menor (RF019). | - |

### pix_recebimento

Subtipo de transação: Pix recebido, avisado pelo webhook do parceiro.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `transacao_id` | uuid | não | - | PK<br>FK → transacao (transacao_id, tipo) | Transação base. | - |
| `tipo` | text | não | 'PIX_RECEBIMENTO'::text | tipo = 'PIX_RECEBIMENTO'<br>FK → transacao (transacao_id, tipo) | Sempre PIX_RECEBIMENTO. | - |
| `nome_pagador` | text | não | - | - | Nome de quem pagou, falado no aviso (US05). | PII |
| `banco_pagador` | text | não | - | - | Instituição de quem pagou. | - |

### pagamento_boleto

Subtipo de transação: boleto ou conta de consumo paga (RF013).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `transacao_id` | uuid | não | - | PK<br>FK → transacao (transacao_id, tipo) | Transação base. | - |
| `tipo` | text | não | 'BOLETO'::text | tipo = 'BOLETO'<br>FK → transacao (transacao_id, tipo) | Sempre BOLETO. | - |
| `linha_digitavel` | text | não | - | linha_digitavel ~ '^[0-9]{44,48}$' | Código lido pela câmera ou digitado, só números (44 a 48 dígitos). | - |
| `beneficiario` | text | não | - | - | Empresa que recebe, falada antes da confirmação. | - |
| `vencimento` | date | não | - | - | Data de vencimento do boleto. | - |
| `juros_centavos` | bigint | não | 0 | juros_centavos >= 0 | Juros e multa por atraso, mostrados separados (US08). | - |

### movimento_meta

Subtipo de transação: guardar ou resgatar dinheiro de uma meta.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `transacao_id` | uuid | não | - | PK<br>FK → transacao (transacao_id, tipo) | Transação base. | - |
| `tipo` | text | não | - | (tipo IN ('META_GUARDAR', 'META_RESGATAR'))<br>FK → transacao (transacao_id, tipo) | META_GUARDAR ou META_RESGATAR. | - |
| `meta_id` | uuid | não | - | FK → meta | Meta movimentada. | - |

Índices:

- `CREATE INDEX ix_movimento_meta_meta ON movimento_meta USING btree (meta_id)`

### chave_pix

Chaves Pix da conta para receber (RF011).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da chave. | - |
| `conta_id` | uuid | não | - | FK → conta | Conta dona da chave. | - |
| `tipo` | text | não | - | (tipo IN ('CPF', 'CELULAR', 'ALEATORIA')) | CPF, CELULAR ou ALEATORIA. | - |
| `valor` | text | não | - | UNIQUE parcial ((status = 'ATIVA'::text)) | Valor da chave (CPF, celular ou código aleatório). | PII |
| `status` | text | não | 'ATIVA'::text | (status IN ('ATIVA', 'EXCLUIDA')) | ATIVA ou EXCLUIDA. | - |
| `criada_em` | timestamp with time zone | não | now() | - | Momento do cadastro. | - |

Índices:

- `CREATE UNIQUE INDEX ux_chave_pix_valor_ativa ON chave_pix USING btree (valor) WHERE (status = 'ATIVA'::text)`
- `CREATE INDEX ix_chave_pix_conta ON chave_pix USING btree (conta_id)`

### meta

Meta de economia (RF017). O dinheiro guardado fica na carteira META da própria meta.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da meta. | - |
| `conta_id` | uuid | não | - | FK → conta | Conta dona da meta. | - |
| `carteira_id` | uuid | não | - | UNIQUE<br>FK → carteira | Carteira META criada junto com a meta (composição). | - |
| `nome` | text | não | - | (length(TRIM(BOTH FROM nome)) >= 1) AND (length(TRIM(BOTH FROM nome)) <= 60) | Nome dado pelo cliente, por exemplo Notebook. | - |
| `valor_alvo_centavos` | bigint | não | - | valor_alvo_centavos > 0 | Quanto o cliente quer juntar. | - |
| `data_alvo` | date | sim | - | - | Data desejada, opcional. | - |
| `imagem_url` | text | sim | - | - | Endereço da imagem da meta no S3. | - |
| `status` | text | não | 'ATIVA'::text | (status IN ('ATIVA', 'CONCLUIDA', 'CANCELADA')) | ATIVA, CONCLUIDA ou CANCELADA. | - |

Índices:

- `CREATE UNIQUE INDEX meta_carteira_id_key ON meta USING btree (carteira_id)`
- `CREATE INDEX ix_meta_conta ON meta USING btree (conta_id) WHERE (status = 'ATIVA'::text)`

## Módulo familia

### vinculo_responsavel

Liga o menor ao responsável legal e guarda os limites (RF014, RF015).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do vínculo. | - |
| `menor_cliente_id` | uuid | não | - | UNIQUE<br>FK → cliente | Cliente menor. Único: um responsável vinculado por menor. | - |
| `responsavel_cliente_id` | uuid | não | - | FK → cliente | Cliente titular que é o responsável legal. | - |
| `status` | text | não | 'CONVIDADO'::text | (status IN ('CONVIDADO', 'ATIVO', 'ENCERRADO')) | CONVIDADO, ATIVO ou ENCERRADO. | - |
| `limite_diario_centavos` | bigint | não | - | limite_diario_centavos >= 0 | Saída máxima por dia da conta do menor. | - |
| `limite_mensal_centavos` | bigint | não | - | limite_mensal_centavos >= 0 | Saída máxima por mês. Não pode ser menor que o diário. | - |
| `convidado_em` | timestamp with time zone | não | now() | - | Momento do convite. | - |
| `aceito_em` | timestamp with time zone | sim | - | - | Momento do aceite do responsável. Obrigatório para ATIVO. | - |
| `expira_em` | timestamp with time zone | não | (now() + '7 days'::interval) | - | Prazo do convite: 7 dias (US09). | - |

Regras entre colunas:

- `menor_cliente_id <> responsavel_cliente_id`
- `limite_diario_centavos <= limite_mensal_centavos`
- `(status = 'ATIVO') <= (aceito_em IS NOT NULL)`

Índices:

- `CREATE UNIQUE INDEX vinculo_responsavel_menor_cliente_id_key ON vinculo_responsavel USING btree (menor_cliente_id)`
- `CREATE INDEX ix_vinculo_responsavel ON vinculo_responsavel USING btree (responsavel_cliente_id) WHERE (status = 'ATIVO'::text)`

### pedido_aprovacao

Pedido do menor para uma saída acima do limite (RF016).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do pedido. | - |
| `vinculo_id` | uuid | não | - | FK → vinculo_responsavel | Vínculo entre o menor e o responsável. | - |
| `transacao_id` | uuid | não | - | UNIQUE<br>FK → transacao | Transação que aguarda a decisão. | - |
| `status` | text | não | 'PENDENTE'::text | (status IN ('PENDENTE', 'APROVADO', 'RECUSADO', 'EXPIRADO')) | PENDENTE, APROVADO, RECUSADO ou EXPIRADO. | - |
| `criado_em` | timestamp with time zone | não | now() | - | Momento do pedido. | - |
| `expira_em` | timestamp with time zone | não | (now() + '24:00:00'::interval) | - | Prazo de 24 horas para decidir (US18). | - |
| `decidido_em` | timestamp with time zone | sim | - | - | Momento da decisão ou da expiração. | - |

Regras entre colunas:

- `(status = 'PENDENTE') = (decidido_em IS NULL)`

Índices:

- `CREATE UNIQUE INDEX pedido_aprovacao_transacao_id_key ON pedido_aprovacao USING btree (transacao_id)`
- `CREATE INDEX ix_pedido_pendente ON pedido_aprovacao USING btree (vinculo_id, expira_em) WHERE (status = 'PENDENTE'::text)`

### contato_confianca

Pessoa avisada em movimentação fora do padrão, sem acesso à conta (RF018).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do contato. | - |
| `cliente_id` | uuid | não | - | FK → cliente | Cliente protegido. | - |
| `nome` | text | não | - | - | Nome do contato (terceiro, não cliente). | PII |
| `celular` | text | não | - | celular ~ '^\+55[0-9]{10,11}$' | Celular do contato, que recebe o aviso por SMS. | PII |
| `status` | text | não | 'CONVIDADO'::text | (status IN ('CONVIDADO', 'ATIVO', 'REMOVIDO')) | CONVIDADO, ATIVO ou REMOVIDO. | - |
| `aceito_em` | timestamp with time zone | sim | - | - | Momento do aceite do convite. | - |

Índices:

- `CREATE INDEX ix_contato_confianca_cliente ON contato_confianca USING btree (cliente_id) WHERE (status = 'ATIVO'::text)`

## Módulo antifraude

### analise_risco

Nota de risco de cada Pix enviado e decisão automática ou do analista (RF026, RF027).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da análise. | - |
| `transacao_id` | uuid | não | - | UNIQUE<br>FK → transacao | Pix analisado. | - |
| `nota` | integer | não | - | (nota >= 0) AND (nota <= 100) | Soma das regras de risco, de 0 a 100. A partir de 70 o Pix é retido. | - |
| `motivos` | text[] | não | '{}'::text[] | - | Regras que pontuaram, por exemplo DESTINATARIO_NOVO e HORARIO_NOTURNO. | - |
| `resultado` | text | não | - | (resultado IN ('LIBERADA_AUTOMATICA', 'RETIDA', 'LIBERADA_ANALISTA', 'RECUSADA_ANALISTA')) | LIBERADA_AUTOMATICA, RETIDA, LIBERADA_ANALISTA ou RECUSADA_ANALISTA. | - |
| `analista_id` | uuid | sim | - | FK → funcionario | Analista que decidiu, quando a decisão é humana. | - |
| `decidida_em` | timestamp with time zone | sim | - | - | Momento da decisão humana. | - |

Regras entre colunas:

- `(resultado IN ('LIBERADA_ANALISTA', 'RECUSADA_ANALISTA')) = ((analista_id IS NOT NULL) AND (decidida_em IS NOT NULL))`
- `(NOT ((resultado = 'LIBERADA_AUTOMATICA') AND (nota >= 70)))`

Índices:

- `CREATE UNIQUE INDEX analise_risco_transacao_id_key ON analise_risco USING btree (transacao_id)`
- `CREATE INDEX ix_analise_fila ON analise_risco USING btree (resultado, id) WHERE (resultado = 'RETIDA'::text)`

## Módulo atendimento

### chamado

Atendimento humano aberto de dentro do app (RF024, RF025).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do chamado. | - |
| `cliente_id` | uuid | não | - | FK → cliente | Cliente que abriu. | - |
| `atendente_id` | uuid | sim | - | FK → funcionario | Atendente responsável. Obrigatório a partir de EM_ATENDIMENTO. | - |
| `assunto` | text | não | - | - | Assunto escrito pelo cliente. Pode conter dado pessoal. | PII |
| `status` | text | não | 'ABERTO'::text | (status IN ('ABERTO', 'EM_ATENDIMENTO', 'RESOLVIDO')) | ABERTO, EM_ATENDIMENTO ou RESOLVIDO. | - |
| `aberto_em` | timestamp with time zone | não | now() | - | Momento da abertura. | - |
| `fechado_em` | timestamp with time zone | sim | - | - | Momento da resolução. | - |

Regras entre colunas:

- `(status = 'RESOLVIDO') = (fechado_em IS NOT NULL)`
- `(status = 'ABERTO') OR (atendente_id IS NOT NULL)`

Índices:

- `CREATE INDEX ix_chamado_cliente ON chamado USING btree (cliente_id, aberto_em DESC)`
- `CREATE INDEX ix_chamado_fila ON chamado USING btree (status, aberto_em) WHERE (status <> 'RESOLVIDO'::text)`

### mensagem_chamado

Mensagens de um chamado. Composição: apagar o chamado apaga as mensagens.

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da mensagem. | - |
| `chamado_id` | uuid | não | - | FK → chamado | Chamado a que pertence. | - |
| `autor` | text | não | - | (autor IN ('CLIENTE', 'ATENDENTE')) | CLIENTE ou ATENDENTE. | - |
| `texto` | text | sim | - | - | Texto da mensagem. Pode conter dado pessoal. | PII |
| `audio_url` | text | sim | - | - | Endereço no S3 do áudio enviado pelo cliente (US14). Voz é dado pessoal. | PII |
| `enviada_em` | timestamp with time zone | não | now() | - | Momento do envio. | - |

Regras entre colunas:

- `(texto IS NOT NULL) OR (audio_url IS NOT NULL)`

Índices:

- `CREATE INDEX ix_mensagem_chamado ON mensagem_chamado USING btree (chamado_id, enviada_em)`

## Módulo backoffice

### funcionario

Usuário interno dos painéis de SAC, antifraude e administração (RF030).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do funcionário. | - |
| `nome` | text | não | - | - | Nome do funcionário. | PII |
| `email` | text | não | - | email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' | E-mail corporativo, usado no login. Único sem diferenciar maiúsculas. | PII |
| `papel` | text | não | - | (papel IN ('ATENDENTE', 'ANALISTA_ANTIFRAUDE', 'ADMINISTRADOR')) | Papel de acesso (RBAC): ATENDENTE, ANALISTA_ANTIFRAUDE ou ADMINISTRADOR. | - |
| `hash_senha` | text | não | - | hash_senha ~~ '$argon2id$%' | Hash Argon2id da senha. | SEGREDO |
| `segredo_totp_cifrado` | bytea | sim | - | - | Segredo do segundo fator TOTP. Vazio até o primeiro login (US22). | SEGREDO, CIFRADO |
| `ativo` | boolean | não | true | - | Falso para funcionário desligado. Nunca se apaga, por causa da auditoria. | - |

Índices:

- `CREATE UNIQUE INDEX ux_funcionario_email ON funcionario USING btree (lower(email))`

### registro_auditoria

Toda consulta e alteração feita por funcionário. Só inserção. Guardado 5 anos (RNF14, Lei 9.613/1998).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | bigint | não | identity | PK | Número sequencial do registro. | - |
| `funcionario_id` | uuid | não | - | FK → funcionario | Quem fez a ação. | - |
| `acao` | text | não | - | - | O que foi feito, por exemplo CONSULTAR_HISTORICO ou DECIDIR_ANALISE. | - |
| `entidade` | text | não | - | - | Tabela afetada, por exemplo cliente ou analise_risco. | - |
| `entidade_id` | text | não | - | - | Identificador da linha afetada. | - |
| `ip` | inet | não | - | - | Endereço IP de onde veio a ação. | PII |
| `ocorrido_em` | timestamp with time zone | não | now() | - | Momento da ação. | - |

Índices:

- `CREATE INDEX ix_auditoria_entidade ON registro_auditoria USING btree (entidade, entidade_id, ocorrido_em DESC)`
- `CREATE INDEX ix_auditoria_funcionario ON registro_auditoria USING btree (funcionario_id, ocorrido_em DESC)`

## Módulo notificacao

### notificacao

Push e SMS enviados ao cliente (RF028).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador da notificação. | - |
| `cliente_id` | uuid | não | - | FK → cliente | Cliente que recebe. | - |
| `canal` | text | não | - | (canal IN ('PUSH', 'SMS')) | PUSH ou SMS. | - |
| `tipo` | text | não | - | - | Evento que gerou a notificação, por exemplo PixConcluido. | - |
| `conteudo` | text | não | - | - | Texto enviado. Pode ter valor e nome de terceiro. | PII |
| `status` | text | não | 'PENDENTE'::text | (status IN ('PENDENTE', 'ENVIADA', 'FALHOU')) | PENDENTE, ENVIADA ou FALHOU. | - |
| `criada_em` | timestamp with time zone | não | now() | - | Momento da criação. | - |
| `enviada_em` | timestamp with time zone | sim | - | - | Momento da entrega ao provedor de push ou SMS. | - |

Regras entre colunas:

- `(status = 'ENVIADA') = (enviada_em IS NOT NULL)`

Índices:

- `CREATE INDEX ix_notificacao_cliente ON notificacao USING btree (cliente_id, criada_em DESC)`

### outbox_evento

Eventos gravados na mesma transação do dado e entregues pelo worker (ADR-008).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | bigint | não | identity | PK | Número sequencial do evento. | - |
| `tipo` | text | não | - | - | Nome do evento de domínio, por exemplo PixConcluido ou ContaBloqueada. | - |
| `agregado_id` | uuid | não | - | - | Identificador da entidade de origem. | - |
| `payload` | jsonb | não | - | - | Dados do evento em JSON. Pode conter dado pessoal; apagado 90 dias após processado. | PII |
| `criado_em` | timestamp with time zone | não | now() | - | Momento da gravação. | - |
| `processado_em` | timestamp with time zone | sim | - | - | Momento em que o worker terminou. Vazio enquanto pendente. | - |
| `tentativas` | integer | não | 0 | tentativas >= 0 | Quantas vezes o worker tentou. | - |
| `proxima_tentativa_em` | timestamp with time zone | não | now() | - | Quando tentar de novo (espera crescente após erro). | - |

Índices:

- `CREATE INDEX ix_outbox_pendentes ON outbox_evento USING btree (proxima_tentativa_em) WHERE (processado_em IS NULL)`

### lembrete_conta

Conta a vencer cadastrada pelo cliente para receber lembrete (RF022).

| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | uuid | não | gen_random_uuid() | PK | Identificador do lembrete. | - |
| `cliente_id` | uuid | não | - | FK → cliente | Cliente lembrado. | - |
| `descricao` | text | não | - | - | Nome da conta, por exemplo Conta de água. | - |
| `dia_vencimento` | integer | não | - | (dia_vencimento >= 1) AND (dia_vencimento <= 31) | Dia do mês do vencimento (1 a 31). O lembrete sai 3 dias antes. | - |
| `ativo` | boolean | não | true | - | Falso quando o cliente desliga o lembrete. | - |

Índices:

- `CREATE INDEX ix_lembrete_dia ON lembrete_conta USING btree (dia_vencimento) WHERE ativo`
