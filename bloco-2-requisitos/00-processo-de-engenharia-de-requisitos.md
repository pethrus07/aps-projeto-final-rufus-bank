# 2.0 Processo de Engenharia de Requisitos

Os requisitos deste bloco saíram do processo de Engenharia de Requisitos em 6 passos visto na Aula 04: elicitação, estudo de viabilidade, análise e negociação, especificação, validação e gerência. A tabela diz o que foi feito em cada passo e o que fica planejado para quando houver equipe e usuários reais, sem misturar os dois.

> Requisito, pela definição do IEEE (2008): uma capacidade que um usuário precisa para resolver um problema ou atingir um objetivo, ou que o sistema precisa ter para cumprir um contrato, padrão ou norma.

## Os 6 passos no Rufus

| Passo | O que é | O que fizemos | O que fica planejado |
| --- | --- | --- | --- |
| 1. Elicitação | Investigar, descobrir e extrair as necessidades reais, os problemas ocultos e as restrições. Não é só anotar pedidos | **Brainstorming** do grupo para o problema e as personas. **Pesquisa documental** em fontes oficiais: Banco Central, Inaf, Febraban (Bloco 1). **Análise das regras** que restringem o produto: LGPD, Lei 9.613, Resolução BCB 142, Código Civil | **Entrevistas** com 5 pessoas de cada perfil de persona. **Observação** (etnografia): acompanhar uma pessoa idosa pagando uma conta no app do banco atual, para ver onde ela trava. **Prototipação** com os protótipos do item 2.5 |
| 2. Estudo de viabilidade | Responder se vale a pena e se dá para fazer | As 4 perguntas da disciplina respondidas no Bloco 1, item 4, com custo real e a decisão de comprar (parceiro BaaS) em vez de fazer o core bancário | Revisar a viabilidade quando o parceiro BaaS mandar a tabela de tarifas |
| 3. Análise e negociação | Achar conflitos entre requisitos e chegar a um acordo | Os 6 conflitos da tabela abaixo, cada um com a decisão | Rodada de negociação com sócios e parceiro BaaS antes do sprint 0 |
| 4. Especificação | Registrar e oficializar os requisitos | RF com MoSCoW (2.1), RNF com métrica e classificação (2.2), histórias com Given/When/Then (2.3), regras de negócio (2.4) e matriz de rastreabilidade | Manter no repositório, versionado no git |
| 5. Validação | Mostrar, com o cliente e o usuário, que os requisitos descrevem o sistema certo | Revisão cruzada no trio: cada requisito conferido contra as personas e as fontes. Checklist: completo, sem ambiguidade, mensurável, rastreável | O PO valida e aprova cada história antes do sprint (Definition of Ready, Bloco 9). Teste de uso com 5 pessoas do perfil a cada sprint (RNF08) e TER dos protótipos (item 2.5) |
| 6. Gerência de requisitos | Controlar mudanças, que são regra e não exceção | Rastreabilidade de ponta a ponta: funcionalidade (F) → RF → história (US) → teste. Histórico de mudanças no git | Toda mudança entra como item do backlog. O PO avalia o impacto pela rastreabilidade e reprioriza. Nada muda sem passar pelo PO |

## Conflitos encontrados e como foram resolvidos

| Conflito | Lados | Decisão | Onde ficou |
| --- | --- | --- | --- |
| Facilidade de uso x segurança | "Poucos passos" (Antônio) x proteção contra golpe | A segurança entra sem passo extra: biometria no lugar de senha, confirmação falada na mesma tela do Pix, limite só para destinatário novo e à noite | RF003, RF009, RF019 |
| Autonomia do menor x controle dos pais | Camila quer decidir; os pais respondem por ela | Limite diário e mensal definido pelo responsável, e pedido de aprovação só acima do limite | RF015, RF016 |
| Autonomia do idoso x rede de apoio | Dona Marlene não quer depender do neto; a família quer protegê-la | O contato de confiança é só avisado, sem ver saldo nem movimentar | RF018 |
| Voz de qualidade x custo | Áudio em toda tela x orçamento de infraestrutura | Voz gerada no servidor com cache das frases fixas; a voz do celular fica como reserva | ADR-011 |
| Escopo amplo x prazo | Crédito e investimento atrairiam clientes x risco ao público e outra regulação | Fora do escopo do MVP | Bloco 1, fora do escopo |
| Estágio x jovem aprendiz | O texto inicial da persona Camila citava os dois contratos | Jovem aprendiz (Lei 10.097/2000), que é o caso de renda mensal com carteira | Persona Camila |

## O que aprendemos com as "situações da vida real" da Aula 04

- **Um ponto único de contato.** O Product Owner é quem mantém o backlog valorado e priorizado. Pedido que chega por outro caminho vai para ele.
- **Requisito validado precisa estar escrito.** O que não está no repositório não existe. Por isso a Definition of Ready exige a história escrita, com critérios de aceite e aprovada pelo PO.
- **Nada é óbvio.** "É só um login" virou 3 requisitos (RF003 a RF005), um ADR (ADR-010) e um diagrama de sequência.
