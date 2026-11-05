"""Gera o dicionário de dados (04-dicionario-de-dados.md) a partir do catálogo do PostgreSQL.

Nada é digitado à mão: o script sobe um PostgreSQL 17 descartável no Docker,
aplica sql/001_schema.sql e lê do catálogo (pg_catalog) cada tabela, coluna,
tipo, nulidade, valor padrão, restrição, índice e o COMMENT ON de cada coluna.
A coluna LGPD sai das marcações no começo do comentário: [PII], [PII-SENSIVEL],
[CIFRADO], [SEGREDO].

Uso: python -I bloco-5-banco/ferramentas/gerar_dicionario.py
Precisa de: Docker em execução.
"""

import json
import pathlib
import re
import subprocess
import sys
import time

AQUI = pathlib.Path(__file__).resolve().parent
BLOCO = AQUI.parent
SCHEMA = BLOCO / "sql" / "001_schema.sql"
SAIDA = BLOCO / "04-dicionario-de-dados.md"
NOME = "rufus-db-dicionario"

# dono de cada tabela, igual a bloco-3-arquitetura/05-modelo-de-dominio.md
MODULOS = {
    "identidade": ["cliente", "dispositivo", "credencial", "sessao_renovacao", "consentimento"],
    "contas": ["conta", "carteira", "lancamento", "saldo_fechamento_diario"],
    "pagamentos": ["transacao", "pix_envio", "pix_recebimento", "pagamento_boleto", "movimento_meta", "chave_pix", "meta"],
    "familia": ["vinculo_responsavel", "pedido_aprovacao", "contato_confianca"],
    "antifraude": ["analise_risco"],
    "atendimento": ["chamado", "mensagem_chamado"],
    "backoffice": ["funcionario", "registro_auditoria"],
    "notificacao": ["notificacao", "outbox_evento", "lembrete_conta"],
}

CONSULTA = r"""
SELECT json_agg(t ORDER BY t.tabela) FROM (
  SELECT c.relname AS tabela,
         obj_description(c.oid, 'pg_class') AS descricao,
         (SELECT json_agg(json_build_object(
                    'campo', a.attname,
                    'tipo', format_type(a.atttypid, a.atttypmod),
                    'nulo', NOT a.attnotnull,
                    'padrao', pg_get_expr(d.adbin, d.adrelid),
                    'identity', a.attidentity <> '',
                    'comentario', col_description(c.oid, a.attnum),
                    'num', a.attnum) ORDER BY a.attnum)
            FROM pg_attribute a
            LEFT JOIN pg_attrdef d ON d.adrelid = a.attrelid AND d.adnum = a.attnum
           WHERE a.attrelid = c.oid AND a.attnum > 0 AND NOT a.attisdropped) AS colunas,
         (SELECT json_agg(json_build_object(
                    'nome', k.conname, 'tipo', k.contype,
                    'colunas', (SELECT json_agg(att.attname ORDER BY att.attnum) FROM pg_attribute att
                                 WHERE att.attrelid = k.conrelid AND att.attnum = ANY (k.conkey)),
                    'def', pg_get_constraintdef(k.oid),
                    'ref', CASE WHEN k.contype = 'f' THEN k.confrelid::regclass::text END))
            FROM pg_constraint k WHERE k.conrelid = c.oid) AS restricoes,
         (SELECT json_agg(json_build_object('nome', i.relname, 'def', pg_get_indexdef(i.oid),
                                            'unico', x.indisunique, 'pk', x.indisprimary))
            FROM pg_index x JOIN pg_class i ON i.oid = x.indexrelid WHERE x.indrelid = c.oid) AS indices
    FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
   WHERE n.nspname = 'rufus' AND c.relkind = 'r') t;
"""


def sh(*cmd, entrada=None):
    r = subprocess.run(cmd, input=entrada, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        sys.exit(f"ABORTADO: {' '.join(cmd[:4])}...\n{r.stderr}")
    return r.stdout


def catalogo():
    subprocess.run(["docker", "rm", "-f", NOME], capture_output=True)
    sh("docker", "run", "-d", "--name", NOME, "-e", "POSTGRES_PASSWORD=d", "-e", "POSTGRES_DB=rufus", "postgres:17-alpine")
    try:
        for _ in range(40):
            if subprocess.run(["docker", "exec", NOME, "pg_isready", "-U", "postgres", "-d", "rufus"],
                              capture_output=True).returncode == 0:
                break
            time.sleep(1)
        time.sleep(2)
        psql = ["docker", "exec", "-i", NOME, "psql", "-U", "postgres", "-d", "rufus", "-v", "ON_ERROR_STOP=1", "-q"]
        sh(*psql, entrada=SCHEMA.read_text(encoding="utf-8"))
        bruto = sh(*psql, "-tA", entrada=CONSULTA)
        versao = sh(*psql, "-tA", "-c", "show server_version").strip()
        return json.loads(bruto), versao
    finally:
        subprocess.run(["docker", "rm", "-f", NOME], capture_output=True)


def lgpd(comentario):
    tags = re.findall(r"\[(PII-SENSIVEL|PII|CIFRADO|SEGREDO)\]", comentario or "")
    return ", ".join(tags) if tags else "-"


def sem_tags(comentario):
    return re.sub(r"^(\[[A-Z-]+\])+\s*", "", comentario or "").strip()


def legivel(expr):
    """Deixa a expressão do catálogo mais fácil de ler, sem mudar o sentido."""
    e = expr.removeprefix("CHECK ")
    e = re.sub(r"::(text|bpchar|interval|timestamp with time zone|integer|bigint)", "", e)
    e = re.sub(r"(\w+) = ANY \(ARRAY\[(.*?)\]\)", r"\1 IN (\2)", e)
    while e.startswith("((") and e.endswith("))"):
        e = e[1:-1]
    if e.startswith("(") and e.endswith(")") and e.count("(") == 1:
        e = e[1:-1]
    return e


def celula(txt):
    return (txt or "").replace("|", "\\|").replace("\n", " ")


def restricoes_da_coluna(campo, tab):
    itens = []
    for k in tab["restricoes"] or []:
        cols = k["colunas"] or []
        if campo not in cols:
            continue
        if k["tipo"] == "p":
            itens.append("PK")
        elif k["tipo"] == "f":
            itens.append(f"FK → {k['ref'].removeprefix('rufus.')}" + ("" if len(cols) == 1 else f" ({', '.join(cols)})"))
        elif k["tipo"] == "u":
            itens.append("UNIQUE" if len(cols) == 1 else f"UNIQUE ({', '.join(cols)})")
        elif k["tipo"] == "c" and len(cols) == 1:
            itens.append(legivel(k["def"]))
    for i in tab["indices"] or []:
        if i["unico"] and not i["pk"] and " WHERE " in i["def"]:
            cols = re.search(r"\((.+?)\)", i["def"].split(" USING ")[1]).group(1)
            if campo in [c.strip() for c in cols.split(",")] or f"({campo})" in i["def"]:
                itens.append(f"UNIQUE parcial ({i['def'].split(' WHERE ')[1]})")
    return "<br>".join(celula(x) for x in itens) or "-"


def main():
    tabelas, versao = catalogo()
    por_nome = {t["tabela"]: t for t in tabelas}
    faltando = set(por_nome) - {t for ts in MODULOS.values() for t in ts}
    if faltando:
        sys.exit(f"ABORTADO: tabelas sem módulo no mapa: {sorted(faltando)}")

    total_cols = sum(len(t["colunas"]) for t in tabelas)
    pii = [(t["tabela"], c["campo"], lgpd(c["comentario"])) for t in tabelas for c in t["colunas"] if lgpd(c["comentario"]) != "-"]
    sem_desc = [(t["tabela"], c["campo"]) for t in tabelas for c in t["colunas"] if not sem_tags(c["comentario"])]
    if sem_desc:
        sys.exit(f"ABORTADO: colunas sem descrição de negócio: {sem_desc}")

    out = [
        "# 5.5 Dicionário de dados",
        "",
        "> Arquivo **gerado** por `bloco-5-banco/ferramentas/gerar_dicionario.py` a partir do catálogo de um "
        f"PostgreSQL {versao} real com o `sql/001_schema.sql` aplicado. Não editar à mão: mude o SQL (inclusive os "
        "`COMMENT ON`) e rode o script de novo.",
        "",
        f"{len(tabelas)} tabelas, {total_cols} colunas, **{len(pii)} colunas com marcação LGPD**.",
        "",
        "Legenda da coluna LGPD: **PII** = dado pessoal (LGPD art. 5º, I) · **PII-SENSIVEL** = dado pessoal sensível "
        "(art. 5º, II) · **CIFRADO** = guardado cifrado pela aplicação · **SEGREDO** = credencial, nunca sai do banco "
        "nem vai para log · **-** = sem tratamento especial.",
        "",
        "## Campos com tratamento LGPD",
        "",
        "| Tabela | Campo | Marcação |",
        "| --- | --- | --- |",
    ]
    out += [f"| {t} | {c} | {m} |" for t, c, m in pii]
    out.append("")

    for modulo, nomes in MODULOS.items():
        out += [f"## Módulo {modulo}", ""]
        for nome in nomes:
            t = por_nome[nome]
            out += [f"### {nome}", "", celula(t["descricao"]), "",
                    "| Campo | Tipo | Nulo | Padrão | Restrições | Descrição de negócio | LGPD |",
                    "| --- | --- | --- | --- | --- | --- | --- |"]
            for c in t["colunas"]:
                padrao = "identity" if c["identity"] else (c["padrao"] or "-")
                out.append(
                    f"| `{c['campo']}` | {c['tipo']} | {'sim' if c['nulo'] else 'não'} | {celula(padrao)} | "
                    f"{restricoes_da_coluna(c['campo'], t)} | {celula(sem_tags(c['comentario']))} | {lgpd(c['comentario'])} |")
            regras = [legivel(k["def"]) for k in (t["restricoes"] or []) if k["tipo"] == "c" and len(k["colunas"] or []) > 1]
            if regras:
                out += ["", "Regras entre colunas:", ""] + [f"- `{celula(r)}`" for r in regras]
            idx = [i["def"].replace("rufus.", "") for i in (t["indices"] or []) if not i["pk"]]
            if idx:
                out += ["", "Índices:", ""] + [f"- `{celula(i)}`" for i in idx]
            out.append("")

    SAIDA.write_text("\n".join(out), encoding="utf-8")
    print(f"ok {SAIDA.name}: {len(tabelas)} tabelas, {total_cols} colunas, {len(pii)} com LGPD")
    diagramas_logicos(por_nome)


# Diagramas do modelo lógico, gerados do mesmo catálogo (tabela e desenho não divergem).
GRUPOS = {
    "logico-1-identidade-familia-backoffice": (
        "Modelo lógico 1 de 3: identidade, família e backoffice",
        MODULOS["identidade"] + MODULOS["familia"] + MODULOS["backoffice"]),
    "logico-2-contas-pagamentos": (
        "Modelo lógico 2 de 3: contas, razão contábil e pagamentos",
        MODULOS["contas"] + MODULOS["pagamentos"]),
    "logico-3-antifraude-atendimento-notificacao": (
        "Modelo lógico 3 de 3: antifraude, atendimento e notificação",
        MODULOS["antifraude"] + MODULOS["atendimento"] + MODULOS["notificacao"]),
}


def tipo_curto(t):
    t = t.replace("timestamp with time zone", "timestamptz").replace("character", "char")
    t = t.replace("[]", "_array").replace(" ", "_")
    return re.sub(r"\((\d+)\)", r"\1", t)  # char(64) -> char64 (o Mermaid não aceita parênteses)


def diagramas_logicos(por_nome):
    pasta = BLOCO / "diagramas"
    pasta.mkdir(exist_ok=True)
    for arquivo, (titulo, nomes) in GRUPOS.items():
        fks = []  # (pai, filho, coluna, unica, nula)
        for nome in nomes:
            t = por_nome[nome]
            unicas = {tuple(k["colunas"]) for k in t["restricoes"] or [] if k["tipo"] in "pu"}
            for k in t["restricoes"] or []:
                if k["tipo"] != "f":
                    continue
                pai = k["ref"].removeprefix("rufus.")
                col = k["colunas"][0]
                nula = next(c["nulo"] for c in t["colunas"] if c["campo"] == col)
                fks.append((pai, nome, col, (col,) in unicas, nula))
        externos = sorted({pai for pai, *_ in fks if pai not in nomes})
        linhas = [f"%% titulo: {titulo}", "erDiagram"]
        for nome in nomes:
            t = por_nome[nome]
            pk = {c for k in t["restricoes"] or [] if k["tipo"] == "p" for c in k["colunas"]}
            fk = {k["colunas"][0] for k in t["restricoes"] or [] if k["tipo"] == "f"}
            uk = {k["colunas"][0] for k in t["restricoes"] or [] if k["tipo"] == "u" and len(k["colunas"]) == 1}
            linhas.append(f"    {nome} {{")
            for c in t["colunas"]:
                marcas = [m for m, s in (("PK", pk), ("FK", fk), ("UK", uk)) if c["campo"] in s]
                linhas.append(f"        {tipo_curto(c['tipo'])} {c['campo']} {','.join(marcas)}".rstrip())
            linhas.append("    }")
        for nome in externos:  # tabela de outro grupo: só a chave, para mostrar a ligação
            linhas += [f"    {nome} {{", "        uuid id PK", "    }"]
        for pai, filho, col, unica, nula in fks:
            esquerda = "|o" if nula else "||"
            direita = "o|" if unica else "o{"
            linhas.append(f'    {pai} {esquerda}--{direita} {filho} : "{col}"')
        (pasta / f"{arquivo}.mmd").write_text("\n".join(linhas) + "\n", encoding="utf-8")
        print(f"ok diagramas/{arquivo}.mmd")


if __name__ == "__main__":
    main()
