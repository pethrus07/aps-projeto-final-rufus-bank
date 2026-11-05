# 3.5 Modelo de domínio (fonte única)

Este arquivo é a **fonte única** das entidades, atributos, tipos e relações do Rufus. O diagrama de classes (Bloco 4), o banco de dados (Bloco 5), o contrato OpenAPI (Bloco 8) e o glossário (Bloco 9) seguem exatamente estes nomes. Mudou aqui, muda lá.

Convenções: nomes de classe em PascalCase e de atributo em camelCase no código; no banco, tabelas e colunas em snake_case com os mesmos nomes. Dinheiro sempre em centavos inteiros (`valorCentavos: Long`, `bigint` no banco). Identificadores são `UUID`. Datas e horas em `Instant` (UTC, `timestamptz`).

## Módulos e entidades

| Módulo | Entidades que ele é dono (só ele escreve) |
| --- | --- |
| identidade | Cliente, Dispositivo, Credencial, SessaoRenovacao, Consentimento |
| contas | Conta, Carteira, Lancamento |
| pagamentos | Transacao (e subtipos PixEnvio, PixRecebimento, PagamentoBoleto, MovimentoMeta), ChavePix, Meta |
| familia | VinculoResponsavel, PedidoAprovacao, ContatoConfianca |
| antifraude | AnaliseRisco |
| atendimento | Chamado, MensagemChamado |
| backoffice | Funcionario, RegistroAuditoria |
| notificacao | Notificacao, OutboxEvento, LembreteConta |

## Entidades

### Cliente (identidade)
| Atributo | Tipo | Regra |
| --- | --- | --- |
| id | UUID | |
| nomeCompleto | String | |
| cpf | Cpf | Único. Cifrado em repouso, com hash para busca. PII |
| dataNascimento | LocalDate | Cifrado. PII |
| celular | String | PII |
| email | String | Opcional. PII |
| tipo | TipoCliente | TITULAR ou MENOR |
| status | StatusCliente | EM_ANALISE, ATIVO, BLOQUEADO, ENCERRADO |
| criadoEm | Instant | |

### Dispositivo (identidade)
| Atributo | Tipo | Regra |
| --- | --- | --- |
| id | UUID | |
| clienteId | UUID | Só 1 ativo por cliente (RF005) |
| modelo | String | |
| chavePublica | String | Chave gerada no Keystore/Keychain (ADR-010) |
| ativo | Boolean | |
| vinculadoEm | Instant | |

### Credencial (identidade)
`clienteId: UUID` (1 para 1 com Cliente), `hashSenha: String` (Argon2id), `tentativasErradas: Integer`, `bloqueadaAte: Instant` (opcional).

### SessaoRenovacao (identidade)
`id: UUID`, `dispositivoId: UUID`, `hashToken: String`, `expiraEm: Instant`, `revogadaEm: Instant` (opcional).

### Consentimento (identidade)
`id: UUID`, `clienteId: UUID`, `tipo: TipoConsentimento` (TERMOS_DE_USO, PRIVACIDADE, BIOMETRIA, RESPONSAVEL_LEGAL), `versaoTermo: String`, `aceitoEm: Instant`, `aceitoPorClienteId: UUID` (o próprio ou o responsável).

### Conta (contas)
| Atributo | Tipo | Regra |
| --- | --- | --- |
| id | UUID | |
| clienteId | UUID | 1 conta por cliente |
| agencia | String | Dado do parceiro |
| numero | String | Único |
| idContaParceiro | String | Identificador no parceiro BaaS |
| status | StatusConta | ATIVA, BLOQUEADA_TOTAL, ENCERRADA |
| bloqueadaEm | Instant | Opcional. Preenchido pelo "bloquear tudo agora" (RF020) |
| criadaEm | Instant | |

### Carteira (contas)
`id: UUID`, `contaId: UUID` (vazio nas carteiras técnicas), `tipo: TipoCarteira` (PRINCIPAL, META, LIQUIDACAO_PIX, LIQUIDACAO_BOLETO). Toda conta tem 1 carteira PRINCIPAL e 1 carteira META por meta. As carteiras de liquidação são do sistema e representam o dinheiro em trânsito com o parceiro.

### Lancamento (contas)
`id: UUID`, `transacaoId: UUID`, `carteiraId: UUID`, `valorCentavos: Long` (positivo = crédito, negativo = débito, nunca zero), `criadoEm: Instant`. **A soma dos lançamentos de uma transação é sempre zero** (ADR-007). Saldo da carteira = soma dos seus lançamentos.

### Transacao (pagamentos), classe abstrata
| Atributo | Tipo | Regra |
| --- | --- | --- |
| id | UUID | |
| contaId | UUID | |
| tipo | TipoTransacao | PIX_ENVIO, PIX_RECEBIMENTO, BOLETO, META_GUARDAR, META_RESGATAR |
| valorCentavos | Long | Maior que zero |
| status | StatusTransacao | PENDENTE, RETIDA, ENVIADA, CONCLUIDA, RECUSADA, ESTORNADA |
| chaveIdempotencia | String | Única por conta (RNF11) |
| idParceiro | String | Opcional. Identificador fim a fim no parceiro |
| criadaEm | Instant | |
| concluidaEm | Instant | Opcional |

Subtipos (herança, porque um Pix **é uma** transação e compartilha o ciclo de vida e os lançamentos):
- **PixEnvio**: `chaveDestino: String`, `nomeRecebedor: String`, `documentoRecebedorMascarado: String`, `bancoRecebedor: String`, `destinatarioNovo: Boolean`.
- **PixRecebimento**: `nomePagador: String`, `bancoPagador: String`.
- **PagamentoBoleto**: `linhaDigitavel: String`, `beneficiario: String`, `vencimento: LocalDate`, `jurosCentavos: Long`.
- **MovimentoMeta**: `metaId: UUID`.

### ChavePix (pagamentos)
`id: UUID`, `contaId: UUID`, `tipo: TipoChavePix` (CPF, CELULAR, ALEATORIA), `valor: String` (único), `status: StatusChavePix` (ATIVA, EXCLUIDA), `criadaEm: Instant`.

### Meta (pagamentos)
`id: UUID`, `contaId: UUID`, `carteiraId: UUID` (a carteira META, criada junto, composição), `nome: String`, `valorAlvoCentavos: Long`, `dataAlvo: LocalDate`, `imagemUrl: String`, `status: StatusMeta` (ATIVA, CONCLUIDA, CANCELADA).

### VinculoResponsavel (familia)
`id: UUID`, `menorClienteId: UUID` (único), `responsavelClienteId: UUID`, `status: StatusVinculo` (CONVIDADO, ATIVO, ENCERRADO), `limiteDiarioCentavos: Long`, `limiteMensalCentavos: Long`, `convidadoEm: Instant`, `aceitoEm: Instant`, `expiraEm: Instant` (convite vale 7 dias, US09).

### PedidoAprovacao (familia)
`id: UUID`, `vinculoId: UUID`, `transacaoId: UUID`, `status: StatusPedido` (PENDENTE, APROVADO, RECUSADO, EXPIRADO), `criadoEm: Instant`, `expiraEm: Instant` (24 horas, US18), `decididoEm: Instant`.

### ContatoConfianca (familia)
`id: UUID`, `clienteId: UUID`, `nome: String` (PII), `celular: String` (PII), `status: StatusContato` (CONVIDADO, ATIVO, REMOVIDO), `aceitoEm: Instant`.

### AnaliseRisco (antifraude)
`id: UUID`, `transacaoId: UUID` (1 para 1), `nota: Integer` (0 a 100), `motivos: List<String>`, `resultado: ResultadoAnalise` (LIBERADA_AUTOMATICA, RETIDA, LIBERADA_ANALISTA, RECUSADA_ANALISTA), `analistaId: UUID` (opcional), `decididaEm: Instant`. Pix com nota **igual ou acima de 70** fica RETIDA (RF026).

### Chamado (atendimento)
`id: UUID`, `clienteId: UUID`, `atendenteId: UUID` (opcional), `assunto: String`, `status: StatusChamado` (ABERTO, EM_ATENDIMENTO, RESOLVIDO), `abertoEm: Instant`, `fechadoEm: Instant`.

### MensagemChamado (atendimento)
`id: UUID`, `chamadoId: UUID`, `autor: AutorMensagem` (CLIENTE, ATENDENTE), `texto: String`, `audioUrl: String` (opcional), `enviadaEm: Instant`. Composição: a mensagem não existe sem o chamado.

### Funcionario (backoffice)
`id: UUID`, `nome: String`, `email: String` (único), `papel: Papel` (ATENDENTE, ANALISTA_ANTIFRAUDE, ADMINISTRADOR), `hashSenha: String`, `segredoTotp: String` (cifrado), `ativo: Boolean`.

### RegistroAuditoria (backoffice)
`id: Long`, `funcionarioId: UUID`, `acao: String`, `entidade: String`, `entidadeId: String`, `ip: String`, `ocorridoEm: Instant`. Só inserção, nunca alteração. Guardado 5 anos (RNF14).

### Notificacao (notificacao)
`id: UUID`, `clienteId: UUID`, `canal: Canal` (PUSH, SMS), `tipo: String`, `conteudo: String`, `status: StatusNotificacao` (PENDENTE, ENVIADA, FALHOU), `criadaEm: Instant`, `enviadaEm: Instant`.

### OutboxEvento (notificacao, usado por todos)
`id: Long`, `tipo: String` (ex.: `PixConcluido`), `agregadoId: UUID`, `payload: Json`, `criadoEm: Instant`, `processadoEm: Instant` (opcional), `tentativas: Integer`, `proximaTentativaEm: Instant`.

### LembreteConta (notificacao)
`id: UUID`, `clienteId: UUID`, `descricao: String`, `diaVencimento: Integer` (1 a 31), `ativo: Boolean`.

## Relações

| De | Para | Cardinalidade | Tipo | Por quê |
| --- | --- | --- | --- | --- |
| Cliente | Conta | 1 para 1 | Associação | Uma conta por cliente no MVP |
| Cliente | Dispositivo | 1 para N (1 ativo) | Composição | Dispositivo não existe sem o cliente |
| Cliente | Credencial | 1 para 1 | Composição | |
| Cliente | Consentimento | 1 para N | Composição | |
| Conta | Carteira | 1 para N | Composição | Carteira não existe sem a conta |
| Carteira | Lancamento | 1 para N | Associação | |
| Transacao | Lancamento | 1 para N (no mínimo 2) | Composição | Lançamentos nascem e morrem com a transação |
| Conta | Transacao | 1 para N | Associação | |
| Transacao | PixEnvio, PixRecebimento, PagamentoBoleto, MovimentoMeta | Generalização | Herança | Mesmo ciclo de vida (State) e mesmos lançamentos |
| Conta | ChavePix | 1 para N | Agregação | A chave pode ser excluída sem afetar a conta |
| Conta | Meta | 1 para N | Associação | |
| Meta | Carteira | 1 para 1 | Composição | A carteira da meta nasce com a meta |
| Cliente (menor) | VinculoResponsavel | 1 para 1 | Associação | Um responsável vinculado por menor no MVP |
| Cliente (responsável) | VinculoResponsavel | 1 para N | Associação | Um pai pode ter mais de um filho |
| VinculoResponsavel | PedidoAprovacao | 1 para N | Composição | |
| Cliente | ContatoConfianca | 1 para N | Composição | |
| Transacao | AnaliseRisco | 1 para 0..1 | Associação | Só Pix enviado é analisado |
| Funcionario | AnaliseRisco | 1 para N | Associação | Quem decidiu |
| Cliente | Chamado | 1 para N | Associação | |
| Chamado | MensagemChamado | 1 para N | Composição | |
| Funcionario | RegistroAuditoria | 1 para N | Associação | |

## Como o modelo vira tabela (diferenças de propósito)

O diagrama de classes mostra o domínio; o banco (Bloco 5) guarda alguns campos de forma diferente por segurança e integridade:

| No domínio | No banco | Por quê |
| --- | --- | --- |
| `Cliente.cpf: Cpf` | `cpf_cifrado` + `cpf_hash` | CPF cifrado em repouso (RNF07). O hash permite buscar e garantir unicidade sem decifrar |
| `Cliente.dataNascimento: LocalDate` | `data_nascimento_cifrada` | Cifrado em repouso (RNF07) |
| `Funcionario.segredoTotp: String` | `segredo_totp_cifrado` | Segredo do segundo fator nunca em texto puro |
| Saldo da carteira (soma dos lançamentos) | Tabela extra `saldo_fechamento_diario` | Desnormalização de propósito: a consulta de saldo soma só os lançamentos do dia sobre o fechamento anterior e cabe no p95 de 300 ms (ADR-007, RNF01) |
| Subtipos de `Transacao` (herança) | Uma tabela por subtipo, com chave estrangeira composta (`transacao_id`, `tipo`) | Impede, por exemplo, um registro de Pix apontando para uma transação de boleto |

## Objeto de entrada do Pix

**PedidoPix** (objeto de valor, sem tabela): `chaveDestino: String`, `valorCentavos: Long`, `descricao: String` (opcional, até 140 caracteres), `assinaturaDispositivo: String` (o pedido assinado com a chave do aparelho, destravada pela biometria, ADR-010). É o corpo de `POST /v1/pix/envios`; vira `PixEnvio` depois de validado.

## Classes de serviço (para o diagrama de classes e o C4 nível 4)

| Classe | Métodos principais |
| --- | --- |
| ServicoEnvioPix | `+iniciar(contaId: UUID, pedido: PedidoPix, chaveIdempotencia: String): Transacao`, `+confirmarRetorno(idParceiro: String, aceito: Boolean): void`, `-reservarSaldo(t: Transacao): void`, `-compensar(t: Transacao): void` |
| MotorAntifraude | `+avaliar(t: PixEnvio): AnaliseRisco` (soma as notas das `RegraRisco`) |
| RegraRisco (interface) | `+pontuar(t: PixEnvio, h: HistoricoCliente): Integer` |
| PortaBancaria (interface) | `+consultarChave(chave: String): DadosRecebedor`, `+enviarPix(t: PixEnvio): RespostaParceiro`, `+pagarBoleto(b: PagamentoBoleto): RespostaParceiro` |
| PortaVoz (interface) | `+falar(texto: String): UrlAudio` |
| UnidadeDeTrabalho | `+executar<T>(trabalho: Funcao<T>): T` |
