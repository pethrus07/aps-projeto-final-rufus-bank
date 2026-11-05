# Bloco 1 · Concepção e Escopo

O que vamos construir e por quê. Os cinco itens pedidos no enunciado (slide 6):

| Item | Arquivo | Resumo |
| --- | --- | --- |
| 1. Documento de Visão | [01-visao.md](01-visao.md) | Nome, slogan, problema com dados reais do Banco Central, Inaf e Febraban, proposta de valor, 10 atores, 16 funcionalidades, fora do escopo |
| 2. Personas | [02-personas.md](02-personas.md) | Antônio (47, baixa leitura), Camila (17, jovem aprendiz), Dona Marlene (68, aposentada) |
| 3. Mapa de Stakeholders | [03-stakeholders.md](03-stakeholders.md) | 10 stakeholders com interesse, influência e estratégia, matriz poder x interesse |
| 4. Estudo de Viabilidade | [04-viabilidade.md](04-viabilidade.md) | Técnica, operacional e custo mensal real: R$ 3.790,14 em produção, R$ 1.136,64 em homologação e R$ 519,62 de serviços fora da AWS, todos com fonte |
| 5. Riscos iniciais | [05-riscos.md](05-riscos.md) | 8 riscos com probabilidade, impacto, severidade, mitigação e sinal de alerta |

## O que este bloco obriga nos próximos

O enunciado avisa que inconsistência entre blocos tira nota. Estas decisões do Bloco 1 precisam aparecer iguais depois:

| Decidido aqui | Então, obrigatoriamente |
| --- | --- |
| 16 funcionalidades (F01 a F16) | Bloco 2: cada uma vira pelo menos um RF com MoSCoW. Os mesmos atores aparecem no diagrama de casos de uso (Bloco 4) |
| 10.000 usuários ativos por mês | Bloco 2: RNF de escalabilidade com esse número. Bloco 6: a mesma carga |
| 99,9% de disponibilidade | Bloco 2: RNF com esse número. Bloco 6: 2 zonas, banco Multi-AZ, balanceador e failover |
| Ações principais em no máximo 3 toques, áudio em toda tela | Bloco 2: RNFs de usabilidade com esses números |
| Parceiro BaaS para conta e Pix | Bloco 3: ADR da integração isolada em camada própria. Bloco 4: o parceiro aparece como sistema externo |
| PostgreSQL como escolha preliminar | Bloco 3 e Bloco 5: ADR comparando com a alternativa descartada |
| AWS sa-east-1, Fargate, RDS, ALB, WAF | Bloco 6: o diagrama de infra usa estas peças. Se mudar, rodar de novo o script de custo |
| LGPD, dados de menores e biometria | Bloco 5: campos com dado pessoal marcados no dicionário de dados. Biometria nunca vai para o banco |
| 8 riscos iniciais | Bloco 7: a matriz de riscos parte destes 8 |

## Pendências para o grupo

- [x] Equipe: Pedro Oliveira (PO), Izaias Terto (Arquiteto), Carlos Eduardo (DBA). Os nomes ficam em `projeto.json` e entram em todos os diagramas.
- [ ] Confirmar o slogan. O usado é "Rufus, iluminando sua vida financeira". A outra opção era "o melhor amigo do homem moderno".
- [ ] Camila: o texto original dizia "primeiro estágio" e "jovem aprendiz". São contratos diferentes por lei. Ficou jovem aprendiz. Trocar se o grupo preferir estágio.
- [ ] Fora do escopo: o grupo tinha só "atendimento presencial". Foram acrescentados 7 itens (crédito, investimentos, PJ, cartão físico, câmbio, web completa, core próprio). Revisar.
- [ ] Stakeholders: foi acrescentado o parceiro BaaS. Riscos: foram acrescentados R07 e R08.
- [ ] DBA: lançar os itens de [custo-gerado.md](../ferramentas/custo-infra/custo-gerado.md) em https://calculator.aws (região São Paulo), salvar o link público da estimativa e colar aqui. O professor citou a calculadora; os preços do script vêm da mesma tabela oficial, mas o link é a prova mais fácil de mostrar.
