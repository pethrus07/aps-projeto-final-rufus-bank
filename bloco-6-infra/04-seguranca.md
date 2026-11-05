# 6.4 Segurança

Quatro camadas: quem é o usuário (autenticação), o que ele pode fazer (autorização), onde ficam os segredos e como cada item do OWASP Top 10 é tratado. As decisões vêm do ADR-010 e dos RNF05, RNF06, RNF07 e RNF14.

## Autenticação

### Cliente (app)

| Passo | Como funciona |
| --- | --- |
| Cadastro | O app gera um par de chaves no Keystore (Android) ou Keychain (iOS). A chave privada nunca sai do celular. A pública vai para o servidor e fica em `Dispositivo.chavePublica` |
| Login | CPF, senha de 6 números (guardada com Argon2id) e a assinatura de um desafio com a chave do aparelho. Aparelho diferente do vinculado é recusado (RF005) |
| Tokens | Token de acesso JWT assinado, válido por **15 minutos**. Token de renovação aleatório, válido por **30 dias**, guardado no servidor só como hash (`SessaoRenovacao.hashToken`) |
| Renovação | Cada uso do token de renovação gera outro e invalida o anterior. Se um token já trocado for usado de novo, todas as sessões do aparelho são revogadas: sinal de que alguém copiou o token |
| Biometria | Só destrava a chave do aparelho no próprio celular. Nada biométrico chega ao servidor (R08) |
| Operação com dinheiro | Pix e boleto exigem, além do token, a assinatura do pedido com a chave do aparelho, destravada pela biometria na hora |
| Bloqueio | 5 senhas erradas bloqueiam o acesso por 30 minutos (RF004) |

### Funcionário (painéis internos)

Senha com Argon2id e código TOTP de 6 dígitos (segundo fator obrigatório desde o primeiro acesso, US22). Token de 15 minutos, sem renovação por mais de 8 horas, e acesso a `/admin` só pelos IPs da empresa (regra do WAF).

## Autorização: RBAC e ABAC

**RBAC (por papel) para funcionários.** O papel vem no token e cada rota `/admin` declara o papel que aceita (`x-papel` no OpenAPI).

| Papel | Pode | Não pode |
| --- | --- | --- |
| ATENDENTE | Ver e responder chamados, ver histórico do cliente (registrado na auditoria) | Fila antifraude, decidir Pix, cadastrar funcionário |
| ANALISTA_ANTIFRAUDE | Ver a fila de Pix retidos, liberar, recusar e bloquear conta | Responder chamado, cadastrar funcionário |
| ADMINISTRADOR | Cadastrar funcionários e papéis | Movimentar dinheiro de cliente (nenhum papel pode) |

**ABAC (por atributo) para clientes.** O que um cliente pode fazer depende da relação entre ele e o recurso, não de um papel fixo:

| Regra | Atributos checados |
| --- | --- |
| Ver e mexer na própria conta | `conta.clienteId == token.clienteId` |
| Responsável muda limite do menor | Existe `VinculoResponsavel` com `responsavelClienteId == token.clienteId`, `menorClienteId == alvo` e `status == ATIVO` |
| Responsável decide pedido de aprovação | Mesmo vínculo ativo e `pedido.status == PENDENTE` e `agora < pedido.expiraEm` |
| Menor envia Pix | `cliente.tipo == MENOR` obriga checar `limiteDiarioCentavos` e `limiteMensalCentavos` do vínculo |
| Contato de confiança | Recebe aviso, mas não tem nenhuma permissão de leitura na conta |

Toda negação devolve 403 com o código `SEM_PERMISSAO` e o mesmo texto, para não revelar se o recurso existe.

## Gestão de segredos

| Segredo | Onde fica | Rotação |
| --- | --- | --- |
| Senha do banco | Secrets Manager, rotação automática do RDS | 30 dias |
| Segredo de assinatura do JWT | Secrets Manager | 90 dias, com 2 chaves válidas na troca |
| Chave de cifra de CPF e data de nascimento | Chave de dados gerada pelo AWS KMS, guardada cifrada | Anual |
| Credenciais e segredo do webhook do parceiro BaaS | Secrets Manager | Conforme o contrato com o parceiro |
| Token do Expo | Secrets Manager | Quando alguém sai da equipe |

As tarefas do ECS recebem os segredos como variáveis de ambiente injetadas pela AWS no momento da partida (campo `secrets` das definições em `codigo/infra/ecs/`). Nenhum segredo fica no repositório: o `.env` está no `.gitignore` e o gitleaks bloqueia o pipeline se encontrar algum (etapa 4 do CI). São os 10 segredos já custeados no Bloco 1.

## OWASP Top 10 (2021), item por item

| Item | Risco no Rufus | Medida |
| --- | --- | --- |
| A01 Quebra de controle de acesso | Cliente ver a conta de outro, atendente decidir Pix | ABAC em toda rota de cliente, RBAC em toda rota `/admin`, testes de autorização por rota no CI, ids em UUID (não sequenciais) |
| A02 Falhas de criptografia | Vazamento de CPF, senha ou token | TLS 1.2 ou superior no ALB, Argon2id para senha, CPF e data de nascimento cifrados no banco, RDS e S3 cifrados em repouso com KMS, token de renovação guardado só como hash |
| A03 Injeção | SQL injection no extrato ou na busca de cliente | Kysely com parâmetros em toda consulta (sem concatenar SQL), validação de entrada com DTOs, regras gerenciadas de SQL injection no WAF |
| A04 Design inseguro | Golpe da falsa central, Pix por engano | Confirmação falada do recebedor (RF009), limites para destinatário novo e noturno (RF019), "bloquear tudo agora" (RF020), atendimento só de dentro do app (RF024) |
| A05 Configuração insegura | Porta do banco exposta, `/docs` em produção, cabeçalho revelando framework | Banco e tarefas em subnet privada, `/docs` desligado em produção, cabeçalho `X-Powered-By` removido, container sem root e com disco só de leitura |
| A06 Componentes vulneráveis | Dependência npm com falha conhecida | `npm audit` e Trivy bloqueando alta e crítica no CI (RNF06), Dependabot abrindo PR de atualização toda semana |
| A07 Falhas de identificação e autenticação | Força bruta na senha de 6 números, roubo de sessão | Bloqueio após 5 erros (RF004), limite por IP no WAF, aparelho vinculado com assinatura, token curto, renovação de uso único com revogação em caso de reuso |
| A08 Falhas de integridade de software e dados | Webhook falso dizendo que um Pix chegou, imagem adulterada | Webhook com assinatura HMAC conferida e idempotente pelo `idEvento`, imagem com tag igual ao hash do commit e publicada só pelo pipeline, `package-lock.json` com `npm ci` |
| A09 Falhas de log e monitoramento | Golpe ou invasão percebidos só pela reclamação | Log estruturado com correlação em 100% das requisições (RNF13), auditoria de toda ação de funcionário por 5 anos (RNF14), alarmes do item 6.5 |
| A10 SSRF | API buscar uma URL enviada pelo usuário (imagem da meta, áudio do chamado) | A API não baixa URL arbitrária: imagem e áudio sobem para o S3 por URL pré-assinada, e a saída da rede só vai para os domínios do parceiro e do Expo |
