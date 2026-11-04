# Custo mensal de infraestrutura (gerado)

Arquivo gerado por `custo_infra.py`. Não editar à mão: mude as premissas no script e rode de novo.

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
| **Total** | | | **600,41** |

Em reais: **R$ 3.288,92 por mês**.

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

### Resumo por ambiente

| Ambiente | USD por mês | R$ por mês |
| --- | --- | --- |
| Produção | 600,41 | 3.288,92 |
| Homologação | 207,50 | 1.136,64 |
| Desenvolvimento | 0,00 | 0,00 (Docker Compose na máquina do dev) |
| **Total** | **807,91** | **4.425,55** |
