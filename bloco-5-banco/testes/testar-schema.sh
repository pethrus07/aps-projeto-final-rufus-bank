#!/usr/bin/env bash
# Rufus Bank · Teste de execução real do modelo físico
# Sobe um PostgreSQL 17 descartável no Docker, aplica 001_schema.sql e 002_seed_dev.sql
# e confere que as restrições recusam o que devem recusar e aceitam o que devem aceitar.
# Uso: bash bloco-5-banco/testes/testar-schema.sh   (grava o resultado em testes/resultado.txt)
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"
SQL="$AQUI/../sql"
NOME=rufus-db-teste
SAIDA="$AQUI/resultado.txt"
export MSYS_NO_PATHCONV=1

docker rm -f "$NOME" >/dev/null 2>&1
docker run -d --name "$NOME" -e POSTGRES_PASSWORD=teste -e POSTGRES_DB=rufus postgres:17-alpine >/dev/null || exit 1
for i in $(seq 1 30); do docker exec "$NOME" pg_isready -U postgres -d rufus >/dev/null 2>&1 && break; sleep 1; done
sleep 2

psql() { docker exec -i "$NOME" psql -U postgres -d rufus -v ON_ERROR_STOP=1 -q "$@"; }

aprovados=0; reprovados=0
{
echo "Rufus Bank · teste do modelo físico · $(date '+%d/%m/%Y %H:%M')"
echo "Servidor: $(docker exec "$NOME" psql -U postgres -tAc 'select version()')"
echo

echo "== Aplicando 001_schema.sql"
psql < "$SQL/001_schema.sql" && echo "ok" || { echo "FALHOU"; exit 1; }
echo "== Aplicando 002_seed_dev.sql"
psql < "$SQL/002_seed_dev.sql" && echo "ok" || { echo "FALHOU"; exit 1; }
echo
echo "Tabelas criadas: $(docker exec "$NOME" psql -U postgres -d rufus -tAc "select count(*) from information_schema.tables where table_schema='rufus'")"
echo "Colunas sem comentário: $(docker exec "$NOME" psql -U postgres -d rufus -tAc "select count(*) from pg_attribute a join pg_class c on c.oid = a.attrelid join pg_namespace n on n.oid = c.relnamespace where n.nspname = 'rufus' and c.relkind = 'r' and a.attnum > 0 and not a.attisdropped and col_description(c.oid, a.attnum) is null")"
echo "Tabelas sem comentário: $(docker exec "$NOME" psql -U postgres -d rufus -tAc "select count(*) from pg_class c join pg_namespace n on n.oid = c.relnamespace where n.nspname = 'rufus' and c.relkind = 'r' and obj_description(c.oid, 'pg_class') is null")"
echo
} > "$SAIDA" 2>&1

caso() { # caso <esperado: passa|falha> <descricao> <sql>
    local esperado="$1" desc="$2" sql="$3" out rc
    out=$(printf 'SET search_path TO rufus;\nBEGIN;\n%s\nCOMMIT;\n' "$sql" | psql 2>&1); rc=$?
    local obtido=passa; [ $rc -ne 0 ] && obtido=falha
    if [ "$obtido" = "$esperado" ]; then
        aprovados=$((aprovados+1)); echo "[OK]    deve $esperado: $desc" >> "$SAIDA"
    else
        reprovados=$((reprovados+1)); echo "[ERRO]  deve $esperado: $desc" >> "$SAIDA"
    fi
    [ -n "$out" ] && echo "        $(echo "$out" | grep -E 'ERROR|ERRO' | head -1)" >> "$SAIDA"
}

A=00000000-0000-0000-0000-0000000a0001   # Antônio
CT=00000000-0000-0000-0000-0000000b0001  # conta do Antônio
CP=00000000-0000-0000-0000-0000000c0001  # carteira principal do Antônio
LQ=00000000-0000-0000-0000-00000000c001  # liquidação Pix

echo "== Casos" >> "$SAIDA"

caso passa "Pix enviado equilibrado (-R\$ 50 na principal, +R\$ 50 na liquidação)" "
INSERT INTO transacao (id, conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('00000000-0000-0000-0000-0000000e0101', '$CT', 'PIX_ENVIO', 5000, 'idem-teste-0001');
INSERT INTO pix_envio (transacao_id, chave_destino, nome_recebedor, documento_recebedor_mascarado, banco_recebedor, destinatario_novo) VALUES ('00000000-0000-0000-0000-0000000e0101', '+5583988887777', 'Mercado Exemplo', '***.456.789-**', 'Banco Exemplo', true);
INSERT INTO lancamento (transacao_id, carteira_id, valor_centavos) VALUES ('00000000-0000-0000-0000-0000000e0101', '$CP', -5000), ('00000000-0000-0000-0000-0000000e0101', '$LQ', 5000);"

caso falha "lançamento desequilibrado (soma diferente de zero)" "
INSERT INTO transacao (id, conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('00000000-0000-0000-0000-0000000e0102', '$CT', 'PIX_ENVIO', 5000, 'idem-teste-0002');
INSERT INTO lancamento (transacao_id, carteira_id, valor_centavos) VALUES ('00000000-0000-0000-0000-0000000e0102', '$CP', -5000), ('00000000-0000-0000-0000-0000000e0102', '$LQ', 4000);"

caso falha "transação com um lançamento só" "
INSERT INTO transacao (id, conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('00000000-0000-0000-0000-0000000e0103', '$CT', 'PIX_ENVIO', 5000, 'idem-teste-0003');
INSERT INTO lancamento (transacao_id, carteira_id, valor_centavos) VALUES ('00000000-0000-0000-0000-0000000e0103', '$CP', -5000);"

caso falha "chave de idempotência repetida na mesma conta (Pix em dobro, RNF11)" "
INSERT INTO transacao (conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('$CT', 'PIX_ENVIO', 5000, 'idem-teste-0001');"

caso passa "mesma chave de idempotência em outra conta" "
INSERT INTO transacao (conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('00000000-0000-0000-0000-0000000b0002', 'PIX_ENVIO', 5000, 'idem-teste-0001');"

caso falha "segundo dispositivo ativo para o mesmo cliente (RF005)" "
INSERT INTO dispositivo (cliente_id, modelo, chave_publica) VALUES ('$A', 'Celular do golpista', 'chave-outra');"

caso passa "troca de aparelho: desativa o antigo e ativa o novo" "
UPDATE dispositivo SET ativo = false WHERE cliente_id = '$A';
INSERT INTO dispositivo (cliente_id, modelo, chave_publica) VALUES ('$A', 'Celular novo', 'chave-nova-antonio');"

caso falha "transação com valor negativo" "
INSERT INTO transacao (conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('$CT', 'BOLETO', -100, 'idem-teste-0004');"

caso falha "lançamento com valor zero" "
INSERT INTO transacao (id, conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('00000000-0000-0000-0000-0000000e0105', '$CT', 'PIX_ENVIO', 1, 'idem-teste-0005');
INSERT INTO lancamento (transacao_id, carteira_id, valor_centavos) VALUES ('00000000-0000-0000-0000-0000000e0105', '$CP', 0), ('00000000-0000-0000-0000-0000000e0105', '$LQ', 0);"

caso falha "alterar um lançamento já gravado (razão só aceita inserção)" "
UPDATE lancamento SET valor_centavos = 999999 WHERE carteira_id = '$CP';"

caso falha "apagar registro de auditoria (RNF14)" "
INSERT INTO registro_auditoria (funcionario_id, acao, entidade, entidade_id, ip) VALUES ('00000000-0000-0000-0000-0000000f0001', 'CONSULTAR_HISTORICO', 'cliente', '$A', '10.0.0.1');
DELETE FROM registro_auditoria;"

caso falha "subtipo de Pix apontando para transação de boleto" "
INSERT INTO transacao (id, conta_id, tipo, valor_centavos, chave_idempotencia) VALUES ('00000000-0000-0000-0000-0000000e0106', '$CT', 'BOLETO', 100, 'idem-teste-0006');
INSERT INTO pix_envio (transacao_id, chave_destino, nome_recebedor, documento_recebedor_mascarado, banco_recebedor, destinatario_novo) VALUES ('00000000-0000-0000-0000-0000000e0106', 'x', 'y', '***', 'z', false);"

caso falha "Pix com nota 85 liberado automaticamente (RF026)" "
INSERT INTO analise_risco (transacao_id, nota, resultado) VALUES ('00000000-0000-0000-0000-0000000e0101', 85, 'LIBERADA_AUTOMATICA');"

caso passa "Pix com nota 85 retido para o analista" "
INSERT INTO analise_risco (transacao_id, nota, motivos, resultado) VALUES ('00000000-0000-0000-0000-0000000e0101', 85, '{DESTINATARIO_NOVO,HORARIO_NOTURNO}', 'RETIDA');"

caso falha "decisão de analista sem analista" "
UPDATE analise_risco SET resultado = 'LIBERADA_ANALISTA' WHERE transacao_id = '00000000-0000-0000-0000-0000000e0101';"

caso falha "limite diário do menor maior que o mensal" "
UPDATE vinculo_responsavel SET limite_diario_centavos = 50000 WHERE menor_cliente_id = '00000000-0000-0000-0000-0000000a0003';"

caso falha "menor vinculado a si mesmo como responsável" "
INSERT INTO vinculo_responsavel (menor_cliente_id, responsavel_cliente_id, limite_diario_centavos, limite_mensal_centavos) VALUES ('$A', '$A', 0, 0);"

caso falha "conta bloqueada sem data de bloqueio" "
UPDATE conta SET status = 'BLOQUEADA_TOTAL' WHERE id = '$CT';"

caso passa "bloquear tudo agora (RF020)" "
UPDATE conta SET status = 'BLOQUEADA_TOTAL', bloqueada_em = now() WHERE id = '$CT';"

caso falha "CPF repetido (mesmo hash)" "
INSERT INTO cliente (nome_completo, cpf_cifrado, cpf_hash, data_nascimento_cifrada, celular, tipo) SELECT 'Outro Nome', cpf_cifrado, cpf_hash, data_nascimento_cifrada, '+5583999990009', 'TITULAR' FROM cliente WHERE id = '$A';"

caso falha "mensagem de chamado sem texto e sem áudio" "
INSERT INTO chamado (id, cliente_id, assunto) VALUES ('00000000-0000-0000-0000-000000ca0001', '$A', 'Dúvida');
INSERT INTO mensagem_chamado (chamado_id, autor) VALUES ('00000000-0000-0000-0000-000000ca0001', 'CLIENTE');"

{
echo
echo "== Saldo da carteira principal do Antônio (soma dos lançamentos)"
docker exec "$NOME" psql -U postgres -d rufus -tAc "select 'R\$ ' || replace((sum(valor_centavos)/100.0)::numeric(14,2)::text, '.', ',') || ' (esperado R\$ 100,00: recebeu 150, enviou 50)' from rufus.lancamento where carteira_id = '$CP'"
echo
echo "Resultado: $aprovados caso(s) como esperado, $reprovados diferente(s) do esperado"
} >> "$SAIDA"

docker rm -f "$NOME" >/dev/null 2>&1
cat "$SAIDA"
[ "$reprovados" -eq 0 ]
