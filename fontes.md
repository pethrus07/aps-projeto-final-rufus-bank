# Fontes e referências

Toda fonte usada no projeto, agrupada pelo que ela sustenta. As páginas foram abertas e os números e artigos conferidos nelas em 04/11/2026. O texto das leis foi conferido no site do Planalto e o da Resolução BCB 142 na API de normativos do Banco Central.

## Problema e público (Bloco 1)

| Dado usado | Fonte |
| --- | --- |
| 21,1 milhões de adultos sem usar produto financeiro em 2024; 53% de acerto em conhecimento financeiro; 87% erraram juros simples; letramento cai com a idade; 59% dos idosos usam internet | Banco Central do Brasil. *Relatório de Cidadania Financeira 2025*, seções 1.1 e 1.2. [https://www.bcb.gov.br/content/cidadaniafinanceira/documentos_cidadania/RIF/relatorio_de_cidadania_financeira_2025.pdf](https://www.bcb.gov.br/content/cidadaniafinanceira/documentos_cidadania/RIF/relatorio_de_cidadania_financeira_2025.pdf) |
| 29% de analfabetos funcionais (15 a 64 anos); 51% entre 50 e 64 anos; 73% dos analfabetos funcionais usam internet e 60% deles estão no nível mais baixo de habilidade digital | Inaf 2024 (Ação Educativa e Conhecimento Social), divulgado em 05/05/2025. Comunicado do UNICEF Brasil: [https://www.unicef.org/brazil/comunicados-de-imprensa/analfabetismo-funcional-nao-apresenta-melhora-e-alcanca-29-por-cento-dos-brasileiros-mesmo-patamar-de-2018-aponta-novo-levantamento-do-inaf](https://www.unicef.org/brazil/comunicados-de-imprensa/analfabetismo-funcional-nao-apresenta-melhora-e-alcanca-29-por-cento-dos-brasileiros-mesmo-patamar-de-2018-aponta-novo-levantamento-do-inaf) |
| 139 mil relatos do golpe da falsa central ou falso funcionário no 1º semestre de 2025, alta de 195,7% | Dados da Febraban divulgados em 11/11/2025: [https://conexaoto.com.br/2025/11/11/golpe-da-falsa-venda-e-o-mais-aplicado-contra-clientes-bancarios-no-1o-semestre-do-ano](https://conexaoto.com.br/2025/11/11/golpe-da-falsa-venda-e-o-mais-aplicado-contra-clientes-bancarios-no-1o-semestre-do-ano) |

## Custos de infraestrutura (Blocos 1, 3 e 6)

| Dado usado | Fonte |
| --- | --- |
| Preço de cada serviço da AWS em São Paulo (Fargate, RDS, ALB, NAT, IPv4, WAF, Secrets Manager, CloudWatch, S3, ECR, Polly, saída de dados) | AWS Price List API, um arquivo oficial por serviço, região sa-east-1. Lista completa com a data de publicação de cada arquivo no item 4.4 (custo item a item). Endereço base: [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json) |
| EKS: US$ 0,10 por hora por cluster em São Paulo (ADR-009) | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEKS/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEKS/current/sa-east-1/index.json) |
| Lambda: US$ 0,0000166667 por GB-segundo e US$ 0,20 por milhão de requisições em São Paulo (ADR-009) | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSLambda/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSLambda/current/sa-east-1/index.json) |
| RDS db.m7g.large Multi-AZ a US$ 0,442 por hora (crescimento, arguição) | Mesma tabela do RDS listada no item 4.4 |
| Dólar a R$ 5,4778 (PTAX de venda de 04/11/2026) | Banco Central, API PTAX: [https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/) |
| Conferência manual dos custos | Calculadora oficial da AWS: [https://calculator.aws](https://calculator.aws) |
| SMS para o Brasil: US$ 0,03 por mensagem | CSV oficial de preços de SMS por país da AWS End User Messaging: [https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/business-applications/approved/documents/End-User-Messaging-SMS-Prices.ebc340b4d416d90832dd59629c4792b0deb6f8bc.csv](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/business-applications/approved/documents/End-User-Messaging-SMS-Prices.ebc340b4d416d90832dd59629c4792b0deb6f8bc.csv) |
| Route 53: US$ 0,50 por zona e US$ 0,40 por milhão de consultas | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json) |
| Expo EAS Starter: US$ 19 por mês, 3.000 usuários incluídos e US$ 0,005 por usuário a mais | [https://expo.dev/pricing](https://expo.dev/pricing) |
| Expo Push sem custo por envio | [https://docs.expo.dev/push-notifications/faq/](https://docs.expo.dev/push-notifications/faq/) |
| GitHub Team: US$ 4 por usuário por mês, 3.000 minutos de Actions | [https://github.com/pricing](https://github.com/pricing) |
| Domínio .com.br: R$ 40,00 por ano | [https://registro.br/](https://registro.br/) |
| Teste de invasão: R$ 10.000 a R$ 25.000 para aplicação, API e autenticação (referência de mercado 2026, não cotação) | [https://www.freelasemcrise.com.br/quanto-cobrar/pentest-teste-seguranca](https://www.freelasemcrise.com.br/quanto-cobrar/pentest-teste-seguranca) |

## Leis e normas

| Norma | Onde usamos | Fonte |
| --- | --- | --- |
| Lei 13.709/2018 (LGPD): art. 5º, II (biometria é dado pessoal sensível), art. 14 (dados de crianças e adolescentes no seu melhor interesse), art. 18 (direitos do titular), art. 19, II (resposta completa em até 15 dias), art. 33 (transferência internacional) | RNF07, RF029, ADR-013, Bloco 5 | [https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm) |
| Lei 9.613/1998, art. 10, §2º: cadastros e registros guardados por no mínimo 5 anos a partir do encerramento da conta ou da conclusão da transação | RNF14, Bloco 5 | [https://www.planalto.gov.br/ccivil_03/leis/l9613.htm](https://www.planalto.gov.br/ccivil_03/leis/l9613.htm) |
| Lei 10.097/2000 (aprendizagem) | Persona Camila | [https://www.planalto.gov.br/ccivil_03/leis/l10097.htm](https://www.planalto.gov.br/ccivil_03/leis/l10097.htm) |
| Código Civil, art. 4º (maiores de 16 e menores de 18 anos assistidos pelos pais) | RF014 | [https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm](https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm) |
| Resolução BCB nº 142/2021, art. 2º, I: limite de R$ 1.000 entre 20h e 6h por conta, entre pessoas físicas | RF019, US11 | [https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=142](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=142) |

## Padrões técnicos

| Padrão | Onde usamos | Fonte |
| --- | --- | --- |
| WCAG 2.2 (contraste mínimo de 4,5:1, nível AA) | RNF09 | [https://www.w3.org/TR/WCAG22/](https://www.w3.org/TR/WCAG22/) |
| Área de toque de 48 dp no Android | RNF09 | [https://developer.android.com/guide/topics/ui/accessibility/apps](https://developer.android.com/guide/topics/ui/accessibility/apps) |
| OWASP Password Storage Cheat Sheet (Argon2id) | RNF05, ADR-010 | [https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) |
| OWASP Top 10 (2021) | Bloco 6 | [https://owasp.org/Top10/](https://owasp.org/Top10/) |
| Teste de usabilidade com 5 usuários (Nielsen) | RNF08 | [https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/) |
| Restauração a ponto no tempo do RDS | RNF12, Bloco 5 | [https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html) |
| Modelo C4 | Bloco 3 | [https://c4model.com/](https://c4model.com/) |
| Architecture Decision Records | Bloco 3 | [https://adr.github.io/](https://adr.github.io/) |
| OpenAPI 3.0 | Bloco 8 | [https://spec.openapis.org/oas/v3.0.3](https://spec.openapis.org/oas/v3.0.3) |
| Conventional Commits | Bloco 8 | [https://www.conventionalcommits.org/pt-br/v1.0.0/](https://www.conventionalcommits.org/pt-br/v1.0.0/) |

## Salários e custo da equipe (Bloco 7)

Consultadas em 04/11/2026. O Glassdoor (glassdoor.com.br), indicado no enunciado, recusou o acesso automático (HTTP 403, exige login); a conferência no Glassdoor está na tabela do item 7.3, em coluna própria.

| Perfil | Valor usado | Fonte |
| --- | --- | --- |
| Product Owner | R$ 8.750,00 | Robert Half, Guia Salarial 2027, Recife, mediana: [https://www.roberthalf.com/br/pt/vagas-detalhes/product-owner-po/recife](https://www.roberthalf.com/br/pt/vagas-detalhes/product-owner-po/recife) |
| Tech Lead (Back-End Sênior) | R$ 14.500,00 | [https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-senior/recife](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-senior/recife) |
| Desenvolvedor Back-End Pleno | R$ 11.800,00 | [https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-pleno/recife](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-pleno/recife) |
| Desenvolvedor Mobile Pleno | R$ 13.800,00 | [https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-mobile-pleno/recife](https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-mobile-pleno/recife) |
| Analista de DevOps | R$ 14.600,00 | [https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-devops/recife](https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-devops/recife) |
| Analista de Testes Pleno | R$ 9.100,00 | [https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-testes-pleno/recife](https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-testes-pleno/recife) |
| Designer UX/UI | R$ 3.344,38 | Salário.com.br, média do Novo CAGED em Recife: [https://www.salario.com.br/profissao/designer-ux-cbo-262410/recife-pe/](https://www.salario.com.br/profissao/designer-ux-cbo-262410/recife-pe/) |
| Conta de desenvolvedor Apple | US$ 99 por ano | [https://developer.apple.com/support/enrollment/](https://developer.apple.com/support/enrollment/) |
| Conta de desenvolvedor Google Play | US$ 25, uma vez | [https://support.google.com/googleplay/android-developer/answer/6112435](https://support.google.com/googleplay/android-developer/answer/6112435) |

Encargos trabalhistas (INSS patronal, RAT, terceiros, FGTS, 13º, férias e um terço) calculados item a item no item 7.3, a partir das alíquotas legais.
