# 8.1 README do desenvolvedor (do clone ao localhost)

O README completo está em [codigo/README.md](../codigo/README.md), que é o primeiro arquivo que o dev abre. Ele cobre: o que instalar, os 4 comandos do clone ao sistema no ar, onde fica cada coisa, como rodar testes e lint, e os problemas comuns.

Resumo dos comandos:

```
git clone https://github.com/pethrus07/aps-projeto-final-rufus-bank.git
cd aps-projeto-final-rufus-bank/codigo
cp .env.example .env
docker compose up --build
```

Depois disso, http://localhost:3000/health responde e http://localhost:3000/docs mostra o contrato da API.

## Prova de que funciona

Executado em 04/11/2026 numa máquina com Docker 29.6.2, a partir de um volume vazio (`docker compose down -v` antes):

```
$ curl -si http://localhost:3000/health
HTTP/1.1 200 OK
X-Correlation-Id: dd340018-b12b-400f-94c0-3a87972b7fba
{"status":"ok","banco":"ok","versao":"dev"}

$ curl -s -o /dev/null -w "docs %{http_code}\n" http://localhost:3000/docs/
docs 200
```

O Swagger UI em `/docs` carregou as **50 operações** do contrato. No log do banco, os dois arquivos do Bloco 5 rodaram na primeira subida:

```
banco-1 | running /docker-entrypoint-initdb.d/001_schema.sql
banco-1 | running /docker-entrypoint-initdb.d/002_seed_dev.sql
```

E o worker processou um evento de teste inserido no outbox:

```
$ psql -c "insert into rufus.outbox_evento (tipo, agregado_id, payload) values ('ExemploPing', gen_random_uuid(), '{}')"
worker-1 | {"level":30,...,"servico":"rufus-worker","eventoId":"1","msg":"ping recebido"}
$ psql -c "select count(*) filter (where processado_em is not null) from rufus.outbox_evento"
1
```

Testes e lint do esqueleto, no mesmo dia:

```
$ npm run lint        (sem erros)
$ npm run typecheck   (sem erros)
$ npm run test:cov
Tests:       12 passed, 12 total
All files    |   99.25 |    89.28 |   94.44 |   99.02 |
$ npm audit --omit=dev --audit-level=high
found 0 vulnerabilities
```

## O que o dev encontra no dia 1

| Já pronto | Entra no Sprint 1 |
| --- | --- |
| API NestJS com `/health`, log estruturado e correlação | Casos de uso dos módulos (`bloco-8-dev/06-sprint-1.md`) |
| Os 8 módulos com pastas, `index.ts` público e README | App mobile com Expo (`codigo/mobile/README.md`) |
| Worker com o laço do outbox, nova tentativa e espera crescente | Painéis internos com Vite (`codigo/admin/README.md`) |
| Banco com o schema completo do Bloco 5 e dados de exemplo | Terraform da AWS e migrações versionadas |
| Contrato OpenAPI validado e navegável | Cliente da API gerado a partir do contrato |
| CI e CD em GitHub Actions, Dockerfiles, `.env.example` | |
