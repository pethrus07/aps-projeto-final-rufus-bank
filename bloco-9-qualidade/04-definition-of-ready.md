# 9.4 Definition of Ready (DoR)

Uma história ou tarefa só entra no Sprint Planning se cumprir **todos** os itens abaixo. Quem confere é o PO, no refinamento da semana anterior.

## Para histórias de usuário

- [ ] Está no formato "Como [persona], quero [ação], para [objetivo]" e a persona é uma das do Bloco 1 ou um papel do modelo de domínio.
- [ ] Tem pelo menos 2 critérios de aceite em Dado/Quando/Então, incluindo pelo menos 1 caso de erro.
- [ ] Está ligada a pelo menos um RF do Bloco 2 e tem prioridade MoSCoW.
- [ ] Foi estimada pela equipe em story points e tem **8 SP ou menos**. Com 13, é quebrada antes.
- [ ] As telas foram desenhadas pelo UX, com o **texto de cada tela e o roteiro do áudio** do botão "Ouvir" escritos em linguagem simples.
- [ ] As rotas que ela usa existem no [`openapi.yaml`](../bloco-8-dev/openapi.yaml) ou a mudança no contrato está descrita.
- [ ] As dependências estão prontas ou estão no mesmo sprint, antes dela (por exemplo, o razão contábil antes do saldo).
- [ ] Se mexe com dado pessoal, os campos estão marcados no dicionário de dados (Bloco 5).
- [ ] Se mexe com dinheiro, diz qual transação cria e quais lançamentos (débito e crédito).

## Para tarefas técnicas

- [ ] Tem objetivo e critério de pronto verificável (por exemplo, "`terraform apply` cria a VPC com 2 subnets privadas e 2 públicas em homologação").
- [ ] Está ligada a um ADR, RNF ou risco.
- [ ] Foi estimada em story points e tem 8 SP ou menos.
