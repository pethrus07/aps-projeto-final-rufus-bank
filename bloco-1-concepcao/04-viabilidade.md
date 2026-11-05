# 4. Estudo de Viabilidade

**Veredito: o projeto é viável.** Tecnicamente, tudo que o Rufus precisa já existe em serviços maduros. Operacionalmente, a condição é ter um parceiro autorizado pelo Banco Central. A infraestrutura custa **R$ 5.435,43 por mês** (produção, homologação e serviços fora da AWS), mais **R$ 25.136,94 de custos únicos** antes do lançamento. Só a produção na AWS dá R$ 0,38 por usuário ativo.

## 4.1 Viabilidade técnica

Cada necessidade do produto foi comparada com uma tecnologia que já está no mercado. Nenhuma exige pesquisa ou invenção.

| Necessidade (do Documento de Visão) | Como se resolve | Maturidade |
| --- | --- | --- |
| Conta, saldo e Pix (F03, F04, F05) | API do parceiro BaaS. O Rufus não constrói core bancário nem se conecta direto ao Pix | Modelo comum no mercado brasileiro |
| Pagar boleto pela câmera (F06) | Leitura do código de barras no próprio celular e pagamento pela API do parceiro | Madura |
| Leitura em voz alta (princípio 1) | Serviço de texto para fala. A tabela de preços da AWS em São Paulo lista o Amazon Polly a US$ 4 por milhão de caracteres. Frases fixas são geradas uma vez e guardadas no S3 | Madura |
| Entrada por biometria (F02) | Biometria nativa do Android e do iOS. O dado biométrico fica no celular e não vai para o servidor | Madura |
| Abertura de conta com documento e selfie (F01) | Serviço de validação de identidade do parceiro ou de um fornecedor especializado | Madura |
| Saldo e movimentação sem erro | Banco relacional com transação ACID. PostgreSQL é a escolha preliminar. A decisão final, comparada com a alternativa, sai no ADR do Bloco 3 e no Bloco 5 | Madura |
| 99,9% de disponibilidade | Serviços gerenciados em 2 zonas de disponibilidade, banco Multi-AZ e balanceador de carga | Madura |
| Conta de menor e contato de confiança (F07, F08, F10) | Regra de negócio própria do Rufus: papéis e permissões sobre a mesma conta | Desenvolvimento próprio, sem risco técnico alto |

**Desenho preliminar de infraestrutura**, só para calcular o custo: app mobile, uma API e um worker em containers no AWS Fargate, PostgreSQL no Amazon RDS, Application Load Balancer com WAF, tudo na região sa-east-1 (São Paulo). A região foi escolhida pela latência para o usuário brasileiro e por manter os dados no país. O Bloco 3 confirma ou muda cada peça com ADR, e o custo é recalculado se mudar.

## 4.2 Viabilidade operacional

| Ponto | Como o Rufus opera |
| --- | --- |
| Modelo regulatório | O Rufus começa como empresa de tecnologia, sem autorização própria do Banco Central. A conta e o Pix ficam com um parceiro BaaS (Banking as a Service) que já é autorizado. O Rufus é a interface e a experiência |
| Regras que o produto precisa seguir | LGPD (Lei 13.709/2018), com cuidado especial com dados de adolescentes (art. 14) e dado biométrico, que é dado sensível. Regras do Pix e de segurança que o Banco Central impõe ao parceiro e que o parceiro repassa por contrato |
| Conta de menor | Adolescente de 16 e 17 anos abre conta assistido pelo responsável. O responsável aceita os termos e pode ver e limitar a movimentação |
| Atendimento | SAC humano por chat e telefone, sempre iniciado de dentro do app, depois que o cliente já entrou com biometria. Assim o cliente sabe que quem fala com ele é o Rufus de verdade |
| Prevenção a fraude | Regras automáticas no backend e analista antifraude para os casos suspeitos |
| Validação com usuário real | Teste de uso com pessoas do perfil das personas a cada sprint. A meta numérica entra como RNF no Bloco 2 |
| Equipe | O tamanho e o custo da equipe, com pesquisa salarial, ficam no Bloco 7 |

O ponto mais frágil da operação é a dependência do parceiro BaaS. Ele vira o risco R04 no item 5.

## 4.3 Custo de infraestrutura mensal

Preços da AWS tirados da tabela oficial (Price List API pública, a mesma base da calculadora em calculator.aws), região South America (São Paulo), preço sob demanda, consultados em 04/11/2026. Preço do SMS tirado do CSV oficial de preços por país da AWS. Serviços fora da AWS (Expo, GitHub, domínio, lojas, teste de invasão) transcritos das páginas de preço de cada fornecedor. Dólar pela PTAX de venda do Banco Central de 04/11/2026: **R$ 5,4778**. Cada fonte, com o link, está no item 4.4.

| Ambiente | Para que serve | USD por mês | R$ por mês |
| --- | --- | --- | --- |
| Produção (AWS) | Clientes reais, alta disponibilidade em 2 zonas | 689,91 | 3.779,18 |
| Homologação (AWS) | Testes antes de publicar, 1 zona, banco menor | 207,50 | 1.136,64 |
| Serviços fora da AWS | Build do app, push, GitHub, domínio e conta da Apple | 94,86 | 519,62 |
| Desenvolvimento | Cada dev roda tudo na própria máquina com Docker Compose | 0,00 | 0,00 |
| **Total mensal** | | **992,27** | **5.435,43** |

Custos únicos antes do lançamento: conta do Google Play (US$ 25) e teste de invasão externo (R$ 25.000, teto da faixa de mercado), total de **R$ 25.136,94**.

A tabela item a item (quantidade, preço unitário, total e fonte de cada serviço) está no item 4.4, em [ferramentas/custo-infra/custo-gerado.md](../ferramentas/custo-infra/custo-gerado.md). Ela é gerada pelo script [custo_infra.py](../ferramentas/custo-infra/custo_infra.py), que baixa os preços oficiais e para com erro se algum preço não for encontrado.

### Onde está o dinheiro em produção

| Serviço | USD por mês | Por que custa isso |
| --- | --- | --- |
| Banco PostgreSQL (RDS Multi-AZ, disco, backup e snapshots mensais) | 284,40 | Multi-AZ mantém uma cópia em outra zona e assume em caso de falha. É o que sustenta os 99,9%. Os snapshots mensais ficam 12 meses (Bloco 5) |
| NAT Gateway (2) | 137,64 | Um por zona, para a API falar com o parceiro BaaS mesmo se uma zona cair |
| Containers (Fargate) | 62,00 | 2 tarefas da API, uma em cada zona, e 1 worker |
| Leitura em voz alta (Polly) | 48,00 | Fala gerada na hora para saldo, valores e nomes |
| SMS para o Brasil | 30,00 | 1.000 SMS por mês a US$ 0,03, só para quem ainda não tem o app (convites e avisos) |
| Restante (balanceador, WAF, logs, saída de dados, IPs, DNS, segredos, S3, ECR) | 127,87 | Rede, segurança e observabilidade |

### Premissas de uso

| Premissa | Valor | De onde vem |
| --- | --- | --- |
| Usuários ativos por mês no 1º ano | 10.000 | Meta inicial. O Bloco 2 usa o mesmo número no RNF de escalabilidade |
| Requisições à API por mês | 6 milhões | 10.000 usuários x 20 acessos x 30 requisições |
| Dados enviados para a internet | 120 GB | 6 milhões de respostas de 20 KB |
| Caracteres falados por mês | 12 milhões | Metade dos usuários usa áudio: 5.000 x 30 falas x 80 caracteres |
| Logs | 20 GB por mês, guardados por 90 dias | Estimativa para API e worker com log estruturado |
| SMS | 1.000 por mês | Push é grátis; SMS só para convite do responsável e do contato de confiança e para aviso a quem não tem o app |
| Usuários que recebem atualização do app (Expo) | 10.000 | Todos os usuários ativos |
| Pessoas no GitHub | 8 | A equipe do Bloco 7 |
| Disponibilidade | 99,9% | Meta que obriga 2 zonas, banco Multi-AZ, 2 NAT e balanceador |

### O que este valor não inclui

- Tarifa do parceiro BaaS por conta, Pix, boleto e validação de identidade. Os parceiros não publicam tabela de preço: depende de contrato e de volume (risco R04).
- Salários da equipe (Bloco 7).
- Descontos de reserva (Savings Plans). Com uso estável depois do lançamento, o custo de containers e banco pode cair.
