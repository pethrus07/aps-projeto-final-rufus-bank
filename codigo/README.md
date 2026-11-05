# Rufus Bank · código

Este é o ponto de partida do desenvolvedor no dia 1: API e worker do backend (Node.js 22, NestJS, TypeScript), banco PostgreSQL 17 e o contrato da API, tudo rodando no seu computador com um comando.

O que já existe é o **esqueleto**: estrutura dos 8 módulos (ADR-001), `/health`, documentação da API em `/docs`, laço do outbox no worker, pipeline de CI/CD, Dockerfiles e banco criado com o schema do Bloco 5. As regras de negócio entram a partir do Sprint 1 (`bloco-8-dev/06-sprint-1.md`).

## 1. O que instalar antes

| Ferramenta | Versão | Para quê |
| --- | --- | --- |
| Git | qualquer recente | clonar o repositório |
| Docker Desktop (ou Docker Engine com Compose v2) | Compose 2.20 ou superior | rodar banco, API e worker |
| Node.js | 22 LTS | rodar testes e lint fora do Docker (opcional para só subir o sistema) |

Confira:

```
git --version
docker compose version
node --version
```

## 2. Do clone ao localhost

```
git clone https://github.com/pethrus07/aps-projeto-final-rufus-bank.git
cd aps-projeto-final-rufus-bank/codigo
cp .env.example .env
docker compose up --build
```

Na primeira vez o Docker baixa as imagens e compila (alguns minutos). Está pronto quando aparecer no log:

```
api-1     | {"level":30,...,"msg":"api no ar"}
worker-1  | {"level":30,...,"msg":"worker no ar"}
```

Abra:

| Endereço | O que é |
| --- | --- |
| http://localhost:3000/health | Saúde da API e do banco. Deve responder `{"status":"ok","banco":"ok",...}` |
| http://localhost:3000/docs | Contrato OpenAPI navegável (Swagger UI), com as 50 rotas |
| `localhost:5432` | PostgreSQL. Usuário `rufus`, senha `rufus_local`, banco `rufus` |

Teste pelo terminal:

```
curl http://localhost:3000/health
```

Para parar: `Ctrl+C` e depois `docker compose down`.

## 3. Banco de dados

Na **primeira** subida o PostgreSQL executa, em ordem, os arquivos de `../bloco-5-banco/sql/` (schema e dados de exemplo). Eles só rodam com o volume vazio. Depois de mudar um SQL, recrie do zero:

```
docker compose down -v
docker compose up --build
```

Para abrir o banco pelo terminal:

```
docker compose exec banco psql -U rufus -d rufus
```

## 4. Rodar testes e lint fora do Docker

```
cd backend
npm ci
npm run lint
npm run typecheck
npm test
```

Para rodar a API fora do Docker (com o banco ainda no Docker), troque `banco` por `localhost` no `DATABASE_URL` do `.env` e use `npm run dev:api`.

## 5. Estrutura

```
codigo/
  backend/                 API e worker (mesmo código, ADR-001)
    src/
      main.ts              partida da API (porta 3000)
      worker/              laço do outbox (ADR-008)
      compartilhado/       configuração, log, banco, correlação
      saude/               GET /health
      modulos/             os 8 módulos, cada um com README
        identidade/  contas/  pagamentos/  familia/
        antifraude/  atendimento/  notificacao/  backoffice/
    test/
  docker/                  api.Dockerfile e worker.Dockerfile (multi-stage)
  .github/workflows/       ci.yml e cd.yml
  docker-compose.yml       ambiente local
  .env.example             todas as variáveis, comentadas
  mobile/                  app React Native com Expo (criado no Sprint 1)
  admin/                   painéis internos React com Vite (criado no Sprint 1)
```

## 6. Onde está cada coisa que você vai precisar

| Preciso de | Está em |
| --- | --- |
| O que fazer primeiro | `bloco-8-dev/06-sprint-1.md` |
| Contrato da API | `bloco-8-dev/openapi.yaml` (e `/docs`) |
| Variáveis de ambiente | `.env.example` e `bloco-8-dev/02-variaveis-de-ambiente.md` |
| Padrões de código | `bloco-8-dev/03-guia-de-padroes-de-codigo.md` |
| Branches, commits e PR | `bloco-8-dev/04-git-workflow.md` |
| Modelo de domínio (nomes de classes e campos) | `bloco-3-arquitetura/05-modelo-de-dominio.md` |
| Decisões de arquitetura | `bloco-3-arquitetura/01-adrs.md` |
| Tabelas e colunas | `bloco-5-banco/` |
| Definition of Ready e Done | `bloco-9-qualidade/` |

## 7. Problemas comuns

| Sintoma | Causa e solução |
| --- | --- |
| `failed to connect to the docker API` | O Docker Desktop está fechado. Abra e espere ficar verde |
| `port is already allocated` na 5432 | Já existe um PostgreSQL na máquina. Pare o outro ou mude a porta em `docker-compose.yml` (`"5433:5432"`) |
| `/health` responde 503 | O banco não está pronto. Veja `docker compose logs banco` |
| Mudei o SQL e nada mudou | Os scripts só rodam com o volume vazio: `docker compose down -v` |
| `Variável de ambiente obrigatória ausente` | Faltou o `cp .env.example .env` |
