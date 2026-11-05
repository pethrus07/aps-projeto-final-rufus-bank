# 9.6 Metodologia de desenvolvimento

**Decisão: Scrum com sprints de 2 semanas**, com um quadro Kanban dentro de cada sprint para acompanhar o fluxo das tarefas.

## Primeiro: o modelo de ciclo de vida

A Aula 03 lembra que o modelo de ciclo de vida é a **primeira escolha** do processo de software. Pela NBR ISO/IEC 12207, ciclo de vida é a estrutura de processos, atividades e tarefas do desenvolvimento, da operação e da manutenção, da definição dos requisitos até o fim do uso. O critério de escolha (Wazlawick) é o quanto os requisitos são conhecidos e estáveis, quando o cliente precisa ver a primeira versão e o tamanho e o risco do sistema.

**Decisão: modelo Incremental e iterativo, executado com Scrum, com duas práticas emprestadas de outros modelos:** a análise de risco a cada ciclo (do Espiral) e o teste planejado junto com cada requisito (do modelo V).

| Modelo | Serve quando | No Rufus | Escolha |
| --- | --- | --- | --- |
| Cascata | Requisitos bem conhecidos e congelados, sistema simples | A usabilidade só se confirma com usuário real (RNF08), e a 1ª versão só sairia no fim. O público nunca foi ouvido por um banco | Descartado |
| Modelo V | Mesmo caso do cascata, com foco em planejar testes | Qualquer mudança no meio obriga a refazer documentos de teste, análise e requisitos. Ficamos só com a ideia de planejar o teste junto do requisito (critérios Given/When/Then e DoR) | Descartado, com uma prática aproveitada |
| Incremental | Requisitos tratados em módulos, valor entregue cedo | Os 7 épicos (E1 a E7) viram incrementos. O beta com usuários reais chega no sprint 8, sem esperar o fim de tudo | **Escolhido** |
| Evolutivo | Requisitos pouco conhecidos, que surgem do uso | O núcleo é conhecido e regulado (Pix, LGPD, regras do Bloco 2). E o evolutivo dificulta limitar escopo e prazo, o que o parceiro BaaS e os investidores exigem | Descartado |
| Espiral (Boehm, 1988) | Sistema grande e de alto risco, guiado por análise de risco | O risco é alto (golpe, dinheiro, regulação), mas o espiral completo é caro e não tem número de voltas definido. Ficamos com a análise de risco a cada ciclo: a matriz do Bloco 7 é revista a cada 2 sprints | Descartado, com uma prática aproveitada |

As 3 etapas macro do ciclo de vida no projeto:

| Etapa | No Rufus |
| --- | --- |
| 1. Definição | Este trabalho: problema, requisitos, arquitetura, banco e plano (Blocos 1 a 9) |
| 2. Desenvolvimento | Sprints 0 a 8, de 16/11/2026 a 19/03/2027 (Bloco 7) |
| 3. Operação | Depois do lançamento: sustentação em Kanban, correções e novos requisitos. Pela referência da Aula 01, a manutenção custa de 15% a 20% do custo inicial por ano (Bloco 7, item 7.3) |

## Por que Scrum e não Kanban puro

| Critério | Scrum | Kanban puro | Por que pesa para o Rufus |
| --- | --- | --- | --- |
| Entrega com data | Sprint de duração fixa, meta por sprint | Fluxo contínuo, sem data por pacote | O parceiro BaaS, as lojas e os investidores precisam de datas (risco R04, R12). O cronograma do Bloco 7 é por sprint |
| Teste com usuários | A Review de cada sprint é o momento natural do teste com 5 pessoas do perfil | Precisaria de uma cadência criada à parte | O RNF08 exige teste de uso a cada ciclo, e a interface é o produto |
| Equipe nova | Cerimônias fixas ajudam um time que nunca trabalhou junto a criar ritmo | Exige um time já maduro para se auto-organizar só pelo quadro | Os 8 perfis do Bloco 7 começam juntos no sprint 0 |
| Medição de velocidade | Velocidade por sprint, usada para recalcular o plano depois do sprint 2 | Mede tempo de ciclo, bom para demanda contínua | O plano do Bloco 7 depende de velocidade em SP |
| Trabalho imprevisível | Mudança espera o próximo sprint | Absorve demanda que chega a qualquer hora | Pesa para Kanban **depois do lançamento**, quando aparecem incidentes e pedidos do SAC |

Kanban seria a melhor escolha para a fase de operação, com muitos pedidos pequenos e incidentes. Para construir o MVP com data e com teste de uso a cada ciclo, Scrum encaixa melhor. Depois do lançamento a equipe reavalia, e o mais provável é passar a Kanban para a sustentação.

## Papéis

| Papel do Scrum | Quem | Observação |
| --- | --- | --- |
| Product Owner | Product Owner (Bloco 7) | Dono do backlog e do aceite. Na equipe do trabalho de faculdade: Pedro Oliveira |
| Scrum Master | Tech Lead, acumulando | Equipe de 8 pessoas não justifica um Scrum Master dedicado. Se a velocidade cair dois sprints seguidos, a decisão é revista |
| Time de desenvolvimento | 2 back-end, 2 mobile, DevOps, QA, UX | QA e UX fazem parte do time e respondem pela DoD |

## Cerimônias

| Cerimônia | Quando | Duração | Resultado |
| --- | --- | --- | --- |
| Sprint Planning | Segunda de manhã, 1º dia do sprint | 2 horas | Meta do sprint e itens escolhidos dentro da capacidade |
| Daily | Todo dia às 9h30 | 15 minutos | Impedimentos visíveis |
| Refinamento | Quarta da 1ª semana | 1 hora | Itens do próximo sprint cumprindo a DoR |
| Teste com usuários | Quinta da 2ª semana | Meio dia | 5 sessões com pessoas do perfil das personas |
| Sprint Review | Sexta da 2ª semana, de manhã | 1 hora | Demonstração em homologação e aceite do PO |
| Retrospectiva | Sexta da 2ª semana, à tarde | 1 hora | Até 3 ações de melhoria. A cada 2 sprints também revisa a matriz de riscos |

## Artefatos

- **Product Backlog:** as 24 histórias do Bloco 2 e as 20 tarefas técnicas do Bloco 7, em ordem de prioridade.
- **Sprint Backlog:** os itens do sprint, num quadro com as colunas A fazer, Fazendo, Em revisão, Em homologação e Pronto. O limite é de 2 itens em "Em revisão" por pessoa, para a revisão não virar gargalo.
- **Incremento:** o que cumpre a DoD e está em homologação ao fim do sprint.
