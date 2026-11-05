# 6.3 Containerização

Um Dockerfile por serviço, os dois com build em 3 estágios, e um Docker Compose que sobe banco, API e worker no computador do dev. Testado em 04/11/2026: as duas imagens compilam, o `docker compose up --build` aplica o schema do Bloco 5, `/health` responde 200 e o worker processa um evento do outbox.

| Arquivo | Serviço |
| --- | --- |
| [codigo/docker/api.Dockerfile](../codigo/docker/api.Dockerfile) | API (porta 3000) |
| [codigo/docker/worker.Dockerfile](../codigo/docker/worker.Dockerfile) | Worker do outbox (sem porta) |
| [codigo/docker-compose.yml](../codigo/docker-compose.yml) | Ambiente local: PostgreSQL 17, API e worker |

## Os 3 estágios

| Estágio | Base | O que faz | Vai para a imagem final? |
| --- | --- | --- | --- |
| `build` | node:22-alpine | `npm ci` com tudo e compila o TypeScript | Só a pasta `dist/` |
| `deps` | node:22-alpine | `npm ci --omit=dev`, só dependências de produção | Só `node_modules/` |
| `final` | node:22-alpine | Junta `dist/` e `node_modules/`, roda como usuário `node` (sem root) | É a imagem |

Resultado: compilador, testes e ferramentas de lint ficam fora da imagem de produção. Menos coisa instalada é menos vulnerabilidade para o Trivy encontrar (RNF06). As duas imagens ficaram com 286 MB no build local.

## Escolhas

| Escolha | Alternativa descartada | Por quê |
| --- | --- | --- |
| Dois Dockerfiles, mesmo código | Uma imagem só com comando diferente | O enunciado pede um por serviço, e assim cada um tem a sua variável `SERVICO`, o seu healthcheck e pode mudar de base sem afetar o outro |
| `node:22-alpine` | `node:22` (Debian completo) | Imagem base bem menor, com menos pacotes para manter atualizados |
| Rodar como usuário `node` | Root, padrão do Docker | Se alguém explorar a API, não tem root dentro do container (OWASP A05) |
| Sistema de arquivos só de leitura na AWS (`readonlyRootFilesystem` nas definições de tarefa) | Gravável | A API não grava em disco: log vai para a saída padrão e arquivo vai para o S3 |
| Healthcheck no container e no ALB batendo em `/health` | Só checar se o processo está vivo | `/health` testa o banco também: tarefa sem banco sai da rotação do balanceador |
| SQL do Bloco 5 montado em `/docker-entrypoint-initdb.d` no Compose | Banco vazio e migração manual | O dev tem o banco com schema e dados de exemplo no primeiro `up` |

## Compose de desenvolvimento

```
cd codigo
cp .env.example .env
docker compose up --build
```

| Serviço | Imagem | Porta no seu computador | Depende de |
| --- | --- | --- | --- |
| banco | postgres:17-alpine | 5432 | |
| api | build de `api.Dockerfile` | 3000 | banco saudável (`pg_isready`) |
| worker | build de `worker.Dockerfile` | nenhuma | banco saudável |

O contrato OpenAPI é montado só no Compose (`/contrato/openapi.yaml`) para o Swagger UI em `/docs`. Em produção o `/docs` não é publicado.
