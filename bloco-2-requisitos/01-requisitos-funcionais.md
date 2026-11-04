# 2.1 Requisitos Funcionais

32 requisitos, numerados de RF001 a RF032, cada um ligado a uma funcionalidade do Documento de Visão (F01 a F16) e priorizado por MoSCoW.

## Critério de prioridade

| Prioridade | Quando usamos | Quantos |
| --- | --- | --- |
| **Must** | Sem ele o MVP não resolve o problema do Bloco 1, não passa pelo parceiro BaaS ou descumpre a lei | 22 |
| **Should** | Importante para as personas, mas o MVP funciona sem ele por algumas semanas | 6 |
| **Could** | Melhora a experiência. Entra se sobrar capacidade | 2 |
| **Won't** | Fica fora desta versão, de forma consciente | 2 |

## Requisitos

| ID | Requisito | F | Prioridade | Justificativa |
| --- | --- | --- | --- | --- |
| RF001 | O sistema deve permitir abrir conta com foto do documento e selfie, com cada passo explicado em áudio | F01 | Must | Sem conta não há produto. O áudio é o que permite Antônio abrir sozinho |
| RF002 | O sistema deve validar a identidade do cliente no parceiro BaaS antes de liberar a conta | F01 | Must | Exigência do parceiro e das regras de prevenção à lavagem de dinheiro |
| RF003 | O sistema deve pedir uma senha de 6 números e oferecer a biometria do celular no primeiro acesso | F02 | Must | Senha numérica é mais fácil para quem lê pouco. Biometria evita digitar |
| RF004 | O sistema deve permitir entrar com biometria ou senha e bloquear o acesso por 30 minutos após 5 senhas erradas | F02 | Must | Proteção contra tentativa de adivinhar a senha |
| RF005 | O sistema deve manter um único celular ativo por conta e exigir nova selfie para trocar de aparelho | F02 | Must | Impede que o golpista instale a conta da vítima no próprio celular (risco R01) |
| RF006 | O sistema deve mostrar o saldo e o extrato com ícone por tipo de movimentação | F03 | Must | É a ação mais usada. Ícone reduz a necessidade de leitura |
| RF007 | O sistema deve ler em voz alta o conteúdo de qualquer tela pelo botão fixo "Ouvir" | F03 | Must | Princípio 1 do Documento de Visão. Sem isso Antônio e Dona Marlene ficam de fora |
| RF008 | O sistema deve permitir enviar Pix por chave, por contato salvo ou por QR Code | F04 | Must | Pix é o meio de pagamento do dia a dia das três personas |
| RF009 | O sistema deve mostrar e falar o nome do recebedor, o banco e o valor antes da confirmação do Pix | F04 | Must | Última barreira contra golpe e contra erro de digitação (R01) |
| RF010 | O sistema deve permitir receber Pix por chave e por QR Code com valor | F05 | Must | Antônio recebe a diária por Pix. Sem isso ele continua dependendo do parente |
| RF011 | O sistema deve permitir cadastrar e excluir chaves Pix de CPF, celular e aleatória | F05 | Must | Pré-requisito para receber Pix por chave |
| RF012 | O sistema deve gerar comprovante de Pix que pode ser ouvido e compartilhado pelo WhatsApp | F04 | Should | O comprovante é pedido pelo patrão e pela família. O Pix funciona sem ele nas primeiras semanas |
| RF013 | O sistema deve permitir pagar boleto lendo o código pela câmera ou digitando | F06 | Must | Motivação principal da Dona Marlene |
| RF014 | O sistema deve permitir abrir conta para adolescente de 16 ou 17 anos com aceite do responsável legal | F07 | Must | Persona Camila. O aceite do responsável é exigido por lei |
| RF015 | O sistema deve permitir que o responsável defina limite diário e mensal de saída da conta do menor | F08 | Must | Garante a "autonomia com limite" que a Camila e os pais querem |
| RF016 | O sistema deve permitir que o menor peça aprovação para uma saída acima do limite e que o responsável aprove ou recuse no app | F08 | Should | Evita o "tudo bloqueado" dos bancos atuais. O limite fixo já protege no início |
| RF017 | O sistema deve permitir criar meta de economia com nome, valor, data e imagem, guardar e resgatar dinheiro da meta | F09 | Should | Persona Camila (notebook). Não é necessário para movimentar a conta |
| RF018 | O sistema deve permitir cadastrar um contato de confiança, que recebe aviso de movimentação fora do padrão | F10 | Should | Rede de apoio da Dona Marlene sem tirar a autonomia dela |
| RF019 | O sistema deve aplicar limite menor para destinatário novo nas primeiras 24 horas e para Pix entre 20h e 6h | F11 | Must | Os golpes acontecem com destinatário novo e com urgência (R01) |
| RF020 | O sistema deve oferecer o botão "bloquear tudo agora", que suspende na hora todas as saídas de dinheiro | F11 | Must | Resposta imediata quando o cliente percebe o golpe (R01) |
| RF021 | O sistema deve mostrar o aviso "o Rufus nunca liga para você" nas telas de dinheiro e no início do atendimento | F11 | Must | Ataca direto o golpe da falsa central, o que mais cresceu em 2025 |
| RF022 | O sistema deve lembrar o cliente de contas a vencer que ele cadastrou | F12 | Could | Ajuda a Dona Marlene, mas ela já paga as contas sem o lembrete |
| RF023 | O sistema deve oferecer dicas de educação financeira em áudio de até 60 segundos | F13 | Could | Diferencial de educação. Não afeta a movimentação |
| RF024 | O sistema deve permitir abrir chamado de atendimento por chat de dentro do app, já identificado | F14 | Must | É o único canal humano. Começar dentro do app prova que é o Rufus de verdade |
| RF025 | O sistema deve permitir que o atendente veja o histórico do cliente e responda chamados no painel do SAC | F16 | Must | Sem o painel o chamado do RF024 não tem quem responda |
| RF026 | O sistema deve dar uma nota de risco a cada Pix enviado e reter para análise os que passarem do limite de risco | F15 | Must | Prevenção de fraude exigida pelo parceiro e pelo risco R01 |
| RF027 | O sistema deve permitir que o analista antifraude libere, recuse ou bloqueie a conta a partir do painel | F15 | Must | Decisão humana para o Pix retido no RF026 |
| RF028 | O sistema deve enviar notificação push a cada entrada e saída de dinheiro | F03 | Should | O cliente percebe na hora uma saída que não fez. O extrato já mostra o mesmo |
| RF029 | O sistema deve permitir encerrar a conta e baixar os próprios dados pessoais | F14 | Must | Direitos do titular da LGPD (art. 18) |
| RF030 | O sistema deve permitir cadastrar funcionários e atribuir papéis (atendente, analista antifraude, administrador) | F16 | Should | Controle de acesso dos painéis. No início os papéis podem ser cadastrados por script |
| RF031 | Agendar Pix para data futura | F04 | Won't | Pouco valor para as personas e aumenta a superfície de golpe. Fica para a próxima versão |
| RF032 | Entrar no app por reconhecimento de voz | F02 | Won't | A biometria nativa do celular já resolve, sem custo e com mais precisão |

## Rastreabilidade

Cada funcionalidade do Bloco 1 tem pelo menos um requisito:

| F | Requisitos |
| --- | --- |
| F01 Abertura de conta | RF001, RF002 |
| F02 Entrada no app | RF003, RF004, RF005, RF032 |
| F03 Saldo e extrato | RF006, RF007, RF028 |
| F04 Enviar Pix | RF008, RF009, RF012, RF031 |
| F05 Receber Pix | RF010, RF011 |
| F06 Pagar contas | RF013 |
| F07 Conta de menor | RF014 |
| F08 Limites e aprovação | RF015, RF016 |
| F09 Metas | RF017 |
| F10 Contato de confiança | RF018 |
| F11 Proteção contra golpe | RF019, RF020, RF021 |
| F12 Lembrete de contas | RF022 |
| F13 Educação financeira | RF023 |
| F14 Atendimento e direitos | RF024, RF029 |
| F15 Antifraude | RF026, RF027 |
| F16 Painel do SAC | RF025, RF030 |
