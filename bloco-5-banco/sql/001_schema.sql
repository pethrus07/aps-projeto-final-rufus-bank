-- Rufus Bank · Modelo físico (PostgreSQL 17)
-- Fonte única dos nomes: bloco-3-arquitetura/05-modelo-de-dominio.md
-- Convenções:
--   dinheiro em centavos inteiros (bigint), nunca float
--   datas e horas em timestamptz (UTC)
--   identificadores uuid gerados por gen_random_uuid()
--   marcação LGPD no começo de cada COMMENT ON COLUMN:
--     [PII]           dado pessoal (LGPD art. 5º, I)
--     [PII-SENSIVEL]  dado pessoal sensível (LGPD art. 5º, II), ex.: biometria
--     [CIFRADO]       guardado cifrado pela aplicação (AES-256-GCM com chave do KMS)
--     [SEGREDO]       credencial; nunca sai do banco nem vai para log
-- Execução: psql -v ON_ERROR_STOP=1 -f 001_schema.sql

BEGIN;

CREATE SCHEMA IF NOT EXISTS rufus;
SET search_path TO rufus;

-- =====================================================================
-- Módulo identidade
-- =====================================================================

CREATE TABLE cliente (
    id                       uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo            text        NOT NULL CHECK (length(trim(nome_completo)) >= 3),
    cpf_cifrado              bytea       NOT NULL,
    cpf_hash                 char(64)    NOT NULL UNIQUE CHECK (cpf_hash ~ '^[0-9a-f]{64}$'),
    data_nascimento_cifrada  bytea       NOT NULL,
    celular                  text        NOT NULL CHECK (celular ~ '^\+55[0-9]{10,11}$'),
    email                    text        CHECK (email IS NULL OR email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
    tipo                     text        NOT NULL CHECK (tipo IN ('TITULAR', 'MENOR')),
    status                   text        NOT NULL DEFAULT 'EM_ANALISE'
                                         CHECK (status IN ('EM_ANALISE', 'ATIVO', 'BLOQUEADO', 'ENCERRADO')),
    criado_em                timestamptz NOT NULL DEFAULT now()
);
COMMENT ON TABLE cliente IS 'Pessoa física com conta no Rufus: titular adulto ou menor de 16 e 17 anos.';
COMMENT ON COLUMN cliente.id IS 'Identificador interno do cliente.';
COMMENT ON COLUMN cliente.nome_completo IS '[PII] Nome civil completo, como no documento.';
COMMENT ON COLUMN cliente.cpf_cifrado IS '[PII][CIFRADO] CPF cifrado pela aplicação. Só é decifrado para envio ao parceiro BaaS.';
COMMENT ON COLUMN cliente.cpf_hash IS '[PII] HMAC-SHA256 do CPF com chave secreta, em hexadecimal. Permite buscar e garantir CPF único sem decifrar.';
COMMENT ON COLUMN cliente.data_nascimento_cifrada IS '[PII][CIFRADO] Data de nascimento cifrada. Usada para checar a idade do menor.';
COMMENT ON COLUMN cliente.celular IS '[PII] Celular no formato +55DDNNNNNNNNN. Recebe SMS e convites.';
COMMENT ON COLUMN cliente.email IS '[PII] E-mail opcional.';
COMMENT ON COLUMN cliente.tipo IS 'TITULAR (adulto) ou MENOR (16 e 17 anos, exige vínculo com responsável).';
COMMENT ON COLUMN cliente.status IS 'Situação do cadastro: EM_ANALISE, ATIVO, BLOQUEADO ou ENCERRADO.';
COMMENT ON COLUMN cliente.criado_em IS 'Momento do início do cadastro.';

CREATE TABLE dispositivo (
    id             uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id     uuid        NOT NULL REFERENCES cliente (id) ON DELETE CASCADE,
    modelo         text        NOT NULL,
    chave_publica  text        NOT NULL UNIQUE,
    ativo          boolean     NOT NULL DEFAULT true,
    vinculado_em   timestamptz NOT NULL DEFAULT now()
);
-- RF005: no máximo 1 celular ativo por cliente
CREATE UNIQUE INDEX ux_dispositivo_um_ativo_por_cliente ON dispositivo (cliente_id) WHERE ativo;
COMMENT ON TABLE dispositivo IS 'Celular vinculado à conta. Só um ativo por cliente (RF005).';
COMMENT ON COLUMN dispositivo.id IS 'Identificador do vínculo do aparelho.';
COMMENT ON COLUMN dispositivo.cliente_id IS 'Cliente dono do aparelho.';
COMMENT ON COLUMN dispositivo.modelo IS 'Modelo informado pelo aparelho, para o cliente reconhecer na lista.';
COMMENT ON COLUMN dispositivo.chave_publica IS 'Chave pública do par gerado no Keystore ou Keychain. Confere a assinatura do login (ADR-010).';
COMMENT ON COLUMN dispositivo.ativo IS 'Verdadeiro para o aparelho em uso. A troca desativa o anterior.';
COMMENT ON COLUMN dispositivo.vinculado_em IS 'Momento do vínculo.';

CREATE TABLE credencial (
    cliente_id          uuid        PRIMARY KEY REFERENCES cliente (id) ON DELETE CASCADE,
    hash_senha          text        NOT NULL CHECK (hash_senha LIKE '$argon2id$%'),
    tentativas_erradas  integer     NOT NULL DEFAULT 0 CHECK (tentativas_erradas BETWEEN 0 AND 5),
    bloqueada_ate       timestamptz
);
COMMENT ON TABLE credencial IS 'Senha de 6 números do cliente e controle de tentativas (RF003, RF004).';
COMMENT ON COLUMN credencial.cliente_id IS 'Cliente dono da senha.';
COMMENT ON COLUMN credencial.hash_senha IS '[SEGREDO] Hash Argon2id da senha (RNF05). A senha nunca é guardada.';
COMMENT ON COLUMN credencial.tentativas_erradas IS 'Senhas erradas seguidas. Na 5ª o acesso é bloqueado por 30 minutos.';
COMMENT ON COLUMN credencial.bloqueada_ate IS 'Fim do bloqueio por tentativas, quando houver.';

CREATE TABLE sessao_renovacao (
    id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    dispositivo_id  uuid        NOT NULL REFERENCES dispositivo (id) ON DELETE CASCADE,
    hash_token      char(64)    NOT NULL UNIQUE,
    expira_em       timestamptz NOT NULL,
    revogada_em     timestamptz,
    CHECK (revogada_em IS NULL OR revogada_em <= expira_em + interval '30 days')
);
CREATE INDEX ix_sessao_dispositivo_validas ON sessao_renovacao (dispositivo_id) WHERE revogada_em IS NULL;
COMMENT ON TABLE sessao_renovacao IS 'Token de renovação de 30 dias, trocado a cada uso (RNF05).';
COMMENT ON COLUMN sessao_renovacao.id IS 'Identificador da sessão.';
COMMENT ON COLUMN sessao_renovacao.dispositivo_id IS 'Aparelho que recebeu o token.';
COMMENT ON COLUMN sessao_renovacao.hash_token IS '[SEGREDO] SHA-256 do token de renovação. O token em si só existe no celular.';
COMMENT ON COLUMN sessao_renovacao.expira_em IS 'Fim da validade (30 dias após a emissão).';
COMMENT ON COLUMN sessao_renovacao.revogada_em IS 'Momento em que o token foi trocado, usado no logout ou revogado na troca de aparelho.';

CREATE TABLE consentimento (
    id                     uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id             uuid        NOT NULL REFERENCES cliente (id) ON DELETE CASCADE,
    tipo                   text        NOT NULL CHECK (tipo IN ('TERMOS_DE_USO', 'PRIVACIDADE', 'BIOMETRIA', 'RESPONSAVEL_LEGAL')),
    versao_termo           text        NOT NULL,
    aceito_em              timestamptz NOT NULL DEFAULT now(),
    aceito_por_cliente_id  uuid        NOT NULL REFERENCES cliente (id),
    UNIQUE (cliente_id, tipo, versao_termo)
);
COMMENT ON TABLE consentimento IS 'Registro de cada aceite de termo, com versão e quem aceitou (LGPD art. 8º e 14, risco R08).';
COMMENT ON COLUMN consentimento.id IS 'Identificador do aceite.';
COMMENT ON COLUMN consentimento.cliente_id IS 'Titular a quem o consentimento se refere.';
COMMENT ON COLUMN consentimento.tipo IS 'Termo aceito: TERMOS_DE_USO, PRIVACIDADE, BIOMETRIA ou RESPONSAVEL_LEGAL.';
COMMENT ON COLUMN consentimento.versao_termo IS 'Versão do texto aceito. Termo novo exige novo aceite.';
COMMENT ON COLUMN consentimento.aceito_em IS 'Momento do aceite.';
COMMENT ON COLUMN consentimento.aceito_por_cliente_id IS 'Quem aceitou: o próprio titular ou, no caso do menor, o responsável.';

-- =====================================================================
-- Módulo backoffice (vem antes porque antifraude e atendimento apontam para ele)
-- =====================================================================

CREATE TABLE funcionario (
    id                     uuid    PRIMARY KEY DEFAULT gen_random_uuid(),
    nome                   text    NOT NULL,
    email                  text    NOT NULL CHECK (email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
    papel                  text    NOT NULL CHECK (papel IN ('ATENDENTE', 'ANALISTA_ANTIFRAUDE', 'ADMINISTRADOR')),
    hash_senha             text    NOT NULL CHECK (hash_senha LIKE '$argon2id$%'),
    segredo_totp_cifrado   bytea,
    ativo                  boolean NOT NULL DEFAULT true
);
CREATE UNIQUE INDEX ux_funcionario_email ON funcionario (lower(email));
COMMENT ON TABLE funcionario IS 'Usuário interno dos painéis de SAC, antifraude e administração (RF030).';
COMMENT ON COLUMN funcionario.id IS 'Identificador do funcionário.';
COMMENT ON COLUMN funcionario.nome IS '[PII] Nome do funcionário.';
COMMENT ON COLUMN funcionario.email IS '[PII] E-mail corporativo, usado no login. Único sem diferenciar maiúsculas.';
COMMENT ON COLUMN funcionario.papel IS 'Papel de acesso (RBAC): ATENDENTE, ANALISTA_ANTIFRAUDE ou ADMINISTRADOR.';
COMMENT ON COLUMN funcionario.hash_senha IS '[SEGREDO] Hash Argon2id da senha.';
COMMENT ON COLUMN funcionario.segredo_totp_cifrado IS '[SEGREDO][CIFRADO] Segredo do segundo fator TOTP. Vazio até o primeiro login (US22).';
COMMENT ON COLUMN funcionario.ativo IS 'Falso para funcionário desligado. Nunca se apaga, por causa da auditoria.';

CREATE TABLE registro_auditoria (
    id              bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    funcionario_id  uuid        NOT NULL REFERENCES funcionario (id),
    acao            text        NOT NULL,
    entidade        text        NOT NULL,
    entidade_id     text        NOT NULL,
    ip              inet        NOT NULL,
    ocorrido_em     timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX ix_auditoria_entidade ON registro_auditoria (entidade, entidade_id, ocorrido_em DESC);
CREATE INDEX ix_auditoria_funcionario ON registro_auditoria (funcionario_id, ocorrido_em DESC);
COMMENT ON TABLE registro_auditoria IS 'Toda consulta e alteração feita por funcionário. Só inserção. Guardado 5 anos (RNF14, Lei 9.613/1998).';
COMMENT ON COLUMN registro_auditoria.id IS 'Número sequencial do registro.';
COMMENT ON COLUMN registro_auditoria.funcionario_id IS 'Quem fez a ação.';
COMMENT ON COLUMN registro_auditoria.acao IS 'O que foi feito, por exemplo CONSULTAR_HISTORICO ou DECIDIR_ANALISE.';
COMMENT ON COLUMN registro_auditoria.entidade IS 'Tabela afetada, por exemplo cliente ou analise_risco.';
COMMENT ON COLUMN registro_auditoria.entidade_id IS 'Identificador da linha afetada.';
COMMENT ON COLUMN registro_auditoria.ip IS '[PII] Endereço IP de onde veio a ação.';
COMMENT ON COLUMN registro_auditoria.ocorrido_em IS 'Momento da ação.';

CREATE FUNCTION recusar_alteracao() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'tabela % só aceita inserção', TG_TABLE_NAME USING ERRCODE = 'P0001';
END $$;

CREATE TRIGGER tg_auditoria_imutavel BEFORE UPDATE OR DELETE ON registro_auditoria
    FOR EACH ROW EXECUTE FUNCTION recusar_alteracao();

-- =====================================================================
-- Módulo contas
-- =====================================================================

CREATE TABLE conta (
    id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id         uuid        NOT NULL UNIQUE REFERENCES cliente (id),
    agencia            text        NOT NULL CHECK (agencia ~ '^[0-9]{4}$'),
    numero             text        NOT NULL UNIQUE CHECK (numero ~ '^[0-9]{5,12}-[0-9X]$'),
    id_conta_parceiro  text        NOT NULL UNIQUE,
    status             text        NOT NULL DEFAULT 'ATIVA' CHECK (status IN ('ATIVA', 'BLOQUEADA_TOTAL', 'ENCERRADA')),
    bloqueada_em       timestamptz,
    criada_em          timestamptz NOT NULL DEFAULT now(),
    CHECK ((status = 'BLOQUEADA_TOTAL') = (bloqueada_em IS NOT NULL))
);
COMMENT ON TABLE conta IS 'Conta de pagamento do cliente, mantida no parceiro BaaS. Uma por cliente no MVP.';
COMMENT ON COLUMN conta.id IS 'Identificador interno da conta.';
COMMENT ON COLUMN conta.cliente_id IS 'Cliente dono da conta. Único: uma conta por cliente.';
COMMENT ON COLUMN conta.agencia IS 'Agência no parceiro (4 dígitos).';
COMMENT ON COLUMN conta.numero IS '[PII] Número da conta com dígito, por exemplo 123456-7.';
COMMENT ON COLUMN conta.id_conta_parceiro IS 'Identificador da conta no parceiro BaaS, usado na conciliação.';
COMMENT ON COLUMN conta.status IS 'ATIVA, BLOQUEADA_TOTAL (botão bloquear tudo, RF020) ou ENCERRADA.';
COMMENT ON COLUMN conta.bloqueada_em IS 'Momento do bloqueio total. Preenchido se e somente se o status é BLOQUEADA_TOTAL.';
COMMENT ON COLUMN conta.criada_em IS 'Momento da abertura.';

CREATE TABLE carteira (
    id        uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    conta_id  uuid REFERENCES conta (id),
    tipo      text NOT NULL CHECK (tipo IN ('PRINCIPAL', 'META', 'LIQUIDACAO_PIX', 'LIQUIDACAO_BOLETO')),
    -- carteira técnica (liquidação) não tem conta; carteira de cliente sempre tem
    CHECK ((tipo LIKE 'LIQUIDACAO_%') = (conta_id IS NULL))
);
CREATE UNIQUE INDEX ux_carteira_principal_por_conta ON carteira (conta_id) WHERE tipo = 'PRINCIPAL';
CREATE UNIQUE INDEX ux_carteira_tecnica_unica ON carteira (tipo) WHERE conta_id IS NULL;
CREATE INDEX ix_carteira_conta ON carteira (conta_id);
COMMENT ON TABLE carteira IS 'Divisão contábil do dinheiro: principal, meta ou carteira técnica de liquidação com o parceiro (ADR-007).';
COMMENT ON COLUMN carteira.id IS 'Identificador da carteira.';
COMMENT ON COLUMN carteira.conta_id IS 'Conta dona. Vazio nas carteiras técnicas de liquidação.';
COMMENT ON COLUMN carteira.tipo IS 'PRINCIPAL (1 por conta), META (1 por meta), LIQUIDACAO_PIX ou LIQUIDACAO_BOLETO (do sistema).';

CREATE TABLE transacao (
    id                  uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    conta_id            uuid        NOT NULL REFERENCES conta (id),
    tipo                text        NOT NULL CHECK (tipo IN ('PIX_ENVIO', 'PIX_RECEBIMENTO', 'BOLETO', 'META_GUARDAR', 'META_RESGATAR')),
    valor_centavos      bigint      NOT NULL CHECK (valor_centavos > 0),
    status              text        NOT NULL DEFAULT 'PENDENTE'
                                    CHECK (status IN ('PENDENTE', 'RETIDA', 'ENVIADA', 'CONCLUIDA', 'RECUSADA', 'ESTORNADA')),
    chave_idempotencia  text        NOT NULL CHECK (length(chave_idempotencia) BETWEEN 8 AND 128),
    id_parceiro         text        UNIQUE,
    criada_em           timestamptz NOT NULL DEFAULT now(),
    concluida_em        timestamptz,
    -- RNF11: o mesmo pedido repetido não cria um segundo Pix
    CONSTRAINT ux_transacao_idempotencia UNIQUE (conta_id, chave_idempotencia),
    -- alvo das chaves estrangeiras dos subtipos, que garantem o tipo certo
    CONSTRAINT ux_transacao_id_tipo UNIQUE (id, tipo),
    CHECK (concluida_em IS NULL OR status IN ('CONCLUIDA', 'RECUSADA', 'ESTORNADA'))
);
-- extrato do cliente (RNF01): mais recentes primeiro, paginado por cursor
CREATE INDEX ix_transacao_extrato ON transacao (conta_id, criada_em DESC, id DESC);
-- fila do antifraude e reprocessamento: só as que estão paradas
CREATE INDEX ix_transacao_pendentes ON transacao (status, criada_em) WHERE status IN ('PENDENTE', 'RETIDA', 'ENVIADA');
COMMENT ON TABLE transacao IS 'Toda movimentação de dinheiro. Classe base dos subtipos pix_envio, pix_recebimento, pagamento_boleto e movimento_meta.';
COMMENT ON COLUMN transacao.id IS 'Identificador da transação.';
COMMENT ON COLUMN transacao.conta_id IS 'Conta do cliente que fez ou recebeu a transação.';
COMMENT ON COLUMN transacao.tipo IS 'PIX_ENVIO, PIX_RECEBIMENTO, BOLETO, META_GUARDAR ou META_RESGATAR. Define qual subtipo existe.';
COMMENT ON COLUMN transacao.valor_centavos IS 'Valor em centavos, sempre maior que zero. O sentido do dinheiro está nos lançamentos.';
COMMENT ON COLUMN transacao.status IS 'Estado (padrão State): PENDENTE, RETIDA, ENVIADA, CONCLUIDA, RECUSADA ou ESTORNADA.';
COMMENT ON COLUMN transacao.chave_idempotencia IS 'Valor do cabeçalho Idempotency-Key. Único por conta (RNF11).';
COMMENT ON COLUMN transacao.id_parceiro IS 'Identificador fim a fim no parceiro BaaS. Preenchido quando o parceiro aceita.';
COMMENT ON COLUMN transacao.criada_em IS 'Momento do pedido.';
COMMENT ON COLUMN transacao.concluida_em IS 'Momento do estado final (concluída, recusada ou estornada).';

CREATE TABLE lancamento (
    id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    transacao_id    uuid        NOT NULL REFERENCES transacao (id),
    carteira_id     uuid        NOT NULL REFERENCES carteira (id),
    valor_centavos  bigint      NOT NULL CHECK (valor_centavos <> 0),
    criado_em       timestamptz NOT NULL DEFAULT now()
);
-- saldo e extrato por carteira (RNF01)
CREATE INDEX ix_lancamento_carteira ON lancamento (carteira_id, criado_em);
-- conferência do equilíbrio por transação (gatilho abaixo)
CREATE INDEX ix_lancamento_transacao ON lancamento (transacao_id);
COMMENT ON TABLE lancamento IS 'Razão contábil em partidas dobradas: a soma dos lançamentos de uma transação é zero (ADR-007). Só inserção.';
COMMENT ON COLUMN lancamento.id IS 'Identificador do lançamento.';
COMMENT ON COLUMN lancamento.transacao_id IS 'Transação que originou o lançamento.';
COMMENT ON COLUMN lancamento.carteira_id IS 'Carteira afetada.';
COMMENT ON COLUMN lancamento.valor_centavos IS 'Positivo é crédito, negativo é débito. Nunca zero.';
COMMENT ON COLUMN lancamento.criado_em IS 'Momento do lançamento.';

-- ADR-007: recusa transação desequilibrada. É DEFERRABLE INITIALLY DEFERRED para
-- a aplicação inserir o débito e o crédito na mesma transação do banco; a conferência
-- acontece no COMMIT.
CREATE FUNCTION conferir_partidas_dobradas() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE
    soma   bigint;
    linhas integer;
BEGIN
    SELECT coalesce(sum(valor_centavos), 0), count(*) INTO soma, linhas
      FROM lancamento WHERE transacao_id = NEW.transacao_id;
    IF soma <> 0 OR linhas < 2 THEN
        RAISE EXCEPTION 'transação % desequilibrada: soma % em % lançamento(s)', NEW.transacao_id, soma, linhas
            USING ERRCODE = '23514';
    END IF;
    RETURN NULL;
END $$;

CREATE CONSTRAINT TRIGGER tg_lancamento_partidas_dobradas
    AFTER INSERT ON lancamento DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION conferir_partidas_dobradas();

CREATE TRIGGER tg_lancamento_imutavel BEFORE UPDATE OR DELETE ON lancamento
    FOR EACH ROW EXECUTE FUNCTION recusar_alteracao();

-- Desnormalização proposital (ver 01-decisao.md): saldo de cada carteira no fim do dia.
-- O saldo atual = saldo do último fechamento + lançamentos depois dele. Mantém o RNF01
-- quando a carteira tiver anos de lançamentos.
CREATE TABLE saldo_fechamento_diario (
    carteira_id     uuid    NOT NULL REFERENCES carteira (id),
    data            date    NOT NULL,
    saldo_centavos  bigint  NOT NULL,
    PRIMARY KEY (carteira_id, data)
);
COMMENT ON TABLE saldo_fechamento_diario IS 'Saldo de fechamento por carteira e dia, calculado pelo worker. Desnormalização para o RNF01.';
COMMENT ON COLUMN saldo_fechamento_diario.carteira_id IS 'Carteira fechada.';
COMMENT ON COLUMN saldo_fechamento_diario.data IS 'Dia do fechamento (horário de Brasília).';
COMMENT ON COLUMN saldo_fechamento_diario.saldo_centavos IS 'Soma de todos os lançamentos da carteira até o fim do dia. Pode ser negativo só em carteira técnica.';

-- =====================================================================
-- Módulo pagamentos
-- =====================================================================

CREATE TABLE pix_envio (
    transacao_id                   uuid    PRIMARY KEY,
    tipo                           text    NOT NULL DEFAULT 'PIX_ENVIO' CHECK (tipo = 'PIX_ENVIO'),
    chave_destino                  text    NOT NULL,
    nome_recebedor                 text    NOT NULL,
    documento_recebedor_mascarado  text    NOT NULL CHECK (documento_recebedor_mascarado ~ '^[*0-9./-]+$'),
    banco_recebedor                text    NOT NULL,
    destinatario_novo              boolean NOT NULL,
    FOREIGN KEY (transacao_id, tipo) REFERENCES transacao (id, tipo)
);
COMMENT ON TABLE pix_envio IS 'Subtipo de transação: Pix enviado. A chave (transacao_id, tipo) garante que a transação base é PIX_ENVIO.';
COMMENT ON COLUMN pix_envio.transacao_id IS 'Transação base.';
COMMENT ON COLUMN pix_envio.tipo IS 'Sempre PIX_ENVIO. Existe para a chave estrangeira composta.';
COMMENT ON COLUMN pix_envio.chave_destino IS '[PII] Chave Pix de quem recebe.';
COMMENT ON COLUMN pix_envio.nome_recebedor IS '[PII] Nome do recebedor devolvido pelo parceiro, falado antes da confirmação (RF009).';
COMMENT ON COLUMN pix_envio.documento_recebedor_mascarado IS '[PII] CPF ou CNPJ do recebedor com dígitos ocultos, por exemplo ***.456.789-**.';
COMMENT ON COLUMN pix_envio.banco_recebedor IS 'Nome da instituição do recebedor.';
COMMENT ON COLUMN pix_envio.destinatario_novo IS 'Verdadeiro se a conta nunca enviou Pix para essa chave. Aciona limite menor (RF019).';

CREATE TABLE pix_recebimento (
    transacao_id   uuid PRIMARY KEY,
    tipo           text NOT NULL DEFAULT 'PIX_RECEBIMENTO' CHECK (tipo = 'PIX_RECEBIMENTO'),
    nome_pagador   text NOT NULL,
    banco_pagador  text NOT NULL,
    FOREIGN KEY (transacao_id, tipo) REFERENCES transacao (id, tipo)
);
COMMENT ON TABLE pix_recebimento IS 'Subtipo de transação: Pix recebido, avisado pelo webhook do parceiro.';
COMMENT ON COLUMN pix_recebimento.transacao_id IS 'Transação base.';
COMMENT ON COLUMN pix_recebimento.tipo IS 'Sempre PIX_RECEBIMENTO.';
COMMENT ON COLUMN pix_recebimento.nome_pagador IS '[PII] Nome de quem pagou, falado no aviso (US05).';
COMMENT ON COLUMN pix_recebimento.banco_pagador IS 'Instituição de quem pagou.';

CREATE TABLE pagamento_boleto (
    transacao_id     uuid   PRIMARY KEY,
    tipo             text   NOT NULL DEFAULT 'BOLETO' CHECK (tipo = 'BOLETO'),
    linha_digitavel  text   NOT NULL CHECK (linha_digitavel ~ '^[0-9]{44,48}$'),
    beneficiario     text   NOT NULL,
    vencimento       date   NOT NULL,
    juros_centavos   bigint NOT NULL DEFAULT 0 CHECK (juros_centavos >= 0),
    FOREIGN KEY (transacao_id, tipo) REFERENCES transacao (id, tipo)
);
COMMENT ON TABLE pagamento_boleto IS 'Subtipo de transação: boleto ou conta de consumo paga (RF013).';
COMMENT ON COLUMN pagamento_boleto.transacao_id IS 'Transação base.';
COMMENT ON COLUMN pagamento_boleto.tipo IS 'Sempre BOLETO.';
COMMENT ON COLUMN pagamento_boleto.linha_digitavel IS 'Código lido pela câmera ou digitado, só números (44 a 48 dígitos).';
COMMENT ON COLUMN pagamento_boleto.beneficiario IS 'Empresa que recebe, falada antes da confirmação.';
COMMENT ON COLUMN pagamento_boleto.vencimento IS 'Data de vencimento do boleto.';
COMMENT ON COLUMN pagamento_boleto.juros_centavos IS 'Juros e multa por atraso, mostrados separados (US08).';

CREATE TABLE chave_pix (
    id         uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    conta_id   uuid        NOT NULL REFERENCES conta (id),
    tipo       text        NOT NULL CHECK (tipo IN ('CPF', 'CELULAR', 'ALEATORIA')),
    valor      text        NOT NULL,
    status     text        NOT NULL DEFAULT 'ATIVA' CHECK (status IN ('ATIVA', 'EXCLUIDA')),
    criada_em  timestamptz NOT NULL DEFAULT now()
);
-- uma chave ativa só pode existir uma vez; depois de excluída pode ser cadastrada de novo
CREATE UNIQUE INDEX ux_chave_pix_valor_ativa ON chave_pix (valor) WHERE status = 'ATIVA';
CREATE INDEX ix_chave_pix_conta ON chave_pix (conta_id);
COMMENT ON TABLE chave_pix IS 'Chaves Pix da conta para receber (RF011).';
COMMENT ON COLUMN chave_pix.id IS 'Identificador da chave.';
COMMENT ON COLUMN chave_pix.conta_id IS 'Conta dona da chave.';
COMMENT ON COLUMN chave_pix.tipo IS 'CPF, CELULAR ou ALEATORIA.';
COMMENT ON COLUMN chave_pix.valor IS '[PII] Valor da chave (CPF, celular ou código aleatório).';
COMMENT ON COLUMN chave_pix.status IS 'ATIVA ou EXCLUIDA.';
COMMENT ON COLUMN chave_pix.criada_em IS 'Momento do cadastro.';

CREATE TABLE meta (
    id                   uuid   PRIMARY KEY DEFAULT gen_random_uuid(),
    conta_id             uuid   NOT NULL REFERENCES conta (id),
    carteira_id          uuid   NOT NULL UNIQUE REFERENCES carteira (id),
    nome                 text   NOT NULL CHECK (length(trim(nome)) BETWEEN 1 AND 60),
    valor_alvo_centavos  bigint NOT NULL CHECK (valor_alvo_centavos > 0),
    data_alvo            date,
    imagem_url           text,
    status               text   NOT NULL DEFAULT 'ATIVA' CHECK (status IN ('ATIVA', 'CONCLUIDA', 'CANCELADA'))
);
CREATE INDEX ix_meta_conta ON meta (conta_id) WHERE status = 'ATIVA';
COMMENT ON TABLE meta IS 'Meta de economia (RF017). O dinheiro guardado fica na carteira META da própria meta.';
COMMENT ON COLUMN meta.id IS 'Identificador da meta.';
COMMENT ON COLUMN meta.conta_id IS 'Conta dona da meta.';
COMMENT ON COLUMN meta.carteira_id IS 'Carteira META criada junto com a meta (composição).';
COMMENT ON COLUMN meta.nome IS 'Nome dado pelo cliente, por exemplo Notebook.';
COMMENT ON COLUMN meta.valor_alvo_centavos IS 'Quanto o cliente quer juntar.';
COMMENT ON COLUMN meta.data_alvo IS 'Data desejada, opcional.';
COMMENT ON COLUMN meta.imagem_url IS 'Endereço da imagem da meta no S3.';
COMMENT ON COLUMN meta.status IS 'ATIVA, CONCLUIDA ou CANCELADA.';

CREATE TABLE movimento_meta (
    transacao_id  uuid PRIMARY KEY,
    tipo          text NOT NULL CHECK (tipo IN ('META_GUARDAR', 'META_RESGATAR')),
    meta_id       uuid NOT NULL REFERENCES meta (id),
    FOREIGN KEY (transacao_id, tipo) REFERENCES transacao (id, tipo)
);
CREATE INDEX ix_movimento_meta_meta ON movimento_meta (meta_id);
COMMENT ON TABLE movimento_meta IS 'Subtipo de transação: guardar ou resgatar dinheiro de uma meta.';
COMMENT ON COLUMN movimento_meta.transacao_id IS 'Transação base.';
COMMENT ON COLUMN movimento_meta.tipo IS 'META_GUARDAR ou META_RESGATAR.';
COMMENT ON COLUMN movimento_meta.meta_id IS 'Meta movimentada.';

-- =====================================================================
-- Módulo familia
-- =====================================================================

CREATE TABLE vinculo_responsavel (
    id                      uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    menor_cliente_id        uuid        NOT NULL UNIQUE REFERENCES cliente (id),
    responsavel_cliente_id  uuid        NOT NULL REFERENCES cliente (id),
    status                  text        NOT NULL DEFAULT 'CONVIDADO' CHECK (status IN ('CONVIDADO', 'ATIVO', 'ENCERRADO')),
    limite_diario_centavos  bigint      NOT NULL CHECK (limite_diario_centavos >= 0),
    limite_mensal_centavos  bigint      NOT NULL CHECK (limite_mensal_centavos >= 0),
    convidado_em            timestamptz NOT NULL DEFAULT now(),
    aceito_em               timestamptz,
    expira_em               timestamptz NOT NULL DEFAULT now() + interval '7 days',
    CHECK (menor_cliente_id <> responsavel_cliente_id),
    CHECK (limite_diario_centavos <= limite_mensal_centavos),
    CHECK ((status = 'ATIVO') <= (aceito_em IS NOT NULL))
);
CREATE INDEX ix_vinculo_responsavel ON vinculo_responsavel (responsavel_cliente_id) WHERE status = 'ATIVO';
COMMENT ON TABLE vinculo_responsavel IS 'Liga o menor ao responsável legal e guarda os limites (RF014, RF015).';
COMMENT ON COLUMN vinculo_responsavel.id IS 'Identificador do vínculo.';
COMMENT ON COLUMN vinculo_responsavel.menor_cliente_id IS 'Cliente menor. Único: um responsável vinculado por menor.';
COMMENT ON COLUMN vinculo_responsavel.responsavel_cliente_id IS 'Cliente titular que é o responsável legal.';
COMMENT ON COLUMN vinculo_responsavel.status IS 'CONVIDADO, ATIVO ou ENCERRADO.';
COMMENT ON COLUMN vinculo_responsavel.limite_diario_centavos IS 'Saída máxima por dia da conta do menor.';
COMMENT ON COLUMN vinculo_responsavel.limite_mensal_centavos IS 'Saída máxima por mês. Não pode ser menor que o diário.';
COMMENT ON COLUMN vinculo_responsavel.convidado_em IS 'Momento do convite.';
COMMENT ON COLUMN vinculo_responsavel.aceito_em IS 'Momento do aceite do responsável. Obrigatório para ATIVO.';
COMMENT ON COLUMN vinculo_responsavel.expira_em IS 'Prazo do convite: 7 dias (US09).';

CREATE TABLE pedido_aprovacao (
    id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    vinculo_id    uuid        NOT NULL REFERENCES vinculo_responsavel (id),
    transacao_id  uuid        NOT NULL UNIQUE REFERENCES transacao (id),
    status        text        NOT NULL DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'APROVADO', 'RECUSADO', 'EXPIRADO')),
    criado_em     timestamptz NOT NULL DEFAULT now(),
    expira_em     timestamptz NOT NULL DEFAULT now() + interval '24 hours',
    decidido_em   timestamptz,
    CHECK ((status = 'PENDENTE') = (decidido_em IS NULL))
);
CREATE INDEX ix_pedido_pendente ON pedido_aprovacao (vinculo_id, expira_em) WHERE status = 'PENDENTE';
COMMENT ON TABLE pedido_aprovacao IS 'Pedido do menor para uma saída acima do limite (RF016).';
COMMENT ON COLUMN pedido_aprovacao.id IS 'Identificador do pedido.';
COMMENT ON COLUMN pedido_aprovacao.vinculo_id IS 'Vínculo entre o menor e o responsável.';
COMMENT ON COLUMN pedido_aprovacao.transacao_id IS 'Transação que aguarda a decisão.';
COMMENT ON COLUMN pedido_aprovacao.status IS 'PENDENTE, APROVADO, RECUSADO ou EXPIRADO.';
COMMENT ON COLUMN pedido_aprovacao.criado_em IS 'Momento do pedido.';
COMMENT ON COLUMN pedido_aprovacao.expira_em IS 'Prazo de 24 horas para decidir (US18).';
COMMENT ON COLUMN pedido_aprovacao.decidido_em IS 'Momento da decisão ou da expiração.';

CREATE TABLE contato_confianca (
    id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id  uuid        NOT NULL REFERENCES cliente (id) ON DELETE CASCADE,
    nome        text        NOT NULL,
    celular     text        NOT NULL CHECK (celular ~ '^\+55[0-9]{10,11}$'),
    status      text        NOT NULL DEFAULT 'CONVIDADO' CHECK (status IN ('CONVIDADO', 'ATIVO', 'REMOVIDO')),
    aceito_em   timestamptz
);
CREATE INDEX ix_contato_confianca_cliente ON contato_confianca (cliente_id) WHERE status = 'ATIVO';
COMMENT ON TABLE contato_confianca IS 'Pessoa avisada em movimentação fora do padrão, sem acesso à conta (RF018).';
COMMENT ON COLUMN contato_confianca.id IS 'Identificador do contato.';
COMMENT ON COLUMN contato_confianca.cliente_id IS 'Cliente protegido.';
COMMENT ON COLUMN contato_confianca.nome IS '[PII] Nome do contato (terceiro, não cliente).';
COMMENT ON COLUMN contato_confianca.celular IS '[PII] Celular do contato, que recebe o aviso por SMS.';
COMMENT ON COLUMN contato_confianca.status IS 'CONVIDADO, ATIVO ou REMOVIDO.';
COMMENT ON COLUMN contato_confianca.aceito_em IS 'Momento do aceite do convite.';

-- =====================================================================
-- Módulo antifraude
-- =====================================================================

CREATE TABLE analise_risco (
    id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    transacao_id  uuid        NOT NULL UNIQUE REFERENCES transacao (id),
    nota          integer     NOT NULL CHECK (nota BETWEEN 0 AND 100),
    motivos       text[]      NOT NULL DEFAULT '{}',
    resultado     text        NOT NULL CHECK (resultado IN ('LIBERADA_AUTOMATICA', 'RETIDA', 'LIBERADA_ANALISTA', 'RECUSADA_ANALISTA')),
    analista_id   uuid        REFERENCES funcionario (id),
    decidida_em   timestamptz,
    -- decisão humana sempre tem analista e momento
    CHECK ((resultado IN ('LIBERADA_ANALISTA', 'RECUSADA_ANALISTA')) = (analista_id IS NOT NULL AND decidida_em IS NOT NULL)),
    -- RF026: nota de 70 para cima nunca é liberada automaticamente
    CHECK (NOT (resultado = 'LIBERADA_AUTOMATICA' AND nota >= 70))
);
-- fila do painel antifraude (RF027): retidas mais antigas primeiro
CREATE INDEX ix_analise_fila ON analise_risco (resultado, id) WHERE resultado = 'RETIDA';
COMMENT ON TABLE analise_risco IS 'Nota de risco de cada Pix enviado e decisão automática ou do analista (RF026, RF027).';
COMMENT ON COLUMN analise_risco.id IS 'Identificador da análise.';
COMMENT ON COLUMN analise_risco.transacao_id IS 'Pix analisado.';
COMMENT ON COLUMN analise_risco.nota IS 'Soma das regras de risco, de 0 a 100. A partir de 70 o Pix é retido.';
COMMENT ON COLUMN analise_risco.motivos IS 'Regras que pontuaram, por exemplo DESTINATARIO_NOVO e HORARIO_NOTURNO.';
COMMENT ON COLUMN analise_risco.resultado IS 'LIBERADA_AUTOMATICA, RETIDA, LIBERADA_ANALISTA ou RECUSADA_ANALISTA.';
COMMENT ON COLUMN analise_risco.analista_id IS 'Analista que decidiu, quando a decisão é humana.';
COMMENT ON COLUMN analise_risco.decidida_em IS 'Momento da decisão humana.';

-- =====================================================================
-- Módulo atendimento
-- =====================================================================

CREATE TABLE chamado (
    id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id    uuid        NOT NULL REFERENCES cliente (id),
    atendente_id  uuid        REFERENCES funcionario (id),
    assunto       text        NOT NULL,
    status        text        NOT NULL DEFAULT 'ABERTO' CHECK (status IN ('ABERTO', 'EM_ATENDIMENTO', 'RESOLVIDO')),
    aberto_em     timestamptz NOT NULL DEFAULT now(),
    fechado_em    timestamptz,
    CHECK ((status = 'RESOLVIDO') = (fechado_em IS NOT NULL)),
    CHECK ((status = 'ABERTO') OR atendente_id IS NOT NULL)
);
CREATE INDEX ix_chamado_cliente ON chamado (cliente_id, aberto_em DESC);
CREATE INDEX ix_chamado_fila ON chamado (status, aberto_em) WHERE status <> 'RESOLVIDO';
COMMENT ON TABLE chamado IS 'Atendimento humano aberto de dentro do app (RF024, RF025).';
COMMENT ON COLUMN chamado.id IS 'Identificador do chamado.';
COMMENT ON COLUMN chamado.cliente_id IS 'Cliente que abriu.';
COMMENT ON COLUMN chamado.atendente_id IS 'Atendente responsável. Obrigatório a partir de EM_ATENDIMENTO.';
COMMENT ON COLUMN chamado.assunto IS '[PII] Assunto escrito pelo cliente. Pode conter dado pessoal.';
COMMENT ON COLUMN chamado.status IS 'ABERTO, EM_ATENDIMENTO ou RESOLVIDO.';
COMMENT ON COLUMN chamado.aberto_em IS 'Momento da abertura.';
COMMENT ON COLUMN chamado.fechado_em IS 'Momento da resolução.';

CREATE TABLE mensagem_chamado (
    id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    chamado_id  uuid        NOT NULL REFERENCES chamado (id) ON DELETE CASCADE,
    autor       text        NOT NULL CHECK (autor IN ('CLIENTE', 'ATENDENTE')),
    texto       text,
    audio_url   text,
    enviada_em  timestamptz NOT NULL DEFAULT now(),
    CHECK (texto IS NOT NULL OR audio_url IS NOT NULL)
);
CREATE INDEX ix_mensagem_chamado ON mensagem_chamado (chamado_id, enviada_em);
COMMENT ON TABLE mensagem_chamado IS 'Mensagens de um chamado. Composição: apagar o chamado apaga as mensagens.';
COMMENT ON COLUMN mensagem_chamado.id IS 'Identificador da mensagem.';
COMMENT ON COLUMN mensagem_chamado.chamado_id IS 'Chamado a que pertence.';
COMMENT ON COLUMN mensagem_chamado.autor IS 'CLIENTE ou ATENDENTE.';
COMMENT ON COLUMN mensagem_chamado.texto IS '[PII] Texto da mensagem. Pode conter dado pessoal.';
COMMENT ON COLUMN mensagem_chamado.audio_url IS '[PII] Endereço no S3 do áudio enviado pelo cliente (US14). Voz é dado pessoal.';
COMMENT ON COLUMN mensagem_chamado.enviada_em IS 'Momento do envio.';

-- =====================================================================
-- Módulo notificacao
-- =====================================================================

CREATE TABLE notificacao (
    id          uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id  uuid        NOT NULL REFERENCES cliente (id),
    canal       text        NOT NULL CHECK (canal IN ('PUSH', 'SMS')),
    tipo        text        NOT NULL,
    conteudo    text        NOT NULL,
    status      text        NOT NULL DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'ENVIADA', 'FALHOU')),
    criada_em   timestamptz NOT NULL DEFAULT now(),
    enviada_em  timestamptz,
    CHECK ((status = 'ENVIADA') = (enviada_em IS NOT NULL))
);
CREATE INDEX ix_notificacao_cliente ON notificacao (cliente_id, criada_em DESC);
COMMENT ON TABLE notificacao IS 'Push e SMS enviados ao cliente (RF028).';
COMMENT ON COLUMN notificacao.id IS 'Identificador da notificação.';
COMMENT ON COLUMN notificacao.cliente_id IS 'Cliente que recebe.';
COMMENT ON COLUMN notificacao.canal IS 'PUSH ou SMS.';
COMMENT ON COLUMN notificacao.tipo IS 'Evento que gerou a notificação, por exemplo PixConcluido.';
COMMENT ON COLUMN notificacao.conteudo IS '[PII] Texto enviado. Pode ter valor e nome de terceiro.';
COMMENT ON COLUMN notificacao.status IS 'PENDENTE, ENVIADA ou FALHOU.';
COMMENT ON COLUMN notificacao.criada_em IS 'Momento da criação.';
COMMENT ON COLUMN notificacao.enviada_em IS 'Momento da entrega ao provedor de push ou SMS.';

CREATE TABLE outbox_evento (
    id                    bigint      GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tipo                  text        NOT NULL,
    agregado_id           uuid        NOT NULL,
    payload               jsonb       NOT NULL,
    criado_em             timestamptz NOT NULL DEFAULT now(),
    processado_em         timestamptz,
    tentativas            integer     NOT NULL DEFAULT 0 CHECK (tentativas >= 0),
    proxima_tentativa_em  timestamptz NOT NULL DEFAULT now()
);
-- o worker busca só os pendentes, na ordem da próxima tentativa (ADR-008)
CREATE INDEX ix_outbox_pendentes ON outbox_evento (proxima_tentativa_em) WHERE processado_em IS NULL;
COMMENT ON TABLE outbox_evento IS 'Eventos gravados na mesma transação do dado e entregues pelo worker (ADR-008).';
COMMENT ON COLUMN outbox_evento.id IS 'Número sequencial do evento.';
COMMENT ON COLUMN outbox_evento.tipo IS 'Nome do evento de domínio, por exemplo PixConcluido ou ContaBloqueada.';
COMMENT ON COLUMN outbox_evento.agregado_id IS 'Identificador da entidade de origem.';
COMMENT ON COLUMN outbox_evento.payload IS '[PII] Dados do evento em JSON. Pode conter dado pessoal; apagado 90 dias após processado.';
COMMENT ON COLUMN outbox_evento.criado_em IS 'Momento da gravação.';
COMMENT ON COLUMN outbox_evento.processado_em IS 'Momento em que o worker terminou. Vazio enquanto pendente.';
COMMENT ON COLUMN outbox_evento.tentativas IS 'Quantas vezes o worker tentou.';
COMMENT ON COLUMN outbox_evento.proxima_tentativa_em IS 'Quando tentar de novo (espera crescente após erro).';

CREATE TABLE lembrete_conta (
    id              uuid    PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id      uuid    NOT NULL REFERENCES cliente (id) ON DELETE CASCADE,
    descricao       text    NOT NULL,
    dia_vencimento  integer NOT NULL CHECK (dia_vencimento BETWEEN 1 AND 31),
    ativo           boolean NOT NULL DEFAULT true
);
CREATE INDEX ix_lembrete_dia ON lembrete_conta (dia_vencimento) WHERE ativo;
COMMENT ON TABLE lembrete_conta IS 'Conta a vencer cadastrada pelo cliente para receber lembrete (RF022).';
COMMENT ON COLUMN lembrete_conta.id IS 'Identificador do lembrete.';
COMMENT ON COLUMN lembrete_conta.cliente_id IS 'Cliente lembrado.';
COMMENT ON COLUMN lembrete_conta.descricao IS 'Nome da conta, por exemplo Conta de água.';
COMMENT ON COLUMN lembrete_conta.dia_vencimento IS 'Dia do mês do vencimento (1 a 31). O lembrete sai 3 dias antes.';
COMMENT ON COLUMN lembrete_conta.ativo IS 'Falso quando o cliente desliga o lembrete.';

COMMIT;
