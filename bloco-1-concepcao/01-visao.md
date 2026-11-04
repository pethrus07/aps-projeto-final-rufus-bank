# 1. Documento de Visão

## Nome e slogan

| | |
| --- | --- |
| Nome | **Rufus Bank** |
| Slogan | **"Rufus, iluminando sua vida financeira"** |
| Domínio | Fintech: conta digital, pagamentos e controle financeiro |

## Problema real

Bancos digitais têm interfaces complexas, cheias de jargão e com menus escondidos. Isso exclui quem tem pouca leitura, pouca familiaridade com tecnologia ou com finanças. O problema hoje não é ter conta: é conseguir usar a conta sozinho e com segurança.

Os dados mostram isso:

| Dado | Número | Fonte |
| --- | --- | --- |
| Adultos que não usaram nenhum produto financeiro em 2024 (nem Pix, nem boleto, nem crédito) | 21,1 milhões (11,6% dos adultos). Predominam idosos e pessoas sem emprego formal | [Banco Central, Relatório de Cidadania Financeira 2025](https://www.bcb.gov.br/content/cidadaniafinanceira/documentos_cidadania/RIF/relatorio_de_cidadania_financeira_2025.pdf), seção 1.1 |
| Acerto médio nas perguntas de conhecimento financeiro | 53%. O Brasil fica em 33º lugar, abaixo da média mundial | Idem, seção 1.2 (pesquisa OCDE/INFE de 2023) |
| Pessoas que erraram uma conta simples de juros | 87% | Idem, seção 1.2 |
| Relação do letramento financeiro com idade e escolaridade | Cai com a idade e sobe com a escolaridade | Idem, seção 1.2 |
| Idosos (60+) que usam internet | 59%, contra 43% em 2022 | Idem, citando a TIC Domicílios 2024 |
| Analfabetos funcionais (15 a 64 anos) | 29%. Na faixa de 50 a 64 anos, 51% | [Inaf 2024, divulgado em 05/05/2025](https://www.unicef.org/brazil/comunicados-de-imprensa/analfabetismo-funcional-nao-apresenta-melhora-e-alcanca-29-por-cento-dos-brasileiros-mesmo-patamar-de-2018-aponta-novo-levantamento-do-inaf) |
| Analfabetos funcionais que usam internet | 73%, mas 60% deles estão no nível mais baixo de habilidade digital | Idem |
| Golpe da falsa central ou falso funcionário de banco | 139 mil relatos no 1º semestre de 2025, alta de 195,7% sobre 2024 | [Febraban, divulgado em 11/11/2025](https://conexaoto.com.br/2025/11/11/golpe-da-falsa-venda-e-o-mais-aplicado-contra-clientes-bancarios-no-1o-semestre-do-ano) |

Leitura dos dados: quase todo mundo já tem acesso, mas uma parte grande da população lê com dificuldade, entende pouco de juros e é alvo de golpes. São exatamente as pessoas que os apps atuais atendem mal.

## Proposta de valor

Um banco digital com interface simples, linguagem clara e foco em quem os bancos tradicionais atendem mal.

Na prática, isso vira cinco princípios que valem para todas as telas e que os próximos blocos precisam cumprir:

1. **Ícone e áudio em toda tela.** Tudo que está escrito pode ser ouvido. Quem não lê bem não fica de fora.
2. **Poucos passos.** As ações principais (ver saldo, mandar Pix, pagar conta) terminam em no máximo 3 toques depois do login.
3. **Linguagem do dia a dia.** Frases curtas, sem jargão. "Dinheiro que você tem" no lugar de "saldo disponível".
4. **Proteção contra golpe por padrão.** O Rufus nunca liga para o cliente. Antes de mandar dinheiro, o app fala em voz alta para quem vai e quanto.
5. **Autonomia com rede de apoio.** O cliente usa sozinho, mas pode ter um contato de confiança e, no caso de menor de idade, um responsável vinculado.

## Público-alvo

Adultos com baixa escolaridade ou pouca familiaridade digital, idosos e adolescentes de 16 e 17 anos com renda própria. As três personas do item 2 representam esses grupos.

## Atores do sistema

O enunciado pede no mínimo 4 atores. O Rufus tem 6 humanos e 3 sistemas externos:

| Ator | Tipo | O que faz |
| --- | --- | --- |
| Cliente titular | Humano | Usa a conta: saldo, Pix, contas, metas |
| Cliente menor (16 e 17 anos) | Humano | Usa a conta dentro dos limites aprovados pelo responsável |
| Responsável legal | Humano | Autoriza a conta do menor, define limites e aprova pedidos |
| Contato de confiança | Humano | Recebe aviso de movimentação fora do padrão (familiar ou cuidador) |
| Atendente do SAC | Humano | Atende chamados abertos dentro do app |
| Analista antifraude | Humano | Analisa transações suspeitas e bloqueia contas |
| Parceiro BaaS | Sistema externo | Instituição autorizada pelo Banco Central que mantém a conta e liquida o Pix |
| Serviço de voz | Sistema externo | Transforma texto em fala (Amazon Polly) |
| Serviço de notificação | Sistema externo | Envia push e SMS |

## Funcionalidades macro

O enunciado pede no mínimo 12. São 16, que o Bloco 2 detalha em requisitos com MoSCoW:

| # | Funcionalidade | Persona que mais precisa |
| --- | --- | --- |
| F01 | Abertura de conta guiada por voz, com foto do documento e selfie | Antônio, Dona Marlene |
| F02 | Entrada no app por biometria do celular ou senha de 6 números | Todas |
| F03 | Saldo e extrato com ícones e leitura em voz alta | Antônio, Dona Marlene |
| F04 | Enviar Pix por contato, chave ou QR Code, com confirmação falada | Todas |
| F05 | Receber Pix por QR Code ou chave | Antônio |
| F06 | Pagar boleto e contas de consumo apontando a câmera | Dona Marlene |
| F07 | Conta de menor vinculada ao responsável | Camila |
| F08 | Limites e pedidos de aprovação ao responsável | Camila |
| F09 | Metas de economia com progresso em imagem ("cofrinho") | Camila |
| F10 | Contato de confiança, avisado em movimentação fora do padrão | Dona Marlene |
| F11 | Alertas contra golpe e botão "bloquear tudo agora" | Todas |
| F12 | Lembrete de conta a vencer | Dona Marlene |
| F13 | Dicas curtas de educação financeira em áudio | Camila, Antônio |
| F14 | Atendimento humano iniciado só de dentro do app | Todas |
| F15 | Painel antifraude para análise de transações suspeitas | Analista antifraude |
| F16 | Painel do SAC com histórico do cliente | Atendente do SAC |

## Fora do escopo

| Fora do escopo | Por quê |
| --- | --- |
| Atendimento presencial (agências, postos) | O produto é 100% digital. O atendimento humano existe, mas dentro do app (F14) |
| Crédito, empréstimo e cartão de crédito | Endividamento é um risco alto para o público-alvo, e crédito exige outra regulação. Fica para uma fase futura |
| Investimentos | Exige outra autorização e outro nível de letramento. Fica para uma fase futura |
| Conta para empresa (PJ ou MEI) | O público é pessoa física |
| Cartão físico e saque em dinheiro | Dependem de logística e de rede de terceiros. O MVP fica no Pix e no boleto |
| Câmbio, conta em outra moeda e criptoativos | Fora do problema que o projeto resolve |
| Versão web completa para o cliente | O público usa celular. Na web existe só o site institucional e os painéis internos (F15 e F16) |
| Core bancário próprio | A conta e a liquidação ficam com o parceiro BaaS (ver item 4) |
