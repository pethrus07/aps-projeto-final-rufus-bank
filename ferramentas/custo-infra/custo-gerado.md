# 4.4 Custo de infraestrutura item a item

Anexo do Estudo de Viabilidade. Tabela gerada pelo script `ferramentas/custo-infra/custo_infra.py` a partir da tabela oficial de preços da AWS e das páginas de preço dos outros fornecedores; para mudar, altere as premissas no script e gere de novo.

- Região: AWS sa-east-1 (São Paulo), preço sob demanda, sem desconto de reserva.
- Tabelas de preço AWS publicadas entre 2026-09-11 e 2026-11-04.
- Câmbio: PTAX de venda de 2026-11-04, R$ 5,4778 por dólar (Banco Central).
- Gerado em 04/11/2026.

### Produção

| Item | Quantidade | Preço unitário (USD) | Total (USD) |
| --- | --- | --- | --- |
| API: 2 tarefas Fargate ARM (1 por zona), 0,5 vCPU cada | 730 vCPU-h | 0,0557 | 40,66 |
| API: memória das 2 tarefas, 1 GB cada | 1.460 GB-h | 0,00612 | 8,94 |
| Worker (filas e notificações): 1 tarefa, 0,25 vCPU | 182 vCPU-h | 0,0557 | 10,17 |
| Worker: memória, 0,5 GB | 365 GB-h | 0,00612 | 2,23 |
| PostgreSQL RDS db.t4g.medium Multi-AZ | 730 h | 0,275 | 200,75 |
| Disco do banco: 50 GB gp3 Multi-AZ | 50 GB-mês | 0,438 | 21,90 |
| Backup além da cota grátis (retenção de 35 dias) | 50 GB-mês | 0,095 | 4,75 |
| Snapshots mensais guardados 12 meses (12 x 50 GB, Bloco 5) | 600 GB-mês | 0,095 | 57,00 |
| Application Load Balancer | 730 h | 0,034 | 24,82 |
| ALB: capacidade media de 1 LCU | 730 LCU-h | 0,011 | 8,03 |
| NAT Gateway: 2, um por zona | 1.460 h | 0,093 | 135,78 |
| NAT: tráfego de saída para o parceiro BaaS | 20 GB | 0,093 | 1,86 |
| Saída para a internet (respostas da API) | 120 GB | 0,25 | 30,00 |
| IPv4 público: 2 do ALB e 2 dos NAT | 2.920 IP-h | 0,005 | 14,60 |
| WAF: 1 web ACL | 1 ACL | 5 | 5,00 |
| WAF: 5 regras | 5 regras | 1 | 5,00 |
| WAF: requisições inspecionadas | 6.000.000 req | 0,0000006 | 3,60 |
| Secrets Manager: 10 segredos | 10 segredos | 0,4 | 4,00 |
| CloudWatch Logs: ingestão | 20 GB | 0,9 | 18,00 |
| CloudWatch Logs: armazenamento (90 dias) | 60 GB-mês | 0,0408 | 2,45 |
| CloudWatch: 10 alarmes | 10 alarmes | 0,135 | 1,35 |
| CloudWatch: 20 métricas de negócio | 20 métricas | 0,3 | 6,00 |
| S3: comprovantes, documentos e cache de áudio | 50 GB-mês | 0,0405 | 2,02 |
| ECR: imagens dos containers | 5 GB-mês | 0,1 | 0,50 |
| Polly: leitura em voz alta (12 mi caracteres) | 12.000.000 caracteres | 0,000004 | 48,00 |
| Route 53: 1 zona de DNS (rufusbank.com.br) | 1 zona | 0,5 | 0,50 |
| Route 53: consultas de DNS | 5.000.000 consultas | 0,0000004 | 2,00 |
| SMS para o Brasil: convites e avisos a quem não tem o app | 1.000 SMS | 0,03 | 30,00 |
| **Total** | | | **689,91** |

Em reais: **R$ 3.779,18 por mês**.

### Homologação (staging)

| Item | Quantidade | Preço unitário (USD) | Total (USD) |
| --- | --- | --- | --- |
| API: 1 tarefa Fargate ARM, 0,5 vCPU | 365 vCPU-h | 0,0557 | 20,33 |
| API: memória, 1 GB | 730 GB-h | 0,00612 | 4,47 |
| Worker: 1 tarefa, 0,25 vCPU | 182 vCPU-h | 0,0557 | 10,17 |
| Worker: memória, 0,5 GB | 365 GB-h | 0,00612 | 2,23 |
| PostgreSQL RDS db.t4g.small Single-AZ | 730 h | 0,069 | 50,37 |
| Disco do banco: 20 GB gp3 | 20 GB-mês | 0,219 | 4,38 |
| Application Load Balancer | 730 h | 0,034 | 24,82 |
| ALB: capacidade mínima | 73 LCU-h | 0,011 | 0,80 |
| NAT Gateway: 1 | 730 h | 0,093 | 67,89 |
| NAT: tráfego | 2 GB | 0,093 | 0,19 |
| IPv4 público: 2 do ALB e 1 do NAT | 2.190 IP-h | 0,005 | 10,95 |
| Secrets Manager: 10 segredos | 10 segredos | 0,4 | 4,00 |
| CloudWatch Logs: ingestão | 3 GB | 0,9 | 2,70 |
| S3 | 5 GB-mês | 0,0405 | 0,20 |
| Polly: testes (1 mi caracteres) | 1.000.000 caracteres | 0,000004 | 4,00 |
| **Total** | | | **207,50** |

Em reais: **R$ 1.136,64 por mês**.

### Serviços fora da AWS

Preços transcritos da página oficial de cada fornecedor em 04/11/2026.

| Item | Valor | Periodicidade | Conta | Equivalente mensal (R$) | Fonte |
| --- | --- | --- | --- | --- | --- |
| Expo EAS, plano Starter (build do app e atualizações) | US$ 54,00 | mês | US$ 19 + 7.000 usuários acima dos 3.000 incluídos x US$ 0,005 | 295,80 | [Expo, página de preços](https://expo.dev/pricing) |
| Notificações push (Expo Push) | US$ 0,00 | mês | Sem custo por envio | 0,00 | [Expo, FAQ de push](https://docs.expo.dev/push-notifications/faq/) |
| GitHub Team (código, revisão e CI) | US$ 32,00 | mês | 8 pessoas x US$ 4; inclui 3.000 minutos de GitHub Actions | 175,29 | [GitHub, página de preços](https://github.com/pricing) |
| Domínio rufusbank.com.br | R$ 40,00 | ano | Anuidade do .com.br | 3,33 | [Registro.br](https://registro.br/) |
| Conta de desenvolvedor Apple | US$ 99,00 | ano | Anuidade | 45,19 | [Apple Developer Program](https://developer.apple.com/support/enrollment/) |
| Conta de desenvolvedor Google Play | US$ 25,00 | único | Taxa única de registro | custo único de 136,94 | [Google Play Console](https://support.google.com/googleplay/android-developer/answer/6112435) |
| Teste de invasão externo antes do lançamento | R$ 25.000,00 | único | Teto da faixa de mercado para aplicação + API + autenticação (R$ 10.000 a R$ 25.000). Referência, não cotação | custo único de 25.000,00 | [FreelaSemCrise, tabela de preços 2026](https://www.freelasemcrise.com.br/quanto-cobrar/pentest-teste-seguranca) |

Equivalente mensal dos serviços externos: **R$ 519,62**. Custos únicos: **R$ 25.136,94**.

Sem preço público, fora do total:

- Tarifa do parceiro BaaS (conta, Pix, boleto e validação de identidade): Os parceiros não publicam tabela de preço; depende de contrato e volume (risco R04).

### Resumo por ambiente

| Ambiente | USD por mês | R$ por mês |
| --- | --- | --- |
| Produção | 689,91 | 3.779,18 |
| Homologação | 207,50 | 1.136,64 |
| Serviços fora da AWS | 94,86 | 519,62 |
| Desenvolvimento | 0,00 | 0,00 (Docker Compose na máquina do dev) |
| **Total** | **992,27** | **5.435,43** |

Custos únicos (antes do lançamento): **R$ 25.136,94**.

### Fontes dos preços

Cada preço unitário da AWS foi lido destes arquivos oficiais (Price List API, pública, sem login), filtrando pelo código de uso (`usagetype`) indicado no script.

| Serviço | Tabela oficial | Publicada em |
| --- | --- | --- |
| AWSELB | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSELB/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSELB/current/sa-east-1/index.json) | 2026-11-02 |
| AWSSecretsManager | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSSecretsManager/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSSecretsManager/current/sa-east-1/index.json) | 2026-09-11 |
| AmazonCloudWatch | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/sa-east-1/index.json) | 2026-11-04 |
| AmazonEC2 | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/sa-east-1/index.json) | 2026-11-04 |
| AmazonECR | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECR/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECR/current/sa-east-1/index.json) | 2026-09-11 |
| AmazonECS | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECS/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECS/current/sa-east-1/index.json) | 2026-10-19 |
| AmazonPolly | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonPolly/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonPolly/current/sa-east-1/index.json) | 2026-10-22 |
| AmazonRDS | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/sa-east-1/index.json) | 2026-10-29 |
| AmazonRoute53 | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRoute53/current/index.json) | 2026-11-04 |
| AmazonS3 | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonS3/current/sa-east-1/index.json) | 2026-11-04 |
| AmazonVPC | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonVPC/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonVPC/current/sa-east-1/index.json) | 2026-11-03 |
| awswaf | [https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/awswaf/current/sa-east-1/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/awswaf/current/sa-east-1/index.json) | 2026-09-14 |
| SMS para o Brasil (End User Messaging) | [https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/business-applications/approved/documents/End-User-Messaging-SMS-Prices.ebc340b4d416d90832dd59629c4792b0deb6f8bc.csv](https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/business-applications/approved/documents/End-User-Messaging-SMS-Prices.ebc340b4d416d90832dd59629c4792b0deb6f8bc.csv) | consultado em 04/11/2026 |

Câmbio: API de cotações PTAX do Banco Central, [https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/](https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/), cotação de venda de 2026-11-04.

Conferência manual: os mesmos itens e quantidades podem ser lançados na calculadora oficial, [https://calculator.aws](https://calculator.aws), região South America (São Paulo).
