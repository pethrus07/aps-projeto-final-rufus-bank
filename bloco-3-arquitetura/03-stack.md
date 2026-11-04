# 3.3 Stack tecnológica

Todas as camadas, cada uma com a escolha, a alternativa descartada e o motivo técnico, ligado ao requisito ou ao ADR de onde veio.

| Camada | Escolha | Alternativa descartada | Motivo técnico |
| --- | --- | --- | --- |
| App mobile | React Native 0.8x com Expo SDK, TypeScript | Flutter | Componentes nativos lidos pelo TalkBack e VoiceOver sem anotação extra (RNF09). Mesma linguagem da API (ADR-005) |
| Armazenamento seguro no celular | Expo SecureStore (Keystore no Android, Keychain no iOS) | AsyncStorage | Token e chave do aparelho precisam de armazenamento cifrado pelo sistema (RNF05, ADR-010) |
| Biometria | expo-local-authentication | Biometria própria | A biometria nativa não tira o dado do celular. Nada biométrico chega ao servidor (risco R08) |
| Leitura de boleto | expo-camera com leitura de código de barras | Biblioteca de terceiros paga | Lê o padrão ITF dos boletos sem custo por leitura (RF013) |
| Painéis internos | React 19 com Vite, TypeScript | Next.js | Painel interno não precisa de renderização no servidor nem de SEO. Arquivos estáticos servidos pela API (ADR-012) |
| API | Node.js 22 LTS, NestJS 11, TypeScript estrito | Java 21 com Spring Boot | Cabe em 1 GB por tarefa, mesma linguagem do app, módulos com injeção de dependência (ADR-004) |
| Validação de entrada | class-validator com DTOs do NestJS | Validação manual | Toda entrada validada antes do domínio, que é o item A03 (injeção) da OWASP |
| Acesso a dados | Kysely (construtor de SQL tipado) com SQL explícito | ORM completo (TypeORM ou Prisma) | O razão contábil usa gatilho, `SELECT ... FOR UPDATE` e `SKIP LOCKED` (ADR-007, ADR-008). SQL explícito evita consulta escondida pelo ORM e deixa o p95 previsível (RNF01) |
| Migrações | Arquivos SQL versionados executados pelo node-pg-migrate | Migração automática do ORM | Migração revisada linha a linha e no padrão expandir e contrair, sem parar o sistema (Bloco 5) |
| Banco de dados | PostgreSQL 17 no Amazon RDS Multi-AZ | MongoDB | Transação ACID entre várias linhas, chave estrangeira e restrição (RNF11, ADR-006, Bloco 5) |
| Fila de eventos | Tabela outbox no PostgreSQL e worker | Amazon SQS | Gravar o dado e o evento na mesma transação (ADR-008) |
| Voz | Amazon Polly e cache no S3 | Só a voz do celular | Mesma voz em todos os aparelhos (ADR-011) |
| Notificação push | Expo Push (sobre FCM e APNs) | Amazon SNS mobile push | Já integrado ao Expo, sem custo por mensagem |
| Autenticação | Módulo próprio: Argon2id, JWT de 15 min, renovação de 30 dias, chave do aparelho | Amazon Cognito | Vínculo de um único aparelho e regras de menor e responsável (ADR-010) |
| Log | pino com saída em JSON para o CloudWatch Logs | Log em texto livre | Log estruturado com identificador de correlação em 100% das requisições (RNF13) |
| Containers | Docker com build em múltiplos estágios | Imagem única com ferramentas de build | Imagem final menor e sem compilador, menos superfície de ataque (RNF06) |
| Execução na nuvem | Amazon ECS com Fargate | Kubernetes (EKS) | Sem custo de plano de controle e sem operar cluster (ADR-009) |
| Rede e borda | Application Load Balancer com AWS WAF | Exposição direta das tarefas | TLS na borda, distribuição entre 2 zonas (RNF03) e regras contra ataques comuns (R02) |
| Segredos | AWS Secrets Manager | Variável de ambiente no código | Segredo fora do repositório, com rotação (R02) |
| Infraestrutura como código | Terraform | Criar recursos pelo console | Ambientes reproduzíveis e revisados em pull request. Homologação e produção com o mesmo código |
| CI/CD | GitHub Actions | Jenkins | O código já está no GitHub e não há servidor de CI para manter |
| Testes | Jest (unidade e integração), Testcontainers (PostgreSQL real), Maestro (E2E mobile), k6 (carga) | Mock do banco em todos os testes | O razão e o outbox só são testados de verdade contra um PostgreSQL real (Bloco 9) |
| Desenvolvimento local | Docker Compose | Ambiente compartilhado na nuvem | Custo zero de desenvolvimento (Bloco 1) e cada dev com o próprio banco |
