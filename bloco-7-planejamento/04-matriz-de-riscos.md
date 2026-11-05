# 7.4 Matriz de riscos

12 riscos, de 5 categorias. Os 8 primeiros vêm do Bloco 1 (mesmo ID, mesma nota). Os 4 novos (R09 a R12) apareceram ao montar o cronograma e a equipe. Escala igual à do Bloco 1: probabilidade e impacto de 1 a 3, severidade = probabilidade x impacto.

## Riscos

| ID | Risco | Categoria | Prob. | Impacto | Sev. | Mitigação | Dono | Gatilho de ação |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | Fraudes e golpes contra usuários vulneráveis | Segurança | 3 | 3 | **9** | Confirmação falada do recebedor (US06), limite para destinatário novo e à noite (US11), bloquear tudo (US12), contato de confiança (US13), fila do antifraude (US16), aviso "o Rufus nunca liga" | PO e Tech Lead | Contestações de Pix acima de 0,5% dos envios no mês |
| R06 | Baixa adesão | Negócio | 3 | 3 | **9** | Conta sem tarifa, indicação pela família, parceria com associações e com quem paga diária. Beta com 50 pessoas no sprint 8 para medir antes de lançar | PO | Menos de 30 dos 50 do beta usando por 2 semanas seguidas |
| R02 | Vazamento de dados pessoais | Segurança | 2 | 3 | **6** | Cifra de CPF e data de nascimento, segredos no Secrets Manager, WAF, 2 fatores no painel, log sem dado pessoal, teste de invasão (T15) | Tech Lead e DevOps | Achado crítico ou alto no teste de invasão ou na varredura do pipeline |
| R03 | Usuários não conseguem usar o app | Negócio | 2 | 3 | **6** | Teste de uso com 5 pessoas do perfil a cada sprint (RNF08), áudio em toda tela, auditoria WCAG (T17) | UX | Menos de 4 de 5 pessoas pagando boleto sozinhas em até 3 minutos |
| R04 | Não conseguir parceria regulatória (BaaS) | Regulatório | 2 | 3 | **6** | Negociar com 2 parceiros. Porta e adaptador (ADR-002) com parceiro falso até o sprint 4, adaptador real no sprint 5 (T10) | PO | Nenhum contrato assinado até o fim do sprint 3 (08/01/2027) |
| R08 | Erro no tratamento de dados de menores e biometria | Regulatório | 2 | 3 | **6** | Consentimento do responsável com versão do termo, biometria só no celular, campos marcados no dicionário de dados | Tech Lead | Pedido de titular sem resposta em 15 dias (RNF07) |
| R09 | Sandbox do parceiro BaaS instável ou diferente da produção | Técnico | 2 | 3 | **6** | Testes de contrato contra o sandbox no pipeline, adaptador falso para os testes do dia a dia, conciliação (T18) desde o primeiro Pix real | Dev Back-End | Mais de 2 diferenças entre sandbox e documentação do parceiro no mesmo sprint |
| R10 | Saída de pessoa-chave (Tech Lead ou dev mobile) | Equipe | 2 | 3 | **6** | Revisão de código obrigatória (ninguém é o único que conhece um módulo), ADRs e README do Bloco 8, pareamento nas partes críticas (razão, identidade) | Tech Lead | Aviso de saída. Plano: redistribuir e usar a reserva do sprint 8 |
| R05 | Custo de infraestrutura maior que o esperado | Técnico | 2 | 2 | **4** | Alerta de orçamento em 80%, tag por ambiente, homologação desligada fora do horário, cache de áudio | DevOps | Gasto parcial acima de 80% do previsto antes do dia 20 do mês |
| R07 | Equipe sem experiência em acessibilidade e produto financeiro | Equipe | 2 | 2 | **4** | Guia de acessibilidade no padrão de código, revisão de acessibilidade na DoD, UX em tempo integral | UX | Tela reprovada no teste de uso por acessibilidade em 2 sprints seguidos |
| R11 | Mudança nas regras do Pix pelo Banco Central durante o projeto | Regulatório | 2 | 2 | **4** | Limites e regras de horário configuráveis, não fixos no código. Acompanhar as resoluções do BC na revisão quinzenal de riscos | PO | Publicação de resolução do BC que afete limites, horários ou devolução do Pix |
| R12 | Revisão da Apple ou do Google atrasar a publicação | Negócio | 2 | 2 | **4** | Primeira versão de teste enviada ao TestFlight e ao teste interno do Google Play no sprint 4 para conhecer a revisão cedo, publicação no sprint 7 com o sprint 8 de folga | Dev Mobile | App recusado na revisão |

## Matriz

| | Impacto 1 | Impacto 2 | Impacto 3 |
| --- | --- | --- | --- |
| **Probabilidade 3** | | | R01, R06 |
| **Probabilidade 2** | | R05, R07, R11, R12 | R02, R03, R04, R08, R09, R10 |
| **Probabilidade 1** | | | |

## Cobertura por categoria

| Categoria | Riscos |
| --- | --- |
| Técnico | R05, R09 |
| Negócio | R03, R06, R12 |
| Equipe | R07, R10 |
| Segurança | R01, R02 |
| Regulatório | R04, R08, R11 |

## Como a matriz é usada

A matriz é revisada a cada 2 sprints, na retrospectiva. Risco com severidade 6 ou mais tem dono e gatilho, e o gatilho disparado vira item no próximo sprint. A reserva do sprint 8 (34 SP) é o colchão para os riscos que se confirmarem.
