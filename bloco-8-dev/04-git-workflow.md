# 8.4 Git workflow

**Trunk-based com branches curtas**: a `main` está sempre pronta para ir a produção, cada mudança nasce numa branch que vive no máximo 2 dias e entra por pull request revisado e com o CI verde.

## Por que esse fluxo

| Escolha | Alternativa descartada | Por quê |
| --- | --- | --- |
| Trunk-based com branches curtas | GitFlow (develop, release, hotfix) | Com deploy contínuo (Bloco 6) não há "versão de release" para estabilizar. Branch longa gera conflito grande, e GitFlow tem 5 tipos de branch para uma equipe de 4 devs (Bloco 7) |
| Squash merge | Merge commit | Cada PR vira 1 commit na `main`, com mensagem no padrão. O histórico fica legível e fácil de reverter |
| Feature flag para o que não está pronto | Segurar a branch até terminar | O código entra cedo, desligado, e não envelhece fora da `main` |

## Branches

| Tipo | Nome | Exemplo |
| --- | --- | --- |
| Funcionalidade | `feat/US<número>-<resumo>` | `feat/US06-pix-com-confirmacao-falada` |
| Correção | `fix/<resumo>` | `fix/extrato-ordem-errada` |
| Tarefa técnica | `chore/<resumo>` | `chore/terraform-vpc` |
| Documentação | `docs/<resumo>` | `docs/adr-014-cache` |

Criada a partir da `main` atualizada. Vida máxima de 2 dias; se passar disso, a história era grande demais e deve ser quebrada.

## Commits: Conventional Commits

```
<tipo>(<módulo>): <o que mudou, no imperativo>

<por que, quando não for óbvio>

Refs: US06
```

| Tipo | Quando |
| --- | --- |
| feat | Comportamento novo para o usuário |
| fix | Correção de defeito |
| refactor | Muda o código sem mudar o comportamento |
| test | Só testes |
| docs | Só documentação |
| chore | Build, dependências, infraestrutura |
| perf | Melhoria de desempenho |

Exemplos: `feat(pagamentos): exige Idempotency-Key no envio de Pix`, `fix(contas): soma do saldo ignorava lançamento estornado`. Mudança que quebra o contrato da API leva `!` (`feat(pagamentos)!: ...`) e o rodapé `BREAKING CHANGE:`.

## Pull request

1. Título no padrão do commit (vira a mensagem do squash).
2. Descrição: o que muda, a história (US) e o critério de aceite atendido, como testar, print da tela quando houver interface.
3. Checklist da Definition of Done (Bloco 9) marcada pelo autor.
4. Pelo menos **1 aprovação** de outra pessoa. Mudança em `identidade`, `contas`, `pagamentos` ou na infraestrutura exige **2 aprovações**, uma delas do Tech Lead.
5. CI verde nos 4 jobs (lint, testes, build, segurança).
6. Até 400 linhas alteradas. Maior que isso, dividir.

## Proteção da main

Configurada no GitHub (Settings, Branches, regra para `main`):

- Proibido push direto, inclusive para administradores.
- Exige pull request com as aprovações acima e descarta aprovação quando chega commit novo.
- Exige os checks `1. lint e tipos`, `2. testes`, `3. build das imagens` e `4. segurança` passando, com a branch atualizada.
- Exige conversas resolvidas.
- Proíbe force push e exclusão da branch.
- `CODEOWNERS` define os revisores obrigatórios por pasta (`/codigo/backend/src/modulos/pagamentos/` para o Tech Lead, por exemplo).

## Versionamento

Versão semântica (`MAJOR.MINOR.PATCH`) para a API e para o app:

| Parte | Sobe quando |
| --- | --- |
| MAJOR | Quebra o contrato da API (commit com `!`). A API mantém `/v1` e cria `/v2` em paralelo |
| MINOR | Funcionalidade nova compatível (`feat`) |
| PATCH | Correção (`fix`) |

Cada deploy em produção ganha uma tag `vX.Y.Z` no commit que subiu, e as notas da versão saem das mensagens de commit. O app mobile segue a mesma versão nas lojas; correções só de texto e acessibilidade vão por EAS Update sem nova versão na loja (ADR-005).

## Hotfix

Mesmo fluxo, com prioridade: branch `fix/` a partir da `main`, PR com 2 aprovações, pipeline completo. Não existe atalho que pule testes ou segurança. Se a correção não puder esperar o pipeline, a saída é reverter o último deploy (reaplicar a task definition anterior), não subir código sem teste.
