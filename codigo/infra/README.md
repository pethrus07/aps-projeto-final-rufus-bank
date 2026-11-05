# Infraestrutura

`ecs/` tem as definições de tarefa do ECS Fargate usadas pelo `cd.yml`, uma por serviço e ambiente. O tamanho de cada tarefa é o mesmo do custo do Bloco 1: API com 0,5 vCPU e 1 GB, worker com 0,25 vCPU e 0,5 GB, processador ARM64.

`${CONTA}` é o número da conta AWS e `{{TAG}}` é trocado pelo hash do commit no deploy. Os segredos vêm do Secrets Manager, nunca de variável escrita aqui.

O restante da infraestrutura (VPC, subnets, ALB, WAF, RDS, NAT, S3, roles) é criado com Terraform no Sprint 1, a partir do desenho de `bloco-6-infra/01-diagrama-de-infra.md`.
