# 7.3 Composição da equipe e custo do projeto

> Arquivo gerado por `ferramentas/planejamento.py`. Não editar à mão.

A equipe tem **8 pessoas** e custa **R$ 132.664,11 por mês** com encargos. O projeto dura 4,05 meses (16/11/2026 a 19/03/2027) e custa **R$ 572.922,39** no total, somando equipe, infraestrutura do Bloco 1, serviços fora da AWS e custos únicos (conta do Google Play e teste de invasão).

## Pesquisa salarial: de onde vêm os números

- **Glassdoor (exigido no enunciado):** tentamos abrir as páginas de salário do glassdoor.com.br em 04/11/2026 e o site recusou o acesso automático (HTTP 403, exige login). Por isso nenhum valor desta tabela é do Glassdoor. A coluna de conferência abaixo fica para o grupo preencher abrindo o Glassdoor logado.
- **Robert Half, Guia Salarial 2027:** fonte principal. Usamos a **mediana (50º percentil) de Recife**, a cidade com página no guia mais próxima de João Pessoa, onde a equipe trabalha.
- **Designer UX/UI:** o guia da Robert Half não tem o cargo em Recife. Usamos a média do Novo CAGED para Designer de UX em Recife (Salário.com.br). É a média de todos os níveis com carteira assinada e provavelmente fica abaixo de um pleno: é o número mais fraco da tabela.

| Perfil | Salário mensal (R$) | Fonte | Glassdoor (conferência do grupo) |
| --- | --- | --- | --- |
| Product Owner | 8.750,00 | [Robert Half, Guia Salarial 2027, Product Owner - PO, Recife, 50º percentil](https://www.roberthalf.com/br/pt/vagas-detalhes/product-owner-po/recife) | a preencher |
| Tech Lead (Back-End Sênior) | 14.500,00 | [Robert Half, Guia Salarial 2027, Desenvolvedor(a) Back-End Sênior, Recife, 50º percentil](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-senior/recife) | a preencher |
| Desenvolvedor Back-End Pleno | 11.800,00 | [Robert Half, Guia Salarial 2027, Desenvolvedor(a) Back-End Pleno, Recife, 50º percentil](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-pleno/recife) | a preencher |
| Desenvolvedor Mobile Pleno (React Native) | 13.800,00 | [Robert Half, Guia Salarial 2027, Desenvolvedor(a) Mobile Pleno, Recife, 50º percentil](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-mobile-pleno/recife) | a preencher |
| Analista de DevOps | 14.600,00 | [Robert Half, Guia Salarial 2027, Analista de DevOps, Recife, 50º percentil](https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-devops/recife) | a preencher |
| Analista de Testes Pleno (QA) | 9.100,00 | [Robert Half, Guia Salarial 2027, Analista de Testes Pleno, Recife, 50º percentil](https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-testes-pleno/recife) | a preencher |
| Designer UX/UI | 3.344,38 | [Salário.com.br, Designer de UX (CBO 2624-10), Recife-PE, média com dados do Novo CAGED, atualizado em 08/10/2026](https://www.salario.com.br/profissao/designer-ux-cbo-262410/recife-pe/) | a preencher |

## Perfis, quantidade e por quê

| Perfil | Qtd. | Alocação | O que faz no projeto |
| --- | --- | --- | --- |
| Product Owner | 1 | 100% | Backlog, prioridade MoSCoW, aceite das histórias, contato com o parceiro BaaS |
| Tech Lead (Back-End Sênior) | 1 | 100% | Arquitetura, revisão de código, módulos de identidade, contas e pagamentos |
| Desenvolvedor Back-End Pleno | 1 | 100% | Módulos de família, antifraude, atendimento, notificação e integrações |
| Desenvolvedor Mobile Pleno (React Native) | 2 | 100% | App Android e iOS, acessibilidade, voz, câmera e biometria |
| Analista de DevOps | 1 | 50% | Terraform, pipeline, observabilidade, backup. Meio período: o trabalho pesado é no início e no lançamento |
| Analista de Testes Pleno (QA) | 1 | 100% | Testes automatizados de integração e E2E, teste de carga, testes com usuários junto com o UX |
| Designer UX/UI | 1 | 100% | Telas, linguagem simples, roteiro de áudio, teste de uso com pessoas do perfil a cada sprint |

Por que este tamanho: o ADR-001 (monolito modular) foi pensado para **2 devs de back-end**, e o app em React Native (ADR-005) para **2 devs mobile** cobrirem Android e iOS. Sem QA dedicado, os testes de integração e com usuários (RNF08) ficariam com os devs e a velocidade cairia. O UX é tempo integral porque a interface é o produto: cada tela passa por teste de uso com pessoas do perfil das personas.

## Encargos CLT: a conta

Empresa no Lucro Presumido ou Real, sem a desoneração da folha (CPRB). Encargos sobre o salário:

| Encargo | Alíquota | Base legal |
| --- | --- | --- |
| INSS patronal | 20,0% | Lei 8.212/1991, art. 22, I |
| RAT/SAT (risco leve, FAP 1,0) | 1,0% | Lei 8.212/1991, art. 22, II, a. Desenvolvimento de software é grau de risco leve |
| Terceiros (Sistema S, salário-educação, INCRA) | 5,8% | Contribuições de terceiros da guia do INSS |
| FGTS | 8,0% | Lei 8.036/1990, art. 15 |
| **Total de encargos** | **34,8%** | |

Provisões mensais:

| Provisão | % do salário por mês | Conta |
| --- | --- | --- |
| 13º salário | 8,33% | 1 salário por ano, dividido em 12 meses |
| Férias + 1/3 | 11,11% | 1 salário + 1/3 por ano, dividido em 12 meses |
| **Total de provisões** | **19,44%** | |

Os encargos também incidem sobre o 13º e as férias, então o fator é:

**custo mensal = salário x (1 + 0,1944) x (1 + 0,348) = salário x 1,6101**

## Custo mensal da equipe

| Perfil | Qtd. | Alocação | Salário (R$) | Custo mensal com encargos (R$) |
| --- | --- | --- | --- | --- |
| Product Owner | 1 | 100% | 8.750,00 | 14.088,47 |
| Tech Lead (Back-End Sênior) | 1 | 100% | 14.500,00 | 23.346,61 |
| Desenvolvedor Back-End Pleno | 1 | 100% | 11.800,00 | 18.999,31 |
| Desenvolvedor Mobile Pleno (React Native) | 2 | 100% | 13.800,00 | 44.439,07 |
| Analista de DevOps | 1 | 50% | 14.600,00 | 11.753,81 |
| Analista de Testes Pleno (QA) | 1 | 100% | 9.100,00 | 14.652,01 |
| Designer UX/UI | 1 | 100% | 3.344,38 | 5.384,82 |
| **Total** | **8** | | | **132.664,11** |

## Custo total do projeto

| Item | Conta | R$ |
| --- | --- | --- |
| Equipe | R$ 132.664,11 x 4,05 meses | 537.945,66 |
| Infra de homologação (Bloco 1) | R$ 1.136,64 x 4,05 meses | 4.609,01 |
| Infra de produção (Bloco 1), a partir do sprint 7 | R$ 3.790,14 x 0,82 meses | 3.123,74 |
| Serviços fora da AWS (Bloco 1, item 4.4: Expo, GitHub, domínio, conta Apple) | R$ 519,62 x 4,05 meses | 2.107,03 |
| Custos únicos (Bloco 1, item 4.4: conta do Google Play e teste de invasão) | valor único | 25.136,94 |
| **Total** | | **572.922,39** |

Meses = semanas do projeto x 12 / 52. Câmbio: a mesma PTAX do Bloco 1.

## Fora deste valor (precisa de cotação)

- Benefícios (vale-refeição, plano de saúde) e provisão de multa rescisória do FGTS.
- Cotação formal do teste de invasão (tarefa T15): o total usa o teto da faixa de mercado, R$ 25.000.
- Tarifa do parceiro BaaS por conta e por transação: depende de contrato (Bloco 1).
- Equipamentos, licenças de software e espaço de trabalho.

Depois do lançamento, a operação custa por mês a infraestrutura do Bloco 1 (R$ 5.446,39) mais a equipe que ficar para evoluir o produto.

## Conferência com a referência da disciplina (Aula 01)

A Aula 01 traz faixas de custo por tipo de software e três regras práticas. O Rufus conferido contra elas:

| Referência da Aula 01 | No Rufus |
| --- | --- |
| Sistema complexo (app mobile, alta segurança): R$ 150 mil a R$ 500 mil | R$ 572.922,39, um pouco acima do teto. Faz sentido: é app em Android e iOS (a aula diz que multiplataforma dobra ou triplica o esforço), tem painéis internos na web (SAC, antifraude e administração) e integração com parceiro BaaS (a aula diz que integrações de API somam de 20% a 30%) |
| Manutenção pós-lançamento: 15% a 20% do custo inicial por ano | De R$ 85.938,36 a R$ 114.584,48 por ano, além da infraestrutura mensal |
| Cerca de 60% do custo em desenvolvimento e 40% em teste | O teste não fica só com o QA: entra na Definition of Done de cada item (Bloco 9), com cobertura mínima no pipeline. A referência é o motivo de o QA ser dedicado desde o sprint 0, e não cortado para baratear |
| Corrigir depois de ir ao ar custa muito mais do que testar antes | Teste de uso a cada sprint (RNF08), teste de invasão antes do lançamento e o sprint 8 inteiro reservado para o beta |
