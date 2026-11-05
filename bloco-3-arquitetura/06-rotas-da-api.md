# 3.6 Rotas da API (fonte única)

Lista canônica das rotas. O contrato completo, com corpos de requisição e resposta, está em OpenAPI 3.0 no Bloco 8 (`bloco-8-dev/openapi.yaml`), que segue esta lista. Os diagramas de sequência (Bloco 4) usam estes mesmos caminhos.

Base: `https://api.rufusbank.com.br/v1` em produção, `http://localhost:3000/v1` no desenvolvimento. Todas as rotas, exceto as marcadas como públicas, exigem `Authorization: Bearer <token de acesso>`.

| Método | Rota | Módulo | RF | Observação |
| --- | --- | --- | --- | --- |
| POST | /onboarding/cadastros | identidade | RF001 | Pública. Inicia o cadastro |
| POST | /onboarding/cadastros/{id}/documentos | identidade | RF001 | Pública com token do cadastro. Foto do documento |
| POST | /onboarding/cadastros/{id}/selfie | identidade | RF001, RF002 | Envia a selfie e dispara a validação no parceiro |
| GET | /onboarding/cadastros/{id} | identidade | RF002 | Situação do cadastro |
| POST | /auth/login | identidade | RF003, RF004 | Pública. CPF, senha e assinatura do aparelho |
| POST | /auth/renovacao | identidade | RNF05 | Pública com token de renovação. Troca o token |
| POST | /auth/logout | identidade | | Revoga a sessão |
| POST | /dispositivos/troca | identidade | RF005 | Selfie nova para trocar de aparelho |
| GET | /contas/me | contas | RF006 | Dados da conta |
| GET | /contas/me/saldo | contas | RF006 | Saldo da carteira principal |
| GET | /contas/me/extrato | contas | RF006 | Paginado por cursor |
| POST | /contas/me/bloqueio-total | contas | RF020 | "Bloquear tudo agora" |
| DELETE | /contas/me/bloqueio-total | contas | RF020 | Desbloqueio com selfie e 1 hora de espera |
| POST | /pix/consultas-chave | pagamentos | RF009 | Devolve nome do recebedor e banco |
| POST | /pix/envios | pagamentos | RF008, RF019 | Exige `Idempotency-Key` |
| GET | /pix/envios/{id} | pagamentos | RF008 | Situação do Pix |
| GET | /pix/envios/{id}/comprovante | pagamentos | RF012 | |
| POST | /pix/cobrancas | pagamentos | RF010 | Gera QR Code para receber |
| GET | /pix/chaves | pagamentos | RF011 | |
| POST | /pix/chaves | pagamentos | RF011 | |
| DELETE | /pix/chaves/{id} | pagamentos | RF011 | |
| POST | /boletos/consultas | pagamentos | RF013 | Lê a linha digitável e devolve beneficiário, valor e vencimento |
| POST | /boletos/pagamentos | pagamentos | RF013 | Exige `Idempotency-Key` |
| GET | /metas | pagamentos | RF017 | |
| POST | /metas | pagamentos | RF017 | |
| POST | /metas/{id}/depositos | pagamentos | RF017 | Exige `Idempotency-Key` |
| POST | /metas/{id}/resgates | pagamentos | RF017 | Exige `Idempotency-Key` |
| POST | /familia/convites-responsavel | familia | RF014 | O menor convida o responsável |
| POST | /familia/vinculos/{id}/aceite | familia | RF014 | O responsável aceita |
| PUT | /familia/vinculos/{id}/limites | familia | RF015 | Só o responsável |
| POST | /familia/pedidos-aprovacao | familia | RF016 | O menor pede |
| POST | /familia/pedidos-aprovacao/{id}/decisao | familia | RF016 | O responsável decide |
| POST | /contatos-confianca | familia | RF018 | |
| DELETE | /contatos-confianca/{id} | familia | RF018 | |
| POST | /falas | notificacao | RF007 | Texto para áudio. Devolve URL do áudio |
| POST | /lembretes | notificacao | RF022 | |
| POST | /chamados | atendimento | RF024 | |
| GET | /chamados/{id}/mensagens | atendimento | RF024 | |
| POST | /chamados/{id}/mensagens | atendimento | RF024 | |
| POST | /titular/exportacoes | identidade | RF029 | Gera arquivo com os dados do titular |
| POST | /titular/encerramento | identidade | RF029 | |
| POST | /webhooks/baas | pagamentos | RF010, RF008 | Pública, com assinatura HMAC do parceiro |
| POST | /admin/auth/login | backoffice | RF030 | Pública. Senha e TOTP |
| GET | /admin/analises | antifraude | RF027 | Papel ANALISTA_ANTIFRAUDE |
| POST | /admin/analises/{id}/decisao | antifraude | RF027 | Papel ANALISTA_ANTIFRAUDE |
| GET | /admin/chamados | atendimento | RF025 | Papel ATENDENTE |
| POST | /admin/chamados/{id}/mensagens | atendimento | RF025 | Papel ATENDENTE |
| GET | /admin/clientes/{id}/historico | atendimento | RF025 | Papel ATENDENTE. Gera registro de auditoria |
| POST | /admin/funcionarios | backoffice | RF030 | Papel ADMINISTRADOR |
| GET | /health (fora do prefixo /v1) | | RNF03 | Pública. Usada pelo balanceador e pela verificação externa do Route 53. Também responde em /v1/health |

Portas: a API escuta na **3000** dentro do container. O balanceador recebe na **443** (HTTPS) e redireciona a 80 para 443. O PostgreSQL usa a **5432**, acessível só de dentro da VPC.
