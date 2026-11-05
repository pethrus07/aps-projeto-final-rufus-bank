# 8.2 Variáveis de ambiente

Todas as variáveis estão em [codigo/.env.example](../codigo/.env.example), com comentário. O dev copia para `.env` (que não vai para o git). Em homologação e produção os valores vêm das definições de tarefa do ECS e os segredos do Secrets Manager (Bloco 6, segurança).

A API valida as obrigatórias na partida: se faltar uma, ela não sobe e diz qual falta (`codigo/backend/src/compartilhado/config.ts`).

| Variável | Obrigatória | Valor local | Em produção | Para quê |
| --- | --- | --- | --- | --- |
| NODE_ENV | não | desenvolvimento | producao | Liga ou desliga `/docs` e ajusta o log |
| PORTA | não | 3000 | 3000 | Porta HTTP da API |
| LOG_NIVEL | não | debug | info | Nível do log |
| VERSAO | não | dev | hash do commit (pipeline) | Mostrada em `/health`. O smoke test confere |
| POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD | só no Compose | rufus, rufus, rufus_local | não usadas | Criação do banco no container |
| DATABASE_URL | **sim** | postgres://rufus:rufus_local@banco:5432/rufus | segredo | Conexão da API e do worker |
| JWT_SEGREDO | **sim** | texto local longo | segredo, rotação a cada 90 dias | Assinatura do token de acesso (ADR-010) |
| JWT_ACESSO_MINUTOS | não | 15 | 15 | Validade do token de acesso (RNF05) |
| JWT_RENOVACAO_DIAS | não | 30 | 30 | Validade do token de renovação (RNF05) |
| LOGIN_TENTATIVAS_MAX | não | 5 | 5 | Senhas erradas antes do bloqueio (RF004) |
| LOGIN_BLOQUEIO_MINUTOS | não | 30 | 30 | Duração do bloqueio (RF004) |
| CHAVE_CIFRA_PII | sim no Sprint 1 | chave local de teste | chave de dados do KMS | Cifra de CPF e data de nascimento (RNF07) |
| OUTBOX_INTERVALO_MS | não | 1000 | 1000 | Pausa entre leituras do outbox (ADR-008) |
| OUTBOX_LOTE | não | 50 | 50 | Eventos por leitura |
| BAAS_ADAPTADOR | não | falso | http | Escolhe o adaptador do parceiro (ADR-002) |
| BAAS_URL, BAAS_CLIENT_ID, BAAS_CLIENT_SECRET | só com `http` | vazio | segredo | Acesso ao parceiro |
| BAAS_WEBHOOK_SEGREDO | sim no Sprint 1 | texto local | segredo | Confere a assinatura HMAC do webhook |
| BAAS_TIMEOUT_MS | não | 8000 | 8000 | Tempo máximo de espera do parceiro, dentro dos 10 s do RNF02 |
| VOZ_ADAPTADOR | não | falso | polly | Voz falsa local ou Amazon Polly (ADR-011) |
| AWS_REGION | não | sa-east-1 | sa-east-1 | Região dos serviços AWS (ADR-013) |
| S3_BUCKET_AUDIOS | não | rufus-audios-local | rufus-audios-prd | Cache dos áudios |
| PUSH_ADAPTADOR | não | falso | expo | Push falso (só log) ou Expo |
| EXPO_ACCESS_TOKEN | só com `expo` | vazio | segredo | Envio de push |
| TOTP_EMISSOR | não | Rufus Bank (local) | Rufus Bank | Nome no app autenticador dos funcionários |
| OPENAPI_CAMINHO | não | definido no Compose | não usada | Arquivo do contrato para o `/docs` |

Regra para variável nova: entra no `.env.example` com comentário e nesta tabela no mesmo pull request. O revisor recusa o PR se faltar uma das duas.
