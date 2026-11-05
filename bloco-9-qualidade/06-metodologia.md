# 9.6 Metodologia de desenvolvimento

**Decisão: Scrum com sprints de 2 semanas**, com um quadro Kanban dentro de cada sprint para acompanhar o fluxo das tarefas.

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
