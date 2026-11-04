# 2.3 Histórias de Usuário

24 histórias no formato "Como [persona], quero [ação], para [objetivo]", cada uma com critérios de aceite em Given/When/Then (Dado/Quando/Então) e estimativa em story points.

## Escala de story points

Sequência de Fibonacci (1, 2, 3, 5, 8, 13), estimada pela equipe por comparação. A história de referência é a **US13 (cadastrar contato de confiança) = 3 pontos**: um formulário, uma regra e uma notificação. Uma história de 13 pontos é grande demais para um sprint e precisa ser quebrada antes de entrar.

## Resumo

| ID | Persona | História | RF | MoSCoW | SP |
| --- | --- | --- | --- | --- | --- |
| US01 | Antônio | Abrir a conta ouvindo cada passo | RF001, RF002 | Must | 8 |
| US02 | Antônio | Entrar com a digital | RF003, RF004 | Must | 5 |
| US03 | Dona Marlene | Trocar de celular com selfie | RF005 | Must | 5 |
| US04 | Antônio | Ouvir o saldo e o extrato | RF006, RF007 | Must | 5 |
| US05 | Antônio | Receber a diária por QR Code | RF010, RF011 | Must | 5 |
| US06 | Dona Marlene | Enviar Pix ouvindo para quem vai | RF008, RF009 | Must | 8 |
| US07 | Antônio | Não mandar Pix em dobro | RF008, RNF11 | Must | 3 |
| US08 | Dona Marlene | Pagar boleto pela câmera | RF013 | Must | 8 |
| US09 | Camila | Abrir conta com aceite do pai | RF014 | Must | 8 |
| US10 | Responsável da Camila | Definir limite da conta da filha | RF015 | Must | 3 |
| US11 | Antônio | Ter limite menor com destinatário novo e à noite | RF019 | Must | 3 |
| US12 | Dona Marlene | Bloquear tudo na hora | RF020, RF021 | Must | 3 |
| US14 | Antônio | Falar com uma pessoa pelo chat do app | RF024 | Must | 5 |
| US15 | Atendente do SAC | Responder chamado vendo o histórico | RF025 | Must | 5 |
| US16 | Analista antifraude | Analisar Pix retido | RF026, RF027 | Must | 8 |
| US17 | Antônio | Encerrar a conta e baixar meus dados | RF029 | Must | 5 |
| US13 | Dona Marlene | Cadastrar o neto como contato de confiança | RF018 | Should | 3 |
| US18 | Camila | Pedir aprovação acima do limite | RF016 | Should | 5 |
| US19 | Camila | Criar a meta do notebook | RF017 | Should | 5 |
| US20 | Camila | Receber aviso de cada movimentação | RF028 | Should | 3 |
| US21 | Dona Marlene | Ouvir e compartilhar o comprovante | RF012 | Should | 3 |
| US22 | Administrador | Cadastrar funcionário com papel | RF030 | Should | 3 |
| US23 | Dona Marlene | Lembrete de conta a vencer | RF022 | Could | 3 |
| US24 | Camila | Ouvir dicas de dinheiro | RF023 | Could | 2 |
| | | **Total** | | | **114** |

Must: 87 pontos em 16 histórias. Should: 22 pontos em 6 histórias. Could: 5 pontos em 2 histórias. O Bloco 7 soma a isso as tarefas técnicas (infraestrutura, pipeline, integração com o parceiro) e calcula os sprints.

## Histórias com critérios de aceite

### US01 · Abrir a conta ouvindo cada passo (8 SP, Must)

Como **Antônio**, quero abrir minha conta ouvindo o que fazer em cada passo, para não depender de ninguém para ler as instruções.

- **Dado** que instalei o app e toquei em "Abrir conta", **quando** cada tela aparece, **então** a instrução é falada automaticamente e pode ser repetida pelo botão "Ouvir".
- **Dado** que enviei foto do documento e selfie, **quando** o parceiro aprova a identidade, **então** a conta fica ativa e o app avisa por voz e por push.
- **Dado** que a foto ficou escura ou cortada, **quando** o envio é recusado, **então** o app fala o motivo em uma frase ("a foto ficou escura, tente perto da janela") e permite tentar de novo.

### US02 · Entrar com a digital (5 SP, Must)

Como **Antônio**, quero entrar no app com a minha digital, para não precisar lembrar nem digitar senha.

- **Dado** que criei a senha de 6 números, **quando** aceito usar a biometria, **então** os próximos acessos pedem só a digital.
- **Dado** que errei a senha 5 vezes, **quando** tento a 6ª, **então** o acesso fica bloqueado por 30 minutos e o app explica por voz.
- **Dado** que meu celular não tem biometria, **quando** entro, **então** o app pede a senha de 6 números com teclado grande.

### US03 · Trocar de celular com selfie (5 SP, Must)

Como **Dona Marlene**, quero que só o meu celular acesse a minha conta, para que ninguém instale minha conta em outro aparelho.

- **Dado** que minha conta já está ativa num celular, **quando** alguém tenta entrar em outro aparelho, **então** o app exige uma selfie nova e só libera se ela bater com a do cadastro.
- **Dado** que a troca de aparelho foi aprovada, **quando** a nova sessão começa, **então** o aparelho antigo é desconectado e eu recebo aviso no contato cadastrado.

### US04 · Ouvir o saldo e o extrato (5 SP, Must)

Como **Antônio**, quero ouvir quanto dinheiro eu tenho e o que entrou e saiu, para saber das minhas contas sem ler.

- **Dado** que entrei no app, **quando** a tela inicial abre, **então** o saldo aparece em número grande com o botão "Ouvir" ao lado.
- **Dado** que toquei em "Ouvir" no extrato, **quando** o áudio toca, **então** cada movimentação é falada como "Recebeu 120 reais de José, ontem".
- **Dado** que estou na tela inicial, **quando** quero ver o extrato, **então** chego nele com 1 toque.

### US05 · Receber a diária por QR Code (5 SP, Must)

Como **Antônio**, quero mostrar um QR Code para o mestre de obras me pagar, para receber a diária na minha conta.

- **Dado** que toquei em "Receber", **quando** digito o valor (ou deixo em branco), **então** o app mostra um QR Code Pix em tela cheia.
- **Dado** que o pagamento caiu, **quando** o parceiro confirma, **então** o celular vibra, fala "Recebeu 150 reais de Carlos" e o saldo é atualizado.

### US06 · Enviar Pix ouvindo para quem vai (8 SP, Must)

Como **Dona Marlene**, quero ouvir o nome de quem vai receber e o valor antes de confirmar, para ter certeza de que não estou errando.

- **Dado** que informei a chave e o valor, **quando** chego na tela de confirmação, **então** o app mostra e fala o nome do recebedor, o banco e o valor.
- **Dado** que confirmei com a biometria, **quando** o parceiro aceita o Pix, **então** o app mostra "Pix enviado" com ícone verde em até 10 segundos (RNF02).
- **Dado** que o saldo não é suficiente, **quando** tento confirmar, **então** o app avisa antes de pedir a biometria e não envia nada.

### US07 · Não mandar Pix em dobro (3 SP, Must)

Como **Antônio**, quero que o Pix não saia duas vezes se eu apertar o botão de novo, para não perder dinheiro.

- **Dado** que toquei em "confirmar" e a internet caiu, **quando** o app reenvia o pedido, **então** o servidor reconhece a mesma chave de idempotência e devolve o resultado do primeiro pedido.
- **Dado** que toquei duas vezes seguidas, **quando** os dois pedidos chegam, **então** só um Pix é criado.

### US08 · Pagar boleto pela câmera (8 SP, Must)

Como **Dona Marlene**, quero apontar a câmera para a conta de luz e pagar, para não precisar digitar aquele número enorme.

- **Dado** que abri "Pagar conta", **quando** aponto a câmera para o código de barras, **então** o app lê o código e mostra e fala a empresa, o valor e o vencimento.
- **Dado** que o código não foi lido em 15 segundos, **quando** o tempo acaba, **então** o app oferece digitar o código com teclado grande.
- **Dado** que o boleto está vencido, **quando** o valor é calculado, **então** o app mostra os juros separados e fala o total.

### US09 · Abrir conta com aceite do pai (8 SP, Must)

Como **Camila**, quero abrir minha conta com meu pai aceitando pelo celular dele, para não precisar ir a lugar nenhum.

- **Dado** que informei que tenho 17 anos, **quando** termino meu cadastro, **então** o app pede o CPF e o celular do responsável e envia um convite para ele.
- **Dado** que meu pai abriu o convite, **quando** ele confirma a identidade e aceita os termos, **então** minha conta fica ativa vinculada a ele.
- **Dado** que o responsável não aceitou em 7 dias, **quando** o prazo vence, **então** o pedido é cancelado e os dados enviados são apagados.

### US10 · Definir limite da conta da filha (3 SP, Must)

Como **responsável da Camila**, quero definir quanto ela pode gastar por dia e por mês, para ela ter autonomia sem risco.

- **Dado** que sou o responsável vinculado, **quando** defino o limite diário e o mensal, **então** os novos limites valem na hora.
- **Dado** que a Camila tenta um Pix acima do limite, **quando** ela confirma, **então** o Pix não é enviado e ela vê a opção de pedir aprovação (US18).

### US11 · Limite menor com destinatário novo e à noite (3 SP, Must)

Como **Antônio**, quero que o app limite Pix para alguém novo e à noite, para que um golpista não leve tudo de uma vez.

- **Dado** que o destinatário nunca recebeu Pix meu, **quando** envio nas primeiras 24 horas, **então** o limite é de R$ 300 por Pix.
- **Dado** que são entre 20h e 6h, **quando** envio um Pix, **então** o limite é de R$ 1.000 por período, como na regra do Pix noturno.
- **Dado** que bati o limite, **quando** a mensagem aparece, **então** o app explica o motivo em uma frase e diz quando libera.

### US12 · Bloquear tudo na hora (3 SP, Must)

Como **Dona Marlene**, quero um botão para travar a conta na hora, para me proteger se eu achar que caí num golpe.

- **Dado** que toquei em "bloquear tudo agora" e confirmei, **quando** o bloqueio é aplicado, **então** nenhuma saída de dinheiro é aceita e o contato de confiança é avisado.
- **Dado** que a conta está bloqueada, **quando** eu quiser desbloquear, **então** preciso de selfie e de 1 hora de espera.
- **Dado** que estou em qualquer tela de dinheiro, **quando** ela abre, **então** aparece o aviso "o Rufus nunca liga para você".

### US13 · Cadastrar o neto como contato de confiança (3 SP, Should)

Como **Dona Marlene**, quero que meu neto seja avisado se sair dinheiro estranho da minha conta, para ter ajuda sem dar a ele acesso à conta.

- **Dado** que informei o nome e o celular do meu neto, **quando** ele aceita o convite, **então** ele vira meu contato de confiança.
- **Dado** que sai um Pix acima de 3 vezes a minha média, **quando** o Pix é confirmado, **então** meu neto recebe aviso com o valor, sem ver meu saldo.

### US14 · Falar com uma pessoa pelo chat do app (5 SP, Must)

Como **Antônio**, quero falar com uma pessoa de dentro do app, para ter certeza de que é o banco mesmo.

- **Dado** que toquei em "Falar com uma pessoa", **quando** o chat abre, **então** o atendente já sabe quem eu sou e eu não preciso informar senha nem código.
- **Dado** que prefiro falar, **quando** toco no microfone, **então** posso mandar mensagem de áudio no chat.

### US15 · Responder chamado vendo o histórico (5 SP, Must)

Como **atendente do SAC**, quero ver o histórico do cliente ao abrir o chamado, para resolver sem fazer o cliente repetir tudo.

- **Dado** que abri um chamado, **quando** o painel carrega, **então** vejo os chamados anteriores e as últimas 10 movimentações do cliente.
- **Dado** que respondi o chamado, **quando** o cliente lê, **então** a resposta também pode ser ouvida no app.
- **Dado** que consultei os dados do cliente, **quando** a consulta acontece, **então** ela fica registrada na auditoria (RNF14).

### US16 · Analisar Pix retido (8 SP, Must)

Como **analista antifraude**, quero ver os Pix retidos com o motivo da nota de risco, para decidir rápido se libero ou bloqueio.

- **Dado** que um Pix passou da nota de risco, **quando** ele é retido, **então** aparece na fila do painel com o motivo (destinatário novo, valor fora do padrão, horário).
- **Dado** que liberei o Pix, **quando** a decisão é salva, **então** o Pix segue para o parceiro e o cliente é avisado.
- **Dado** que recusei e bloqueei, **quando** a decisão é salva, **então** o valor volta ao saldo, a conta fica bloqueada e o cliente recebe aviso para falar com o SAC pelo app.

### US17 · Encerrar a conta e baixar meus dados (5 SP, Must)

Como **Antônio**, quero encerrar minha conta e receber meus dados, para exercer meus direitos.

- **Dado** que pedi para baixar meus dados, **quando** o arquivo fica pronto, **então** recebo no app um arquivo com meus dados pessoais e movimentações.
- **Dado** que pedi o encerramento com saldo zero, **quando** confirmo, **então** a conta é encerrada e os dados pessoais são anonimizados, mantidos só os registros que a lei obriga guardar.

### US18 · Pedir aprovação acima do limite (5 SP, Should)

Como **Camila**, quero pedir ao meu pai para liberar um gasto acima do limite, para não ficar travada quando preciso.

- **Dado** que meu Pix passou do limite, **quando** toco em "pedir aprovação", **então** meu responsável recebe push com valor e destinatário.
- **Dado** que ele aprovou em até 24 horas, **quando** a aprovação chega, **então** o Pix é enviado e eu sou avisada.
- **Dado** que ele recusou ou não respondeu em 24 horas, **quando** o prazo acaba, **então** o pedido é cancelado.

### US19 · Criar a meta do notebook (5 SP, Should)

Como **Camila**, quero criar uma meta com a foto do notebook e ver quanto falta, para ter motivação para guardar.

- **Dado** que criei a meta com nome, valor e data, **quando** guardo dinheiro nela, **então** o valor sai do saldo e a barra de progresso avança.
- **Dado** que resgatei da meta, **quando** confirmo, **então** o valor volta para o saldo.

### US20 · Receber aviso de cada movimentação (3 SP, Should)

Como **Camila**, quero receber notificação de cada entrada e saída, para saber na hora se algo estranho aconteceu.

- **Dado** que entrou ou saiu dinheiro, **quando** o lançamento é confirmado, **então** recebo push em até 30 segundos com valor e tipo.

### US21 · Ouvir e compartilhar o comprovante (3 SP, Should)

Como **Dona Marlene**, quero mandar o comprovante pelo WhatsApp, para provar que paguei.

- **Dado** que o Pix ou boleto foi concluído, **quando** toco em "comprovante", **então** vejo o comprovante, posso ouvi-lo e compartilhar como imagem.

### US22 · Cadastrar funcionário com papel (3 SP, Should)

Como **administrador**, quero cadastrar funcionários com um papel, para que cada um veja só o que precisa.

- **Dado** que cadastrei um atendente, **quando** ele entra no painel, **então** vê os chamados mas não a fila antifraude.
- **Dado** que o funcionário entra pela primeira vez, **quando** faz login, **então** é obrigado a configurar o segundo fator.

### US23 · Lembrete de conta a vencer (3 SP, Could)

Como **Dona Marlene**, quero ser lembrada da conta de água, para não pagar multa.

- **Dado** que cadastrei a conta com dia de vencimento, **quando** faltam 3 dias, **então** recebo push e o lembrete aparece na tela inicial.

### US24 · Ouvir dicas de dinheiro (2 SP, Could)

Como **Camila**, quero ouvir dicas curtas sobre dinheiro, para aprender a guardar melhor.

- **Dado** que abri "Dicas", **quando** escolho uma, **então** ouço um áudio de até 60 segundos e posso ler o texto.
