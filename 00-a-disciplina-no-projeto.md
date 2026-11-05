# A disciplina no projeto

O Rufus Bank é a conclusão da disciplina: cada conceito das Aulas 01 a 05 e cada item do enunciado do Projeto Final aparece aplicado em algum bloco. Este mapa mostra onde.

## As etapas da engenharia de software (Aula 01) percorridas pelo projeto

| Etapa da Aula 01 | Onde está |
| --- | --- |
| Levantamento de necessidades | Bloco 1: problema com dados do Banco Central, Inaf e Febraban, personas |
| Definição de requisitos | Bloco 2: 32 RF, 14 RNF, 24 histórias, 16 regras de negócio |
| Análise de viabilidade | Bloco 1, item 4: as 4 perguntas, técnica, operacional e custo real |
| Documentação dos procedimentos | Blocos 3 a 6 e o AID inteiro |
| Definição da metodologia | Bloco 9, item 9.6: ciclo de vida Incremental com Scrum |
| Desenvolvimento | Bloco 7 (9 sprints) e Bloco 8 (o código que roda no localhost) |
| Teste | Bloco 9: estratégia de testes, cobertura, DoD. Bloco 5: o SQL testado num PostgreSQL real |
| Implantação | Bloco 6: pipeline com homologação, smoke test e aprovação |
| Manutenção | Bloco 7: custo de manutenção de 15% a 20% ao ano. Bloco 9: sustentação em Kanban |

## Conceito por aula

| Aula | Conceito | Como aparece no Rufus | Onde |
| --- | --- | --- | --- |
| 01 · Introdução | Engenharia de software é escala, equipe e durabilidade, não "programar bem" | Projeto para 10.000 usuários, equipe de 8 pessoas e operação com disponibilidade de 99,9% | Blocos 1, 2 e 7 |
| 01 · Introdução | Custos: 60% desenvolvimento e 40% teste, manutenção de 15% a 20% ao ano, faixas por tipo de sistema | Estimativa do Rufus conferida contra as faixas da aula | Bloco 7, item 7.3 |
| 01 · Introdução | Os 3 P: pessoas, papéis e processos | Trio com papéis definidos (PO, Arquiteto, DBA) e processo Scrum | README, Bloco 9 |
| 02 · Processos | BPM (gestão) e BPMN (notação), os 5 elementos mínimos | Processos de negócio do Pix e da conta de menor em BPMN 2.0, com pools e raias | Bloco 4 |
| 02 · Processos | Caso Ariane 5: redundância de hardware não protege contra defeito de software | As 2 zonas rodam a mesma imagem. A proteção contra defeito vem de testes, regras no banco, dinheiro em inteiro e deploy que se desfaz sozinho | Bloco 9, item 9.2 |
| 03 · Ciclos de vida | NBR ISO/IEC 12207, as 3 etapas e os 5 modelos (Cascata, V, Incremental, Evolutivo, Espiral) | Incremental escolhido e justificado contra os outros 4, com a análise de risco do Espiral e o teste planejado do V | Bloco 9, item 9.6 |
| 04 · Requisitos | Definição do IEEE, RF e RNF | RF com MoSCoW e RNF com métrica | Bloco 2 |
| 04 · Requisitos | Processo de engenharia de requisitos em 6 passos e técnicas de elicitação | Cada passo aplicado, separando o que foi feito do que fica planejado | Bloco 2, item 2.0 |
| 04 · Requisitos | Estudo de viabilidade com as 4 perguntas, inclusive "comprar ou fazer" | Comprar o core bancário (parceiro BaaS) e fazer a experiência | Bloco 1, item 4 |
| 04 · Requisitos | Classificação dos RNF (Sommerville) | Cada RNF classificado como de produto, organizacional ou externo | Bloco 2, item 2.2 |
| 04 · Requisitos | Regras de negócio (a dinâmica da aula pedia 3) | 16 regras, com origem e onde cada uma é garantida | Bloco 2, item 2.4 |
| 04 · Requisitos | Backlog: épico, história de usuário e tarefa | 7 épicos, 24 histórias e 20 tarefas técnicas | Blocos 2 e 7 |
| 04 · Requisitos | PO como ponto único de contato, requisito validado precisa estar escrito | Definition of Ready com aprovação do PO | Bloco 9 |
| 05 · Interface | Personas, conteúdo e funcionalidades como base do projeto de interface | As telas partem das 3 personas e das 16 funcionalidades | Bloco 2, item 2.5 |
| 05 · Interface | Taxonomia, wireframe, Material Design, protótipo conceito, baixa e alta fidelidade, TER | Árvore de navegação, telas nos três níveis de protótipo e plano de Teste de Resposta Emocional | Bloco 2, item 2.5 |
| 05 · Interface | Análise SWOT (FOFA) | Forças, fraquezas, oportunidades e ameaças do Rufus | Bloco 1, item 1 |

## O enunciado do Projeto Final, item por item

| Bloco do enunciado | Exigência | Onde está |
| --- | --- | --- |
| 1 · Concepção | Visão, personas (mín. 3), stakeholders, viabilidade com custo real, riscos (mín. 5) | Bloco 1: 3 personas, 10 stakeholders, custo da tabela oficial da AWS, 8 riscos |
| 2 · Requisitos | RF (mín. 20) com MoSCoW, RNF com métrica, histórias (mín. 15) com Given/When/Then e story points | Bloco 2: 32 RF, 14 RNF, 24 histórias |
| 3 · Arquitetura | ADR, C4 nos 4 níveis, stack com alternativa descartada, padrões | Bloco 3: 13 ADRs, C4 completo, 23 camadas na stack, 13 padrões |
| 4 · UML | Casos de uso, classes (mín. 10, tipadas), sequência x3, componentes, deployment, atividades x2 | Bloco 4: os 9 diagramas, mais 2 processos em BPMN |
| 5 · Banco | Decisão, conceitual, lógico, físico executável, dicionário, estratégia | Bloco 5: 27 tabelas, SQL testado em PostgreSQL 17 real, dicionário gerado do banco |
| 6 · Infra | Diagrama com custo, CI/CD, Docker, segurança OWASP, observabilidade | Bloco 6, e os arquivos reais em `codigo/` |
| 7 · Planejamento | WBS (3 níveis), estimativa, equipe com salário de mercado, riscos (mín. 8) | Bloco 7: WBS em 4 níveis, 221 SP em 9 sprints, 12 riscos |
| 8 · Dev | README, .env.example, OpenAPI 3.0, padrões, git workflow, Sprint 1 | Bloco 8: o README leva do clone ao localhost, testado |
| 9 · Qualidade | Glossário, testes, cobertura, DoR, DoD, metodologia | Bloco 9 |
| AID | PDF com sumário, os 9 blocos, diagramas com título, autores e data | Este documento, gerado pelo `ferramentas/aid/build.py` |
