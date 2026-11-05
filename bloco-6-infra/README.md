# Bloco 6 · Infraestrutura e DevOps

| Item | Resumo |
| --- | --- |
| [6.1 Diagrama de infraestrutura e custo por ambiente](01-diagrama-de-infra.md) | Produção roda na AWS em São Paulo (ADR-013), em 2 zonas de disponibilidade, com balanceador, 2 tarefas da API, banco Multi-AZ e 1 NAT por zona. |
| [6.2 Pipeline CI/CD](02-pipeline-ci-cd.md) | Oito etapas, do lint à produção, cada uma com o seu critério de bloqueio. |
| [6.3 Containerização](03-containerizacao.md) | Um Dockerfile por serviço, os dois com build em 3 estágios, e um Docker Compose que sobe banco, API e worker no computador do dev. |
| [6.4 Segurança](04-seguranca.md) | Autenticação com JWT e celular vinculado, RBAC e ABAC, segredos no Secrets Manager e OWASP Top 10 item por item. |
| [6.5 Observabilidade](05-observabilidade.md) | Log estruturado com correlação, métricas técnicas e de negócio e alertas com limiar ligado aos RNFs. |

Os arquivos reais (Dockerfiles, docker-compose, workflows do CI/CD e definições de tarefa do ECS) estão em [../codigo/](../codigo/).
