# 2.4 Regras de negócio

Regras de negócio são as políticas do Rufus que valem independentemente da tela ou da tecnologia. São 16, cada uma com a origem e o lugar onde é garantida. Quando a regra vive no banco de dados, nem um erro no código consegue quebrá-la.

| ID | Regra | Origem | Garantida em |
| --- | --- | --- | --- |
| RN01 | Titular precisa ter 18 anos ou mais. De 16 a 17 anos, a conta só existe vinculada a um responsável legal. Menor de 16 não abre conta | Código Civil, art. 4º (16 a 18 anos assistidos pelos pais) | API (`FabricaDeConta`) e banco (vínculo obrigatório) |
| RN02 | Cada cliente tem um único celular ativo. Trocar de aparelho exige selfie aprovada pelo parceiro, desconecta o aparelho anterior e avisa o contato de confiança | RF005, risco R01 | Banco (índice único parcial `ux_dispositivo_um_ativo_por_cliente`) |
| RN03 | A senha tem 6 números. Depois de 5 erros seguidos, o acesso fica bloqueado por 30 minutos | RF004 | API (`Credencial`) |
| RN04 | Pix para um destinatário que nunca recebeu do cliente: até R$ 300 por Pix nas primeiras 24 horas | RF019, risco R01 | API (`MotorAntifraude`) |
| RN05 | Entre 20h e 6h, o total de Pix entre pessoas físicas fica limitado a R$ 1.000 por conta | Resolução BCB 142/2021, art. 2º, I | API (`MotorAntifraude`) |
| RN06 | Pix com nota de risco de 70 ou mais fica retido e só segue com a decisão de um analista | RF026 | Banco (restrição na `analise_risco`) e API |
| RN07 | "Bloquear tudo agora" suspende todas as saídas de dinheiro na hora. Desbloquear exige selfie e só vale 1 hora depois | RF020 | Banco (`conta.status`) e API |
| RN08 | Na conta de menor, o responsável define o limite diário e o mensal. O diário nunca passa do mensal | RF015 | Banco (restrição de verificação no `vinculo_responsavel`) |
| RN09 | O pedido de aprovação do menor expira em 24 horas. Sem resposta, conta como recusado | RF016, US18 | Worker (evento de expiração) |
| RN10 | O convite ao responsável expira em 7 dias. Se expirar, o cadastro do menor é cancelado e os dados enviados são apagados | US09, LGPD art. 14 | Worker e banco (`expira_em`) |
| RN11 | O contato de confiança é avisado quando sai um Pix acima de 3 vezes a média dos Pix enviados nos últimos 90 dias. Ele nunca vê o saldo nem movimenta a conta | RF018, US13 | API (`familia`) |
| RN12 | Toda movimentação gera lançamentos que somam zero. O saldo é a soma dos lançamentos e nunca é editado | ADR-007, RNF11 | Banco (gatilho adiado de partidas dobradas) |
| RN13 | O mesmo pedido de dinheiro, com a mesma chave de idempotência na mesma conta, nunca gera duas transações | RNF11, US07 | Banco (índice único `ux_transacao_idempotencia`) |
| RN14 | A conta só é encerrada com saldo zero. Os dados pessoais são anonimizados e os registros financeiros ficam guardados por 5 anos | RF029, Lei 9.613/1998, art. 10, §2º | API e banco (lançamentos e auditoria só aceitam inserção) |
| RN15 | O Rufus nunca liga para o cliente. O atendimento humano só começa de dentro do app, com o cliente já autenticado | RF021, RF024 | App e processo do SAC |
| RN16 | O funcionário só vê o que o papel dele permite, e toda consulta a dado de cliente gera um registro de auditoria | RF030, RNF14 | API (RBAC) e banco (`registro_auditoria`) |

As regras RN02, RN06, RN08, RN12 e RN13 foram testadas no PostgreSQL real: os casos que deveriam ser recusados foram recusados (Bloco 5, `testes/resultado.txt`).
