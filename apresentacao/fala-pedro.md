# Rufus Bank · fala do Pedro (Analista / PO)

Slides 1 a 7, cerca de 4 min 30 s, e o fechamento nos slides 23 e 24. Fale olhando para a turma: o número está no slide, a sua frase explica o número.

## Slide 1 · Abertura (20 s)

"Boa noite. Somos o Rufus Bank: Pedro, Izaias e Carlos. Rufus vem do latim e quer dizer vermelho, por isso a nossa cor. É um banco digital para quem os bancos de hoje atendem mal: quem lê com dificuldade, os idosos e os adolescentes. Vamos mostrar o projeto inteiro, da concepção até o ponto em que um desenvolvedor consegue começar amanhã."

## Slide 2 · O problema (40 s)

"O problema não é ter conta. Quase todo mundo já tem acesso. O problema é conseguir usar a conta sozinho e com segurança.

São 21,1 milhões de adultos que não usaram nenhum produto financeiro em 2024, segundo o Banco Central. 29% da população de 15 a 64 anos é analfabeta funcional, e entre 50 e 64 anos são 51%, pelo Inaf. 87% erraram uma conta simples de juros. E o golpe da falsa central subiu 195,7% no primeiro semestre de 2025, segundo a Febraban.

Ou seja: quem mais precisa de ajuda é justamente quem mais sofre golpe. Todas as fontes estão com link no documento."

## Slide 3 · Personas (40 s)

"Esses números viraram três pessoas.

O Antônio, 47 anos, ajudante de pedreiro, estudou até o quinto ano e já caiu no golpe do falso atendente. Ele quer usar a conta por ícone e áudio, sem depender de ninguém.

A Camila, 17 anos, jovem aprendiz. Quer juntar dinheiro para um notebook, mas os bancos ou bloqueiam a conta dela ou tratam como adulta.

A Dona Marlene, 68 anos, aposentada, só usa WhatsApp e depende do neto para mexer no banco.

Cada dor delas virou requisito: o Antônio é o áudio, a Camila é a conta com responsável, a Dona Marlene é pagar conta sem pedir ajuda."

## Slide 4 · Proposta de valor e escopo (40 s)

"A proposta é: simples por padrão e protegido por padrão. São cinco princípios que valem para todas as telas:

1. ícone e áudio em toda tela;
2. no máximo 3 toques nas ações principais;
3. linguagem do dia a dia, 'dinheiro que você tem' e não 'saldo disponível';
4. proteção contra golpe: o Rufus nunca liga e o app fala para quem vai o Pix;
5. autonomia com rede de apoio.

À direita está o que ficou fora de propósito. Crédito, por exemplo: endividamento é um risco alto para esse público, então não entra no MVP. Fora do escopo é tão importante quanto o escopo."

## Slide 5 · Requisitos (45 s)

"São 32 requisitos funcionais priorizados por MoSCoW: 22 Must, 6 Should, 2 Could e 2 Won't, cada um com justificativa.

São 14 não funcionais, e todos têm número e forma de medir. 300 milissegundos no p95, 99,9% de disponibilidade, 10 mil usuários com picos de 100 requisições por segundo, 3 toques, contraste 4,5 para 1 da WCAG e perda máxima de 5 minutos de dados. Cada um está classificado como de produto, organizacional ou externo, a classificação de Sommerville da Aula 04.

Também temos 16 regras de negócio, e a gente seguiu o processo de engenharia de requisitos em 6 passos, da elicitação à gerência."

## Slide 6 · Histórias (40 s)

"O backlog segue a hierarquia da Aula 04: épico, história e tarefa. São 7 épicos, 24 histórias e 114 pontos, em Fibonacci, com a US13 de 3 pontos como referência de tamanho.

O exemplo é a US06: 'Como Dona Marlene, quero ouvir o nome de quem vai receber e o valor antes de confirmar, para ter certeza de que não estou errando.' Dado que informei a chave e o valor, quando chego na confirmação, então o app mostra e fala o nome, o banco e o valor. Todo critério é testável."

## Slide 7 · Interface (40 s)

"No Rufus a interface é o produto, então aplicamos a Aula 05. A taxonomia organiza o app em seções, telas e passos. As telas foram feitas nos três níveis de protótipo: conceito, baixa fidelidade e alta fidelidade.

Repare que o vermelho é a marca, mas os valores em dinheiro ficam em grafite, porque número vermelho em banco se lê como dinheiro saindo. E o 'bloquear tudo' usa um vermelho mais escuro, com cadeado, para não se confundir com o botão principal.

O contraste foi medido pela fórmula da WCAG e as áreas de toque têm 48 dp. Agora o Izaias mostra como isso vira arquitetura."

## Slides 23 e 24 · Fechamento (30 s)

"Para fechar: este projeto é a conclusão da matéria. A Aula 01 está nos custos de referência, a Aula 02 no BPMN e na lição do Ariane 5, a Aula 03 no ciclo de vida incremental, escolhido contra os outros quatro modelos, a Aula 04 nos requisitos e a Aula 05 na interface. O documento de apoio abre com esse mapa completo.

Obrigado. Estamos prontos para as perguntas."

## Se perguntarem para você

| Pergunta | Resposta curta |
| --- | --- |
| Por que esse RNF é Must? | Porque protege o dinheiro do cliente, a promessa do produto, a lei ou a meta de operação. Só a observabilidade completa é Should |
| Por que 3 toques e não 5? | É a promessa para quem lê pouco. A confirmação com a digital não conta: é a barreira contra golpe e não foi cortada para bater a meta |
| Por que 300 ms? | Acima de 1 segundo o usuário perde a sensação de resposta imediata; 300 ms deixa folga para a rede do celular |
| Como validariam com usuário? | Teste de uso com 5 pessoas do perfil a cada sprint (Nielsen): pelo menos 4 pagam um boleto sozinhas em até 3 minutos |
| Por que jovem aprendiz e não estágio? | São contratos diferentes por lei. O aprendiz tem renda mensal com carteira (Lei 10.097/2000) |
| Comprar ou fazer? | Compramos o core bancário de um parceiro BaaS autorizado pelo Banco Central e fazemos o que é diferencial: áudio, proteção contra golpe e conta de menor |
| Qual o ciclo de vida? | Incremental com Scrum. Pegamos a análise de risco a cada ciclo do Espiral e o teste planejado junto do requisito do modelo V |

---

# Resumo do projeto inteiro

**Rufus Bank:** banco digital com áudio, ícones e linguagem simples para quem lê com dificuldade, idosos e adolescentes. O projeto vai da concepção ao dia 1 do desenvolvedor, sem implementar, com toda decisão justificada contra a alternativa descartada.

| Bloco | O que tem |
| --- | --- |
| 1 · Concepção | Problema com dados do Banco Central, Inaf e Febraban. SWOT, 3 personas, 10 stakeholders, viabilidade com as 4 perguntas e custo real, 8 riscos |
| 2 · Requisitos | Processo de ER em 6 passos, 32 RF com MoSCoW, 14 RNF com métrica, 24 histórias em 7 épicos (114 SP), 16 regras de negócio, protótipos em 3 níveis |
| 3 · Arquitetura | 13 ADRs, C4 nos 4 níveis, stack de 23 camadas, 13 padrões. Monolito modular, REST com OpenAPI, React Native, NestJS, PostgreSQL, ECS Fargate na AWS de São Paulo |
| 4 · UML | Casos de uso, classes tipadas, 3 sequências (login, Pix e erro crítico com estorno), componentes, implantação e 2 atividades. Mais 2 processos em BPMN 2.0 |
| 5 · Banco | PostgreSQL contra MongoDB, conceitual, lógico, 27 tabelas no DDL testado num PostgreSQL 17 real (21 de 21 testes), dicionário gerado do banco com 26 campos LGPD |
| 6 · Infra | 2 zonas, banco Multi-AZ, 2 NAT. Custo mensal de R$ 5.446,39 (produção na AWS R$ 3.790,14) e R$ 25.136,94 únicos, todos com fonte. CI/CD em 8 etapas, OWASP Top 10 |
| 7 · Planejamento | WBS em 4 níveis, 221 SP em 9 sprints (16/11/2026 a 19/03/2027), 8 pessoas a R$ 132.664,11 por mês, projeto total de R$ 572.922,39, 12 riscos |
| 8 · Dev | README do clone ao localhost testado, .env.example, OpenAPI com 50 rotas validado, padrões de código, git workflow, Sprint 1 detalhado |
| 9 · Qualidade | Glossário, pirâmide de testes, metas de cobertura, DoR, DoD, ciclo de vida Incremental com Scrum |

**Quem apresenta:** Pedro, slides 1 a 7 e o fechamento. Izaias, slides 8 a 14 (ADR, C4, UML e BPMN). Carlos, slides 15 a 19 (banco, infra, CI/CD e segurança). Slides 20 a 22 (planejamento, riscos e o dev pronto), quem o grupo combinar.

**Regra da arguição:** qualquer um responde qualquer parte. As respostas das 7 perguntas do professor estão em `apresentacao/arguicao.md`.
