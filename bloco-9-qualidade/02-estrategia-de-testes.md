# 9.2 Estratégia de testes

O Rufus mexe com dinheiro de quem tem medo de errar, então a estratégia testa mais onde o erro custa mais: razão contábil, Pix, identidade e acessibilidade. Cada tipo de teste diz o que cobre, a ferramenta, quando roda e qual requisito protege.

## Pirâmide

| Nível | Quantidade relativa | Tempo no pipeline | Ferramenta |
| --- | --- | --- | --- |
| Unidade | Muitos | Menos de 2 minutos | Jest |
| Integração com banco real | Médio | Menos de 6 minutos | Jest com Testcontainers (PostgreSQL 17) |
| Contrato da API | Médio | Menos de 2 minutos | Validação das respostas contra o `openapi.yaml` |
| E2E mobile | Poucos, só os fluxos principais | Menos de 15 minutos, em homologação | Maestro |
| Carga | 1 cenário por versão grande | 20 minutos, em homologação | k6 |
| Acessibilidade | Em toda tela | Automático no PR e manual por sprint | Lint de acessibilidade do React Native, TalkBack e VoiceOver |
| Teste com usuários | 5 pessoas por sprint | Fora do pipeline | Roteiro do UX com cronômetro |

## Tipos de teste

| Tipo | O que cobre | Exemplo no Rufus | Requisito protegido |
| --- | --- | --- | --- |
| Unidade | Regras de domínio sem banco nem rede: estados da transação, regras do antifraude, limites | `RegraDestinatarioNovo` devolve a nota certa. Transação CONCLUIDA não pode virar ESTORNADA | RF019, RF026 |
| Integração | Repositórios, SQL, gatilho do razão, outbox, chave de idempotência, contra um PostgreSQL de verdade em container | Transação com lançamentos que não somam zero é recusada pelo banco. Dois `POST /pix/envios` com a mesma chave criam uma transação só | RNF11, ADR-007, ADR-008 |
| Contrato | Toda resposta da API confere com o `openapi.yaml`. O cliente do app é gerado do mesmo arquivo | Campo novo sem estar no contrato quebra o teste | ADR-003 |
| Contrato com o parceiro | Adaptador real contra o sandbox do parceiro BaaS, toda noite | Mudança de formato no sandbox é detectada antes de chegar à produção | R09 |
| E2E | Fluxos do cliente no app, em homologação, com o adaptador falso | Abrir conta, entrar com senha, enviar Pix, pagar boleto, bloquear tudo | US01, US02, US06, US08, US12 |
| Carga | 100 requisições por segundo por 10 minutos nas rotas de leitura e de Pix | p95 das leituras abaixo de 300 ms e taxa de erro abaixo de 1% | RNF01, RNF04 |
| Segurança | Varredura de dependências e da imagem (npm audit, Trivy), busca de segredos no código (gitleaks) e teste de invasão antes do lançamento | Nenhuma vulnerabilidade crítica ou alta | RNF05, RNF06 |
| Acessibilidade | Rótulo de acessibilidade em todo elemento tocável, contraste, área de toque, botão "Ouvir" | Botão sem rótulo reprova o PR | RNF09 |
| Usabilidade com usuários | 5 pessoas do perfil das personas por sprint, com tarefas cronometradas | Pagar um boleto sem ajuda em até 3 minutos | RNF08 |
| Restauração | Restaurar o backup do RDS num banco novo e conferir os saldos | A cada 3 meses e antes do lançamento (T20) | RNF12 |

## Ambientes de teste

| Onde | O que roda | Parceiro BaaS |
| --- | --- | --- |
| Máquina do dev | Unidade, integração (Testcontainers) | Adaptador falso |
| Pipeline (GitHub Actions) | Unidade, integração, contrato, lint, varredura de segurança | Adaptador falso |
| Homologação | E2E, carga, contrato com o parceiro | Sandbox do parceiro (a partir do sprint 5) |
| Produção | Smoke test depois de cada deploy (`/health` e login de uma conta de teste) | Parceiro real |

## Dados de teste

- Nunca usar dado real de cliente fora da produção.
- Dados de teste gerados por script com CPFs válidos de teste, recriados a cada execução.
- Contas de teste em produção marcadas e excluídas da conciliação e das métricas de negócio.
