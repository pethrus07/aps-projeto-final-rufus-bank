# 9.1 Glossário e modelo de domínio

O modelo de domínio completo (entidades, atributos, tipos e relações) está em [bloco-3-arquitetura/05-modelo-de-dominio.md](../bloco-3-arquitetura/05-modelo-de-dominio.md) e é a fonte única. Este glossário explica os termos em linguagem simples e aponta para lá; ele não redefine nada.

Regra para o time: no código, no banco, nas telas internas e nas conversas usamos **estas palavras e só estas**. Se um termo novo aparecer numa história, ele entra aqui antes de entrar no código.

## Termos do negócio

| Termo | O que significa | No modelo |
| --- | --- | --- |
| Cliente | Pessoa que tem conta no Rufus. Pode ser titular (adulto) ou menor (16 ou 17 anos) | `Cliente`, campo `tipo` |
| Titular | Cliente adulto, responsável pela própria conta | `TipoCliente.TITULAR` |
| Menor | Cliente de 16 ou 17 anos, com conta vinculada a um responsável | `TipoCliente.MENOR` |
| Responsável | Cliente adulto que aceitou o vínculo com um menor e define os limites dele | `VinculoResponsavel.responsavelClienteId` |
| Vínculo | Ligação entre menor e responsável, com os limites diário e mensal | `VinculoResponsavel` |
| Pedido de aprovação | Pedido do menor para fazer uma saída acima do limite. Vale 24 horas | `PedidoAprovacao` |
| Contato de confiança | Pessoa avisada quando sai dinheiro fora do padrão. Não vê o saldo nem movimenta a conta | `ContatoConfianca` |
| Conta | A conta de pagamento do cliente, mantida pelo parceiro BaaS | `Conta` |
| Carteira | Divisão interna do dinheiro de uma conta: a principal e uma por meta. Também existem carteiras técnicas de liquidação | `Carteira` |
| Saldo | Soma dos lançamentos de uma carteira. Nunca é um número editado | Soma de `Lancamento.valorCentavos` |
| Lançamento | Registro de crédito ou débito numa carteira. Toda transação tem pelo menos dois e a soma é zero | `Lancamento` |
| Partidas dobradas | Regra contábil: todo dinheiro que sai de um lugar entra em outro | ADR-007 |
| Transação | Qualquer movimentação: Pix enviado, Pix recebido, boleto, guardar ou resgatar da meta | `Transacao` e subtipos |
| Pix enviado | Transferência instantânea para outra pessoa, por chave, contato ou QR Code | `PixEnvio` |
| Pix recebido | Dinheiro que chega por Pix | `PixRecebimento` |
| Chave Pix | Identificador para receber Pix: CPF, celular ou chave aleatória | `ChavePix` |
| Cobrança (QR Code) | QR Code gerado para receber um valor | rota `POST /pix/cobrancas` |
| Destinatário novo | Quem nunca recebeu Pix daquele cliente. Tem limite menor nas primeiras 24 horas | `PixEnvio.destinatarioNovo` |
| Boleto | Conta paga pela linha digitável ou pelo código de barras | `PagamentoBoleto` |
| Meta | Objetivo de economia, com valor, data e imagem. O dinheiro guardado fica numa carteira própria | `Meta` |
| Bloquear tudo | Botão que suspende todas as saídas de dinheiro na hora | `Conta.status = BLOQUEADA_TOTAL` |
| Pix retido | Pix que o antifraude segurou para análise humana | `StatusTransacao.RETIDA` |
| Nota de risco | Pontuação de 0 a 100 dada pelo antifraude. 70 ou mais retém o Pix | `AnaliseRisco.nota` |
| Chamado | Conversa de atendimento aberta pelo cliente dentro do app | `Chamado`, `MensagemChamado` |
| Funcionário | Pessoa da equipe interna: atendente, analista antifraude ou administrador | `Funcionario`, `Papel` |
| Consentimento | Aceite registrado de termo de uso, privacidade, biometria ou do responsável legal | `Consentimento` |
| Dado pessoal (PII) | Informação que identifica a pessoa. Marcado no dicionário de dados do Bloco 5 | Coluna LGPD do dicionário |

## Termos técnicos

| Termo | O que significa | Onde aparece |
| --- | --- | --- |
| Parceiro BaaS | Instituição autorizada pelo Banco Central que mantém a conta e liquida o Pix e o boleto. O Rufus é a interface | ADR-002, Bloco 1 |
| Porta e adaptador | Interface nossa (porta) e a tradução para cada fornecedor (adaptador) | `PortaBancaria`, `PortaVoz` |
| Adaptador falso | Implementação da porta que responde sem rede, usada no localhost e nos testes | Bloco 8 |
| Chave de idempotência | Código enviado no cabeçalho `Idempotency-Key`. A mesma chave nunca cria duas transações | RNF11, US07 |
| Outbox | Tabela onde a API grava os eventos na mesma transação do dado. O worker lê e executa | ADR-008, `OutboxEvento` |
| Worker | Processo separado da API que executa os eventos do outbox | ADR-009 |
| Saga | Sequência de passos com compensação: reservar saldo, enviar ao parceiro, confirmar ou estornar | Bloco 3, padrões |
| Estorno | Compensação que devolve o dinheiro reservado quando o parceiro recusa ou não responde | `StatusTransacao.ESTORNADA` |
| Conciliação | Comparação diária entre o nosso razão e o extrato do parceiro | RNF11, T18 |
| Token de acesso | JWT de 15 minutos enviado em cada requisição | ADR-010 |
| Token de renovação | Token de 30 dias, trocado a cada uso, que gera um novo token de acesso | `SessaoRenovacao` |
| Dispositivo vinculado | O único celular autorizado a usar a conta. Assina o login com uma chave guardada no próprio aparelho | `Dispositivo`, RF005 |
| TOTP | Código de 6 dígitos que muda a cada 30 segundos, usado como segundo fator dos funcionários | `Funcionario.segredoTotp` |
| p95 | Tempo dentro do qual 95% das requisições respondem | RNF01, RNF02 |
| Story point (SP) | Medida relativa de esforço. Referência: US13 = 3 SP | Bloco 2, Bloco 7 |
| DoR e DoD | Definition of Ready (pronto para entrar no sprint) e Definition of Done (pronto de verdade) | 9.4 e 9.5 |

## Modelo de domínio em uma página

| Módulo | Entidades | Regra mais importante |
| --- | --- | --- |
| identidade | Cliente, Dispositivo, Credencial, SessaoRenovacao, Consentimento | Só 1 dispositivo ativo por cliente |
| contas | Conta, Carteira, Lancamento | A soma dos lançamentos de uma transação é zero |
| pagamentos | Transacao (PixEnvio, PixRecebimento, PagamentoBoleto, MovimentoMeta), ChavePix, Meta | A mesma chave de idempotência não cria duas transações |
| familia | VinculoResponsavel, PedidoAprovacao, ContatoConfianca | O menor não passa do limite sem aprovação do responsável |
| antifraude | AnaliseRisco | Nota 70 ou mais retém o Pix |
| atendimento | Chamado, MensagemChamado | Toda consulta de funcionário a dados do cliente vai para a auditoria |
| backoffice | Funcionario, RegistroAuditoria | Registro de auditoria nunca é alterado e fica 5 anos |
| notificacao | Notificacao, OutboxEvento, LembreteConta | Evento só é marcado como processado depois de executado |

O diagrama de classes com tipos, visibilidades e relações está no Bloco 4.
