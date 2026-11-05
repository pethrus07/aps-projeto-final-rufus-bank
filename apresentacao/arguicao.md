# Preparação para a arguição

O professor escolhe qualquer integrante e pergunta sobre qualquer parte. Não existe "essa parte foi do colega". Abaixo, as 7 perguntas do slide 18 do enunciado e outras prováveis, cada uma com a resposta curta (para falar em 30 segundos) e onde está a prova no projeto.

Regra para ensaiar: cada um responde em voz alta todas as perguntas, sem ler. Se travar, volta ao bloco indicado.

## As 7 perguntas do enunciado

### 1. Por que vocês não usaram MongoDB nesse sistema?

Porque o sistema move dinheiro. Um Pix grava a transação, pelo menos dois lançamentos (débito e crédito) e o evento de notificação, e tudo tem de dar certo junto ou nada (RNF11, zero Pix duplicado). No PostgreSQL isso é uma transação ACID com chave estrangeira, restrição única de idempotência e um gatilho que recusa lançamento desequilibrado. No MongoDB a integridade entre documentos ficaria no código da aplicação. O nosso dado é relacional por natureza: cliente, conta, carteira, lançamento, transação.

Onde está: ADR-006 (Bloco 3) e item 5.1 do Bloco 5.

### 2. Se a demanda triplicar, o que muda na arquitetura?

Pouca coisa, e nada de estrutura. Hoje a meta é 10.000 usuários e picos de 100 req/s. Com o triplo:
- a API já tem auto scaling de 2 a 6 tarefas no Fargate (Bloco 6), então só cresce o número de tarefas;
- o banco sobe de db.t4g.medium para db.m7g.large, que já tem preço na mesma tabela (US$ 0,442 por hora em Multi-AZ);
- se a leitura de extrato pesar, entra uma réplica de leitura.

Não viramos microsserviços por causa de volume. Isso só aconteceria se um módulo, como o antifraude, precisasse escalar sozinho, e ele já tem fronteira para ser extraído (ADR-001).

### 3. O que acontece se o banco de dados cair? A infra de vocês cobre isso?

Cobre. O RDS está em Multi-AZ: uma réplica síncrona em outra zona de disponibilidade assume automaticamente, em geral em um ou dois minutos, com o mesmo endereço. A API reconecta sozinha. Se a falha for de dado (alguém apagou algo), restauramos a qualquer ponto dos últimos 35 dias, com perda máxima de 5 minutos (RPO, RNF12) e volta em até 1 hora (RTO). O restore é testado a cada 3 meses. E o outbox (ADR-008) garante que nenhum evento se perde: o que não foi processado continua na tabela.

Onde está: RNF03 e RNF12 (Bloco 2), estratégia de backup (Bloco 5), diagrama de infra (Bloco 6).

### 4. Esse diagrama de classes tem herança aqui. Por que não usou composição?

A herança está só em `Transacao` com os subtipos `PixEnvio`, `PixRecebimento`, `PagamentoBoleto` e `MovimentoMeta`. É herança porque a relação é "é um": um Pix **é uma** transação e compartilha o mesmo ciclo de vida (o padrão State: PENDENTE, RETIDA, ENVIADA, CONCLUIDA, RECUSADA, ESTORNADA), a mesma chave de idempotência e os mesmos lançamentos. Onde a relação é "tem um" e a parte não existe sem o todo, usamos composição: `Chamado` e `MensagemChamado`, `Conta` e `Carteira`, `Transacao` e `Lancamento`. Onde a parte vive sem o todo, agregação: `Conta` e `ChavePix` (a chave pode ser excluída e a conta continua).

Onde está: modelo de domínio (Bloco 3, item 3.5) e diagrama de classes (Bloco 4).

### 5. Vocês marcaram LGPD nos RNFs. No dicionário de dados, quais campos são PII?

Dado pessoal: nome completo, CPF, data de nascimento, celular e e-mail do cliente; nome e celular do contato de confiança; dados do recebedor de Pix (nome e documento mascarado); conteúdo das mensagens do chamado; IP no registro de auditoria. Dado pessoal sensível: a biometria, que **não fica no nosso banco**, porque a digital e o rosto são verificados no próprio celular. A selfie da abertura de conta vai para o parceiro validar. CPF e data de nascimento são cifrados em repouso, com um hash à parte para permitir busca. Cada coluna está marcada no dicionário, que é gerado do próprio banco.

Onde está: RNF07, dicionário de dados e estratégia LGPD (Bloco 5).

### 6. Se precisar adicionar pagamento por PIX depois, o que muda na arquitetura?

No Rufus o Pix já é o meio principal, então a pergunta vale para qualquer novo meio de pagamento (TED, cartão). O que muda:
- um novo subtipo de `Transacao` com o mesmo ciclo de vida;
- um novo método na `PortaBancaria`, implementado no adaptador do parceiro (ADR-002);
- uma nova rota no contrato OpenAPI.

O razão contábil, o antifraude (que avalia por regras plugáveis, padrão Strategy) e o outbox não mudam.

### 7. O SLA de vocês é 99,9%. A infra desenhada garante isso como?

99,9% são até 43 minutos fora do ar por mês. Cada camada tem redundância em 2 zonas de disponibilidade:
- o Application Load Balancer distribui entre 2 tarefas da API, uma em cada zona;
- se uma tarefa falhar no health check, o ECS sobe outra;
- o banco é Multi-AZ, com failover automático;
- há 2 NAT Gateways, um por zona, para a API continuar falando com o parceiro BaaS se uma zona cair.

Tudo isso está no custo do Bloco 1 (o NAT duplo custa US$ 137,64 por mês justamente por isso). Uma verificação externa a cada minuto mede a disponibilidade de verdade.

## Outras perguntas prováveis

| Pergunta | Resposta curta | Onde |
| --- | --- | --- |
| Por que monolito e não microsserviços? | 100 req/s e 2 devs de backend não pagam o custo de vários serviços e bancos. Monolito modular dá fronteira sem transação distribuída | ADR-001 |
| Por que REST e não gRPC? | O ganho do gRPC não é necessário para 300 ms de p95. O navegador dos painéis não fala gRPC sem proxy. Os parceiros usam webhook HTTP | ADR-003 |
| Por que React Native e não Flutter? | Acessibilidade: componentes nativos lidos pelo TalkBack e VoiceOver sem anotação extra. Mesma linguagem da API | ADR-005 |
| Por que ECS e não Kubernetes ou Lambda? | EKS custa US$ 73 por cluster por mês e exige especialista. Lambda tem partida a frio contra o p95 e não serve para o worker contínuo | ADR-009 |
| Por que AWS? | Todos os serviços da arquitetura existem em São Paulo com preço oficial publicado. Dados no Brasil e menor latência | ADR-013 |
| Como evitam Pix duplicado? | Chave de idempotência por conta com restrição única no banco. O segundo pedido devolve o resultado do primeiro | RNF11, US07 |
| E se o parceiro BaaS cair no meio do Pix? | Saga orquestrada: a reserva de saldo é compensada (estorno) e o cliente é avisado. Diagrama de sequência do erro crítico | Bloco 4 |
| Como o saldo nunca fica errado? | Partidas dobradas: o saldo é a soma dos lançamentos e um gatilho recusa transação que não soma zero. Conciliação diária com o parceiro | ADR-007 |
| Por que normalizar até a 3FN? | Evita o mesmo dado em dois lugares e a divergência entre eles. Desnormalizamos de propósito só onde há ganho medido | Bloco 5 |
| Como funciona a conta da Camila? | Conta de menor criada pela `FabricaDeConta`, vinculada ao responsável, que aceita os termos, define limites e aprova pedidos | RF014 a RF016 |
| Como o app ajuda contra golpe? | Um celular por conta, confirmação falada do recebedor, limite para destinatário novo e à noite, "bloquear tudo agora", contato de confiança, aviso de que o Rufus nunca liga | RF005, RF009, RF019 a RF021 |
| De onde vem o custo de infra? | Tabela oficial da AWS para São Paulo, lida por um script que para com erro se faltar preço. Dólar pela PTAX do Banco Central | Bloco 1, item 4.3 |
| O dev consegue começar amanhã? | Sim: o README leva do clone ao localhost com Docker Compose, o banco sobe com o DDL, a API responde em /health e o contrato abre em /docs. O Sprint 1 está detalhado | Bloco 8 |
