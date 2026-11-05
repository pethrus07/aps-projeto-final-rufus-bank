-- Rufus Bank · Dados fictícios para desenvolvimento local
-- NUNCA rodar em homologação ou produção. Todos os nomes, CPFs e celulares são inventados.
-- Os campos cifrados recebem um texto marcador; em desenvolvimento a aplicação usa a chave local do .env.

BEGIN;
SET search_path TO rufus;

-- Carteiras técnicas de liquidação (do sistema, sem conta)
INSERT INTO carteira (id, conta_id, tipo) VALUES
    ('00000000-0000-0000-0000-00000000c001', NULL, 'LIQUIDACAO_PIX'),
    ('00000000-0000-0000-0000-00000000c002', NULL, 'LIQUIDACAO_BOLETO');

-- Funcionários (senha de desenvolvimento: rufus-dev, hash ilustrativo)
INSERT INTO funcionario (id, nome, email, papel, hash_senha) VALUES
    ('00000000-0000-0000-0000-0000000f0001', 'Ana Atendente',  'ana@rufus.dev',     'ATENDENTE',           '$argon2id$v=19$m=65536,t=3,p=4$ZGV2$ZGV2'),
    ('00000000-0000-0000-0000-0000000f0002', 'Bruno Analista', 'bruno@rufus.dev',   'ANALISTA_ANTIFRAUDE', '$argon2id$v=19$m=65536,t=3,p=4$ZGV2$ZGV2'),
    ('00000000-0000-0000-0000-0000000f0003', 'Clara Admin',    'clara@rufus.dev',   'ADMINISTRADOR',       '$argon2id$v=19$m=65536,t=3,p=4$ZGV2$ZGV2');

-- Clientes: Antônio (titular), Sérgio (titular, responsável) e Camila (menor)
INSERT INTO cliente (id, nome_completo, cpf_cifrado, cpf_hash, data_nascimento_cifrada, celular, tipo, status) VALUES
    ('00000000-0000-0000-0000-0000000a0001', 'Antônio da Silva (fictício)',
     convert_to('dev:11111111111', 'UTF8'), encode(sha256(convert_to('11111111111', 'UTF8')), 'hex'),
     convert_to('dev:1979-03-10', 'UTF8'), '+5583999990001', 'TITULAR', 'ATIVO'),
    ('00000000-0000-0000-0000-0000000a0002', 'Sérgio Souza (fictício)',
     convert_to('dev:22222222222', 'UTF8'), encode(sha256(convert_to('22222222222', 'UTF8')), 'hex'),
     convert_to('dev:1980-07-22', 'UTF8'), '+5583999990002', 'TITULAR', 'ATIVO'),
    ('00000000-0000-0000-0000-0000000a0003', 'Camila Souza (fictícia)',
     convert_to('dev:33333333333', 'UTF8'), encode(sha256(convert_to('33333333333', 'UTF8')), 'hex'),
     convert_to('dev:2009-05-14', 'UTF8'), '+5583999990003', 'MENOR', 'ATIVO');

INSERT INTO credencial (cliente_id, hash_senha) VALUES
    ('00000000-0000-0000-0000-0000000a0001', '$argon2id$v=19$m=65536,t=3,p=4$ZGV2$ZGV2'),
    ('00000000-0000-0000-0000-0000000a0002', '$argon2id$v=19$m=65536,t=3,p=4$ZGV2$ZGV2'),
    ('00000000-0000-0000-0000-0000000a0003', '$argon2id$v=19$m=65536,t=3,p=4$ZGV2$ZGV2');

INSERT INTO dispositivo (id, cliente_id, modelo, chave_publica) VALUES
    ('00000000-0000-0000-0000-0000000d0001', '00000000-0000-0000-0000-0000000a0001', 'Android de entrada (emulador)', 'dev-chave-publica-antonio'),
    ('00000000-0000-0000-0000-0000000d0002', '00000000-0000-0000-0000-0000000a0002', 'iPhone (simulador)',            'dev-chave-publica-sergio'),
    ('00000000-0000-0000-0000-0000000d0003', '00000000-0000-0000-0000-0000000a0003', 'Android (emulador)',            'dev-chave-publica-camila');

INSERT INTO consentimento (cliente_id, tipo, versao_termo, aceito_por_cliente_id) VALUES
    ('00000000-0000-0000-0000-0000000a0001', 'TERMOS_DE_USO',     '2026.1', '00000000-0000-0000-0000-0000000a0001'),
    ('00000000-0000-0000-0000-0000000a0001', 'PRIVACIDADE',       '2026.1', '00000000-0000-0000-0000-0000000a0001'),
    ('00000000-0000-0000-0000-0000000a0002', 'TERMOS_DE_USO',     '2026.1', '00000000-0000-0000-0000-0000000a0002'),
    ('00000000-0000-0000-0000-0000000a0003', 'RESPONSAVEL_LEGAL', '2026.1', '00000000-0000-0000-0000-0000000a0002');

INSERT INTO conta (id, cliente_id, agencia, numero, id_conta_parceiro) VALUES
    ('00000000-0000-0000-0000-0000000b0001', '00000000-0000-0000-0000-0000000a0001', '0001', '100001-1', 'baas-dev-0001'),
    ('00000000-0000-0000-0000-0000000b0002', '00000000-0000-0000-0000-0000000a0002', '0001', '100002-8', 'baas-dev-0002'),
    ('00000000-0000-0000-0000-0000000b0003', '00000000-0000-0000-0000-0000000a0003', '0001', '100003-6', 'baas-dev-0003');

INSERT INTO carteira (id, conta_id, tipo) VALUES
    ('00000000-0000-0000-0000-0000000c0001', '00000000-0000-0000-0000-0000000b0001', 'PRINCIPAL'),
    ('00000000-0000-0000-0000-0000000c0002', '00000000-0000-0000-0000-0000000b0002', 'PRINCIPAL'),
    ('00000000-0000-0000-0000-0000000c0003', '00000000-0000-0000-0000-0000000b0003', 'PRINCIPAL');

-- Vínculo da Camila com o pai: R$ 50 por dia, R$ 400 por mês
INSERT INTO vinculo_responsavel (menor_cliente_id, responsavel_cliente_id, status, limite_diario_centavos, limite_mensal_centavos, aceito_em) VALUES
    ('00000000-0000-0000-0000-0000000a0003', '00000000-0000-0000-0000-0000000a0002', 'ATIVO', 5000, 40000, now());

INSERT INTO chave_pix (conta_id, tipo, valor) VALUES
    ('00000000-0000-0000-0000-0000000b0001', 'CELULAR', '+5583999990001');

-- Antônio recebe a diária de R$ 150 por Pix (partidas dobradas: sai da liquidação, entra na principal)
INSERT INTO transacao (id, conta_id, tipo, valor_centavos, status, chave_idempotencia, id_parceiro, concluida_em) VALUES
    ('00000000-0000-0000-0000-0000000e0001', '00000000-0000-0000-0000-0000000b0001', 'PIX_RECEBIMENTO', 15000, 'CONCLUIDA',
     'webhook-dev-0001', 'E00000000202611041200dev0001', now());
INSERT INTO pix_recebimento (transacao_id, nome_pagador, banco_pagador) VALUES
    ('00000000-0000-0000-0000-0000000e0001', 'Carlos Mestre de Obras (fictício)', 'Banco Exemplo');
INSERT INTO lancamento (transacao_id, carteira_id, valor_centavos) VALUES
    ('00000000-0000-0000-0000-0000000e0001', '00000000-0000-0000-0000-00000000c001', -15000),
    ('00000000-0000-0000-0000-0000000e0001', '00000000-0000-0000-0000-0000000c0001',  15000);

COMMIT;
