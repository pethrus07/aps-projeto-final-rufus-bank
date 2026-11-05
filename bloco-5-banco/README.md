# Bloco 5 · Banco de Dados

Do modelo conceitual ao SQL executável. A escolha do banco vem da arquitetura (ADR-006, ADR-007, ADR-008) e dos requisitos (RNF07, RNF11, RNF12, RNF14).

| Item do enunciado | Arquivo |
| --- | --- |
| Decisão do banco (escolhido x descartados x motivo) | [01-decisao.md](01-decisao.md) |
| Modelo conceitual (ER) | [02-modelo-conceitual.md](02-modelo-conceitual.md) |
| Modelo lógico (tabelas, tipos, PK, FK, índices justificados) | [03-modelo-logico.md](03-modelo-logico.md) |
| Modelo físico (CREATE TABLE executável) | [sql/001_schema.sql](sql/001_schema.sql) e dados de desenvolvimento em [sql/002_seed_dev.sql](sql/002_seed_dev.sql) |
| Dicionário de dados (gerado do catálogo) | [04-dicionario-de-dados.md](04-dicionario-de-dados.md) |
| Estratégia (backup, LGPD, migrações sem downtime) | [05-estrategia.md](05-estrategia.md) |

## Prova de que o SQL executa

O modelo físico foi aplicado num **PostgreSQL 17.11 real** (container `postgres:17-alpine`) e testado com 21 casos: 6 que devem ser aceitos e 15 que o banco deve recusar (lançamento desequilibrado, segundo celular ativo, Pix com a mesma chave de idempotência, valor negativo, alteração do razão, apagar auditoria, entre outros). Resultado: **21 de 21 como esperado**. Saída completa em [testes/resultado.txt](testes/resultado.txt).

Para repetir (precisa do Docker em execução):

```
bash bloco-5-banco/testes/testar-schema.sh
python -I bloco-5-banco/ferramentas/gerar_dicionario.py
python -I ferramentas/diagramas/gerar.py bloco-5
```

O primeiro comando roda os testes. O segundo regera o dicionário de dados e as fontes dos 3 diagramas lógicos a partir do catálogo. O terceiro desenha os diagramas com título, autores e data.

## Números do modelo

27 tabelas, 170 colunas, 26 colunas com marcação LGPD, 26 índices criados com CREATE INDEX (além dos que as chaves primárias e as restrições UNIQUE criam sozinhas), 3 gatilhos (partidas dobradas, razão imutável, auditoria imutável).
