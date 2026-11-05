# 6.2 Pipeline CI/CD

Oito etapas, sempre nesta ordem: **lint, testes, build, segurança, homologação, smoke test, aprovação, produção**. Cada etapa tem um critério de bloqueio: se ele falhar, nada segue para a próxima. Os arquivos reais estão em [codigo/.github/workflows/ci.yml](../codigo/.github/workflows/ci.yml) e [cd.yml](../codigo/.github/workflows/cd.yml), no GitHub Actions (stack, Bloco 3).

```
pull request ─► 1 lint ─► 2 testes ─► 3 build ─► 4 segurança ─► merge na main
                                                                    │
main ─► 5 publicar no ECR ─► 6 homologação ─► 7 smoke ─► 8 aprovação ─► produção ─► smoke em produção
```

## Etapas e critérios de bloqueio

| # | Etapa | O que roda | Bloqueia quando | Ligado a |
| --- | --- | --- | --- | --- |
| 1 | Lint e tipos | ESLint, `tsc --noEmit`, `redocly lint` do contrato | Qualquer erro de lint, inclusive import entre módulos (ADR-001), erro de tipo ou contrato OpenAPI inválido | Guia de padrões (Bloco 8) |
| 2 | Testes | Jest de unidade e integração contra um PostgreSQL 17 real com o schema do Bloco 5 | Qualquer teste falhando ou cobertura de linhas abaixo de 80% | Bloco 9 |
| 3 | Build | `docker build` das imagens da API e do worker | Imagem que não compila | Containerização (6.3) |
| 4 | Segurança | `npm audit --audit-level=high`, gitleaks no histórico, Trivy nas duas imagens | Vulnerabilidade alta ou crítica com correção disponível, ou segredo encontrado no código | RNF06, R02 |
| 5 | Publicar | Build e envio das imagens para o ECR, com a tag igual ao hash do commit | Só começa se as etapas 1 a 4 ficaram verdes | |
| 6 | Homologação | Migração do banco (só a parte que expande, Bloco 5) e atualização dos serviços no ECS | As tarefas novas não passam no `/health` do balanceador. O circuit breaker do ECS desfaz o deploy sozinho | RNF03 |
| 7 | Smoke test | `/health` com a versão certa e carga curta com k6 (20 usuários por 30 s) | `/health` diferente de 200, versão diferente do commit, p95 acima de 300 ms ou mais de 1% de erro | RNF01 |
| 8 | Aprovação e produção | Aprovação manual de 1 revisor (que não seja o autor) no ambiente `producao` do GitHub, depois o mesmo deploy da etapa 6 e um `/health` final | Sem aprovação nada sai. Smoke de produção falhando abre incidente e a task definition anterior é reaplicada | |

## Decisões do pipeline

| Decisão | Alternativa descartada | Por quê |
| --- | --- | --- |
| Credenciais da AWS por OIDC, com uma role por ambiente | Chave de acesso guardada nos segredos do GitHub | Chave fixa vaza e não expira. Com OIDC o GitHub recebe uma credencial temporária a cada execução (R02) |
| A mesma imagem vai de homologação para produção | Fazer build de novo para produção | O que foi testado em homologação é exatamente o que sobe |
| Deploy rolling com 100% das tarefas saudáveis no mínimo | Parar tudo e subir de novo | Zero tempo fora do ar a cada versão (RNF03) |
| Migração só "expandir" antes do deploy | Migração que apaga coluna junto com o deploy | A versão antiga continua funcionando enquanto a nova sobe (Bloco 5, migrações sem downtime) |
| Aprovação humana antes de produção | Deploy automático em produção | Sistema financeiro: um olho humano no que vai para o cliente. A aprovação leva minutos e não trava o resto |

## Onde os workflows ficam

O GitHub só executa workflows na pasta `.github/` da raiz do repositório. Nesta entrega a pasta está em `codigo/.github/` de propósito, para o repositório acadêmico não tentar fazer deploy numa AWS que não existe. Quando `codigo/` virar o repositório do produto, a pasta vai para a raiz sem mudança. As variáveis `AWS_ROLE_ARN` e `REDE_TAREFA` e os ambientes `homologacao` e `producao` (com o revisor obrigatório) são configurados no GitHub pelo Tech Lead no Sprint 1.
