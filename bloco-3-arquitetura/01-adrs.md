# 3.1 Architecture Decision Records (ADR)

Um ADR por decisão relevante. Cada um tem contexto, decisão, alternativas descartadas com o motivo e consequências. Os motivos saem dos requisitos do Bloco 2 (RF e RNF) e das premissas do Bloco 1, nunca de "é popular" ou "conhecemos".

| ADR | Decisão | Status |
| --- | --- | --- |
| [ADR-001](#adr-001--monolito-modular-e-não-microsserviços) | Monolito modular | Aceito |
| [ADR-002](#adr-002--parceiro-baas-atrás-de-uma-porta-com-adaptador) | Parceiro BaaS atrás de uma porta com adaptador | Aceito |
| [ADR-003](#adr-003--rest-com-json-e-contrato-openapi-30) | REST com JSON e contrato OpenAPI 3.0 | Aceito |
| [ADR-004](#adr-004--backend-em-typescript-com-nestjs-sobre-nodejs-22) | Backend em TypeScript com NestJS sobre Node.js 22 | Aceito |
| [ADR-005](#adr-005--app-em-react-native-com-expo) | App em React Native com Expo | Aceito |
| [ADR-006](#adr-006--postgresql-17-no-amazon-rds-multi-az) | PostgreSQL 17 no Amazon RDS Multi-AZ | Aceito |
| [ADR-007](#adr-007--razão-contábil-com-partidas-dobradas) | Razão contábil com partidas dobradas | Aceito |
| [ADR-008](#adr-008--eventos-por-outbox-transacional-no-próprio-postgresql) | Eventos por outbox transacional no próprio PostgreSQL | Aceito |
| [ADR-009](#adr-009--containers-no-ecs-fargate) | Containers no ECS Fargate | Aceito |
| [ADR-010](#adr-010--autenticação-própria-com-jwt-curto-e-celular-vinculado) | Autenticação própria com JWT curto e celular vinculado | Aceito |
| [ADR-011](#adr-011--voz-gerada-no-servidor-com-cache) | Voz gerada no servidor, com cache | Aceito |
| [ADR-012](#adr-012--painéis-internos-servidos-pela-própria-api) | Painéis internos servidos pela própria API | Aceito |
| [ADR-013](#adr-013--aws-na-região-de-são-paulo) | AWS na região de São Paulo | Aceito |

---

## ADR-001 · Monolito modular, e não microsserviços

**Contexto.** O MVP atende 10.000 usuários ativos por mês com picos de 100 requisições por segundo (RNF04). A equipe tem 2 desenvolvedores de backend (Bloco 7). Os módulos (contas, Pix, família, antifraude, atendimento) trocam dados o tempo todo e várias operações precisam mexer em mais de um deles na mesma transação: um Pix debita a carteira, passa pelo antifraude e grava o evento de notificação (RNF11, zero Pix duplicado).

**Decisão.** Uma aplicação única (API) e um worker, os dois do mesmo código, divididos em módulos com fronteiras explícitas: cada módulo só expõe um serviço público e só ele escreve nas próprias tabelas. Um único banco PostgreSQL.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Microsserviços, um por módulo | Cada serviço teria o próprio banco, e o Pix viraria uma transação distribuída entre 3 serviços (saga com compensação em cada um). Para 100 req/s não há ganho de escala que pague isso. Exigiria 6 bancos ou mais, o que muda o custo do Bloco 1. 2 devs de backend não sustentam a operação de vários serviços |
| Monolito sem módulos | Resolve hoje, mas mistura as regras de antifraude com as de conta e impede extrair um módulo depois |

**Consequências.** Transações locais garantem o RNF11 com uma transação do banco. Deploy único e simples. Se um módulo precisar escalar sozinho (o antifraude, por exemplo), ele já tem fronteira e pode virar serviço. Risco: alguém acessar a tabela de outro módulo. Mitigação: regra de lint de dependência entre módulos no pipeline (Bloco 6).

---

## ADR-002 · Parceiro BaaS atrás de uma porta com adaptador

**Contexto.** Conta, Pix e boleto dependem de um parceiro autorizado pelo Banco Central (Bloco 1). O parceiro ainda não está contratado e existe o risco de não conseguir ou de precisar trocar (risco R04).

**Decisão.** Padrão Portas e Adaptadores (arquitetura hexagonal) para tudo que é externo. O domínio conversa com interfaces nossas (`PortaBancaria`, `PortaVoz`, `PortaNotificacao`, `PortaIdentidade`). Cada fornecedor ganha um adaptador que traduz o modelo dele para o nosso (camada anticorrupção). Em desenvolvimento e teste roda um adaptador falso, sem rede.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Usar o SDK do parceiro direto nos serviços | Prende o domínio ao parceiro. Trocar de parceiro (R04) obrigaria a reescrever Pix, boleto e conta |
| Contratar um agregador de vários bancos | Coloca mais um intermediário cobrando por transação. Não elimina a dependência, só muda de fornecedor |

**Consequências.** Trocar de parceiro vira escrever um adaptador novo. O dev pode rodar tudo no localhost sem contrato assinado. Custo: uma camada a mais de tradução para manter.

---

## ADR-003 · REST com JSON e contrato OpenAPI 3.0

**Contexto.** Os clientes da API são o app mobile e os painéis web. Os parceiros BaaS do mercado expõem REST e avisam eventos por webhook HTTP. O enunciado pede contrato OpenAPI 3.0 (Bloco 8).

**Decisão.** API REST com JSON, versionada no caminho (`/v1`), descrita em OpenAPI 3.0. Operações que movem dinheiro exigem o cabeçalho `Idempotency-Key`.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| gRPC | O ganho de desempenho do protocolo binário não é necessário para 100 req/s com p95 de 300 ms (RNF01). Navegador não fala gRPC sem proxy, e os painéis web precisariam de gRPC-Web. Webhooks do parceiro são HTTP de qualquer forma |
| GraphQL | As telas são simples e fixas, por isso não há o problema de buscar dados demais. Dificulta cache e limite por rota no WAF. Idempotência por operação é mais natural em REST |

**Consequências.** O cliente do app é gerado a partir do OpenAPI, então o contrato não diverge do código. Ferramentas de teste e de documentação (Swagger UI) prontas.

---

## ADR-004 · Backend em TypeScript com NestJS sobre Node.js 22

**Contexto.** A carga é de entrada e saída (banco, parceiro, voz), não de cálculo pesado. Precisamos de tipagem forte para dinheiro e de módulos com fronteira clara (ADR-001). O app mobile é em TypeScript (ADR-005). Cada tarefa no Fargate tem 1 GB de memória (custo do Bloco 1).

**Decisão.** Node.js 22 LTS, TypeScript em modo estrito e framework NestJS. Valores em dinheiro sempre em centavos inteiros (`bigint` no banco).

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Java 21 com Spring Boot | Muito usado em bancos e igualmente adequado. Descartado porque uma aplicação Spring com JVM costuma precisar de mais memória por tarefa que os 1 GB custeados, e porque exigiria uma segunda linguagem na equipe: os tipos do contrato não seriam compartilhados com o app |
| Go | Ótimo desempenho e baixo consumo de memória, mas sem framework modular equivalente ao NestJS: módulos, injeção de dependência e validação teriam de ser montados à mão. Mesma questão da segunda linguagem |

**Consequências.** Uma linguagem só no app, na API e no worker. O NestJS dá módulos, injeção de dependência (que permite trocar adaptadores do ADR-002) e validação de entrada. Cuidado: número em JavaScript perde precisão acima de 2^53, por isso dinheiro trafega como inteiro em centavos e o banco usa `bigint`.

---

## ADR-005 · App em React Native com Expo

**Contexto.** Android e iOS (RNF10), celular de entrada com 3 GB de RAM, leitor de tela TalkBack e VoiceOver obrigatório (RNF09), câmera para boleto (RF013), biometria (RF003).

**Decisão.** React Native com Expo, em TypeScript.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Flutter | Desenha a própria interface em vez de usar os componentes nativos, então a acessibilidade depende de anotar a árvore de semântica em cada widget. No React Native os componentes já são os nativos e o TalkBack e o VoiceOver os leem sem trabalho extra, que é o RNF mais importante do produto. Também usaria Dart, uma segunda linguagem |
| Dois apps nativos (Kotlin e Swift) | Melhor acesso a cada plataforma, mas dobra o trabalho mobile e exige dois perfis diferentes na equipe |

**Consequências.** Um código para os dois sistemas. Biometria, câmera e armazenamento seguro (Keystore e Keychain) por bibliotecas do Expo. Atualização de correção sem esperar a loja (EAS Update), útil para corrigir texto de acessibilidade.

---

## ADR-006 · PostgreSQL 17 no Amazon RDS Multi-AZ

**Contexto.** Dinheiro exige transação ACID entre várias linhas (RNF11), chaves estrangeiras e restrições. Disponibilidade de 99,9% (RNF03) e RPO de 5 minutos (RNF12).

**Decisão.** PostgreSQL 17 gerenciado no Amazon RDS, com réplica síncrona em outra zona (Multi-AZ). A comparação completa com a alternativa descartada e o modelo estão no Bloco 5.

**Alternativas descartadas.** MongoDB (documento) e Amazon Aurora PostgreSQL. Motivos detalhados no Bloco 5, item 5.1.

**Consequências.** Failover automático para a réplica. Backup com restauração a qualquer ponto dos últimos 35 dias. Custo já no Bloco 1 (US$ 227,40 por mês em produção).

---

## ADR-007 · Razão contábil com partidas dobradas

**Contexto.** Saldo errado é o pior erro possível para o público do Rufus. A diferença entre o nosso registro e o do parceiro precisa ser detectada em até 24 horas (RNF11).

**Decisão.** Toda movimentação gera lançamentos em partidas dobradas: cada transação tem pelo menos um débito e um crédito, e a soma é zero. O saldo de uma carteira é a soma dos lançamentos dela, nunca um número editado. Um gatilho no banco recusa transação desequilibrada.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Coluna `saldo` atualizada a cada operação | Duas operações ao mesmo tempo podem sobrescrever uma à outra, e quando o saldo diverge não há trilha para explicar o porquê |
| Guardar só o saldo informado pelo parceiro | Deixa o Rufus sem registro próprio para conciliar e para mostrar o extrato quando o parceiro está fora |

**Consequências.** Extrato e auditoria saem do mesmo registro. A conciliação diária compara a soma por carteira com o extrato do parceiro. Custo: a consulta de saldo soma lançamentos; com índice por carteira e saldo de fechamento diário, fica dentro dos 300 ms (RNF01).

---

## ADR-008 · Eventos por outbox transacional no próprio PostgreSQL

**Contexto.** Depois de um Pix é preciso enviar ao parceiro, notificar o cliente, avisar o contato de confiança e o responsável. Se a API gravar o Pix e cair antes de avisar, o aviso se perde. Se avisar antes de gravar, avisa algo que não aconteceu.

**Decisão.** Padrão Transactional Outbox: na mesma transação que grava o Pix, a API grava o evento na tabela `outbox_evento`. O worker lê os eventos pendentes com `FOR UPDATE SKIP LOCKED`, executa e marca como processado, com nova tentativa e espera crescente em caso de erro.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Amazon SQS | Gravar no banco e publicar na fila são duas operações que podem falhar separadas, e o problema voltaria. Seria preciso o outbox de qualquer forma |
| Kafka (Amazon MSK) | Feito para milhões de eventos por segundo. Para o volume do Rufus seria um cluster caro e mais uma peça para operar |

**Consequências.** Garantia de "pelo menos uma vez": cada consumidor é idempotente. Nenhum serviço novo na infraestrutura do Bloco 1. Se o volume crescer muito, o worker pode passar a publicar do outbox para uma fila.

---

## ADR-009 · Containers no ECS Fargate

**Contexto.** Duas cargas: a API, sempre ligada e com p95 de 300 ms (RNF01), e o worker, que fica lendo o outbox (ADR-008). 99,9% exige pelo menos 2 zonas (RNF03).

**Decisão.** Amazon ECS com Fargate: containers sem gerenciar servidor, 2 tarefas da API (uma por zona) e 1 do worker, com auto scaling de 2 a 6 tarefas da API.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Kubernetes (EKS) | O plano de controle custa US$ 0,10 por hora por cluster em São Paulo, US$ 73 por mês, e seriam 2 clusters (produção e homologação). Exige uma pessoa que domine Kubernetes. Os recursos extras não são usados por 2 serviços |
| AWS Lambda | O worker fica em execução contínua e a API mantém conexões com o PostgreSQL. Em Lambda, a partida a frio ameaça o p95 de 300 ms e cada execução abriria conexão nova com o banco, exigindo RDS Proxy |
| EC2 com Docker | Mais barato por hora, mas a equipe teria de cuidar de sistema operacional, atualização de segurança e substituição de máquina com defeito |

**Consequências.** O mesmo container roda no localhost (Docker Compose) e na AWS. Custo de containers no Bloco 1: US$ 62,00 por mês em produção.

---

## ADR-010 · Autenticação própria com JWT curto e celular vinculado

**Contexto.** Só um celular ativo por conta e troca de aparelho com selfie (RF005). Senha de 6 números e biometria (RF003, RF004). Sessão segura (RNF05). Funcionários precisam de papéis diferentes (RF030) e de segundo fator.

**Decisão.** Módulo de identidade próprio. No cadastro o app gera um par de chaves no Keystore ou Keychain do celular e envia a chave pública. O login exige senha (guardada com Argon2id) e a assinatura do aparelho. A API emite token de acesso JWT de 15 minutos e token de renovação de 30 dias, trocado a cada uso e guardado só como hash. A biometria destrava a chave no celular e nunca sai dele. Funcionários entram com senha e código TOTP e recebem papéis (RBAC). A relação entre menor e responsável é checada por atributo do vínculo (ABAC).

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Amazon Cognito | Resolve usuário e senha, mas não tem vínculo de um único aparelho com assinatura por chave do celular nem as regras de menor e responsável. Teríamos de escrever essas regras de qualquer forma, e com duas fontes de verdade |
| Sessão no servidor com cookie | App mobile não usa cookie de forma natural e cada requisição consultaria a sessão no banco |

**Consequências.** Controle total do fluxo de troca de aparelho, que é a principal barreira contra golpe (R01). Responsabilidade maior: o módulo de identidade tem a meta de cobertura de testes mais alta (Bloco 9).

---

## ADR-011 · Voz gerada no servidor, com cache

**Contexto.** Toda tela precisa poder ser ouvida (RF007, RNF09). Os celulares de entrada nem sempre têm voz em português instalada e a qualidade varia de aparelho para aparelho.

**Decisão.** A API gera o áudio com o Amazon Polly. Frases fixas (instruções de tela) são geradas uma vez e guardadas no S3. Frases com dados (saldo, nome do recebedor) são geradas na hora e não são guardadas. Se o celular estiver sem internet, o app usa a voz do próprio aparelho.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Só a voz do celular | Custo zero, mas a voz pode faltar ou soar diferente em cada aparelho. Para quem depende do áudio, a voz é a interface |
| Gravar todas as frases com locutor | Não cobre frases com dados (valores, nomes) |

**Consequências.** Mesma voz em todos os aparelhos. Custo no Bloco 1: US$ 48 por mês para 12 milhões de caracteres. A tabela de preços de São Paulo lista só a voz padrão do Polly; a voz neural fica como melhoria.

---

## ADR-012 · Painéis internos servidos pela própria API

**Contexto.** SAC, antifraude e administração precisam de painéis web (RF025, RF027, RF030). São poucos usuários internos.

**Decisão.** Uma aplicação React (Vite) compilada como arquivos estáticos e servida pela API em `/admin`. O acesso ao caminho `/admin` só é aceito a partir dos IPs da empresa (regra do WAF), com senha e TOTP.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Hospedar no S3 com CloudFront | Mais uma distribuição para configurar e proteger, para poucos usuários internos |
| Ferramenta pronta de painel (low-code) | Os dados de cliente sairiam para um terceiro, o que piora o risco R02 e a LGPD |

**Consequências.** Nenhum serviço novo na infraestrutura. O painel usa a mesma API, com rotas `/v1/admin` protegidas por papel.

---

## ADR-013 · AWS na região de São Paulo

**Contexto.** Os dados são de brasileiros, incluindo menores e biometria. A latência para o usuário afeta o RNF01. Todos os serviços da arquitetura precisam estar na mesma região.

**Decisão.** AWS, região sa-east-1 (São Paulo), para todos os ambientes em nuvem.

**Alternativas descartadas.**

| Alternativa | Por que não |
| --- | --- |
| Região dos EUA (us-east-1), mais barata | Dados pessoais fora do país pedem salvaguardas de transferência internacional na LGPD (art. 33) e somam latência de ida e volta a cada requisição |
| Outra nuvem com região em São Paulo (GCP ou Azure) | Também atenderia à latência. Ficamos com a AWS porque todos os serviços escolhidos (Fargate, RDS PostgreSQL Multi-AZ, Polly, WAF, Secrets Manager) existem na região de São Paulo e têm preço publicado na tabela oficial, que o script do Bloco 1 consulta para recalcular o custo a cada mudança |

**Consequências.** Preço mais alto que nos EUA, já refletido no custo do Bloco 1.
