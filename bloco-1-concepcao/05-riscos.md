# 5. Riscos iniciais

Os dois riscos mais graves são **golpe contra o usuário vulnerável (R01)** e **baixa adesão (R06)**: os dois atacam o motivo de o Rufus existir. Seis riscos vieram do grupo e dois foram acrescentados (R07 e R08) para cobrir as categorias equipe e regulatório, que a matriz do Bloco 7 exige (mínimo de 8).

## Escala

| Nota | Probabilidade | Impacto |
| --- | --- | --- |
| 1 | Baixa: pode não acontecer no 1º ano | Baixo: atrasa ou incomoda, sem dano ao cliente |
| 2 | Média: pode acontecer no 1º ano | Médio: perda de dinheiro ou prazo que dá para recuperar |
| 3 | Alta: deve acontecer no 1º ano | Alto: dano ao cliente, multa ou ameaça à existência do produto |

**Severidade = probabilidade x impacto** (de 1 a 9). De 6 para cima, o risco tem dono e plano desde o início.

## Riscos

| ID | Risco | Categoria | Prob. | Impacto | Severidade | Mitigação | Sinal de alerta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R01 | Fraudes e golpes contra usuários vulneráveis | Segurança | 3 | 3 | **9** | O app avisa em toda tela de dinheiro que o Rufus nunca liga pedindo senha. Atendimento só começa de dentro do app. Antes do Pix, o app fala o nome de quem recebe e o valor. Limite menor para destinatário novo e à noite. Contato de confiança avisado em movimentação fora do padrão. Botão "bloquear tudo agora". Analista antifraude para casos suspeitos | Pedidos de devolução de Pix e contestações por mês |
| R02 | Vazamento de dados pessoais | Segurança e regulatório | 2 | 3 | **6** | Criptografia em trânsito e em repouso. Coletar só o dado necessário. Segredos no Secrets Manager, nunca no código. WAF na entrada. Acesso administrativo com dois fatores. Log sem dado pessoal. Teste de invasão antes do lançamento. Plano de resposta a incidente com comunicação à ANPD e aos titulares | Alertas de acesso anormal, achados de teste de invasão |
| R03 | Usuários não conseguem usar o app (o oposto do objetivo) | Negócio | 2 | 3 | **6** | Teste de uso com pessoas do perfil das personas a cada sprint. Áudio e ícone em toda tela. Linguagem simples revisada. Medir onde as pessoas desistem em cada fluxo | Taxa de abandono por tela, chamados de "não consigo" no SAC |
| R04 | Não conseguir parceria regulatória (BaaS) | Regulatório e negócio | 2 | 3 | **6** | Negociar com pelo menos 2 parceiros ao mesmo tempo. Isolar a integração com o parceiro numa camada própria, para trocar de parceiro sem reescrever o sistema (vira ADR no Bloco 3). Começar a conversa antes do desenvolvimento | Nenhum contrato assinado até o fim do 1º sprint |
| R05 | Custo de infraestrutura muito maior que o esperado | Técnico e financeiro | 2 | 2 | **4** | Alerta de orçamento na AWS quando o gasto passar de 80% do previsto (R$ 3.790,14 em produção na AWS). Tag de custo por ambiente. Homologação desligada fora do horário de trabalho. Frases fixas em áudio geradas uma vez e guardadas. Reserva de capacidade depois de 3 meses de uso estável | Fatura parcial acima de 80% do orçamento antes do dia 20 |
| R06 | Baixa adesão | Negócio | 3 | 3 | **9** | Conta sem tarifa. Chegar ao público por quem ele confia: a família (o neto convida a avó), associações, igrejas e quem paga diária na construção civil. Programa de indicação. Medir o uso, não só o download | Contas abertas e usuários ativos por mês abaixo da meta de 10.000 |
| R07 | Equipe sem experiência em acessibilidade e em produto financeiro | Equipe | 2 | 2 | **4** | Guia de acessibilidade no padrão do projeto (Bloco 8). Revisão de acessibilidade na Definition of Done (Bloco 9). Pelo menos uma pessoa com experiência em fintech na equipe (Bloco 7) | Telas reprovadas no teste de uso por motivo de acessibilidade |
| R08 | Erro no tratamento de dados de menores e de dado biométrico | Regulatório | 2 | 3 | **6** | Consentimento do responsável registrado com data e versão do termo. Biometria só no celular, sem guardar no servidor. Campos com dado pessoal marcados no dicionário de dados (Bloco 5) | Pedido de titular ou da ANPD sem resposta no prazo |

## Matriz de risco

| | Impacto 1 | Impacto 2 | Impacto 3 |
| --- | --- | --- | --- |
| **Probabilidade 3** | | | R01, R06 |
| **Probabilidade 2** | | R05, R07 | R02, R03, R04, R08 |
| **Probabilidade 1** | | | |

Nenhum risco ficou com probabilidade baixa: o projeto lida com dinheiro de um público que já é alvo de golpe, então o grupo preferiu ser conservador.
