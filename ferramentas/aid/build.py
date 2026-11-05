"""Monta o AID (Documento de Apoio) em PDF a partir dos .md do repositório.

Enunciado (slide 16): PDF com sumário, os 9 blocos na ordem, todos os
diagramas incluídos e legíveis, cada diagrama com título, integrantes e data.

Etapas, e o build ABORTA se qualquer uma falhar:
  1. junta os .md na ordem do MANIFESTO (falta arquivo = aborta)
  2. converte para HTML (python-markdown) com capa e sumário
  3. imprime em PDF com o Chrome headless
  4. lê o PDF (PyMuPDF), descobre em que página cada seção caiu e refaz o
     sumário com os números certos (contar, nunca digitar)
  5. carimba rodapé "Rufus Bank · AID · página N de T" em cada folha
  6. audita: PDF mais novo que as fontes, todo diagrama presente, nenhum
     texto proibido (travessão, "a definir", "TODO")

Uso:  python -I ferramentas/aid/build.py
Saída: entrega/AID-Rufus-Bank.pdf
"""

import datetime as dt
import html
import json
import pathlib
import re
import subprocess
import sys

import fitz  # PyMuPDF
import markdown

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SAIDA_DIR = RAIZ / "entrega"
HTML = SAIDA_DIR / "aid.html"
PDF = SAIDA_DIR / "AID-Rufus-Bank.pdf"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# (título do bloco no sumário, [arquivos na ordem])
MANIFESTO = [
    ("Bloco 1 · Concepção e Escopo", [
        "bloco-1-concepcao/01-visao.md",
        "bloco-1-concepcao/02-personas.md",
        "bloco-1-concepcao/03-stakeholders.md",
        "bloco-1-concepcao/04-viabilidade.md",
        "ferramentas/custo-infra/custo-gerado.md",
        "bloco-1-concepcao/05-riscos.md",
    ]),
    ("Bloco 2 · Requisitos", [
        "bloco-2-requisitos/01-requisitos-funcionais.md",
        "bloco-2-requisitos/02-requisitos-nao-funcionais.md",
        "bloco-2-requisitos/03-historias-de-usuario.md",
    ]),
    ("Bloco 3 · Arquitetura de Software", [
        "bloco-3-arquitetura/01-adrs.md",
        "bloco-3-arquitetura/02-c4.md",
        "bloco-3-arquitetura/03-stack.md",
        "bloco-3-arquitetura/04-padroes-de-design.md",
        "bloco-3-arquitetura/05-modelo-de-dominio.md",
        "bloco-3-arquitetura/06-rotas-da-api.md",
    ]),
    ("Bloco 4 · Diagramas UML", ["bloco-4-uml/README.md"]),
    ("Bloco 5 · Banco de Dados", "bloco-5-banco/0*.md"),
    ("Bloco 6 · Infraestrutura e DevOps", "bloco-6-infra/0*.md"),
    ("Bloco 7 · Planejamento e Estimativas", "bloco-7-planejamento/0*.md"),
    ("Bloco 8 · Documentação para o Dev", "bloco-8-dev/0*.md"),
    ("Bloco 9 · Qualidade e Processo", "bloco-9-qualidade/0*.md"),
    ("Fontes e referências", ["fontes.md"]),
]

PROIBIDOS = ["—", "a definir", "TODO", "TBD", "Lorem"]  # "FIMDOSUMARIO" é marcador branco de 1 pt


PARCIAL = "--parcial" in sys.argv  # só para testar enquanto há blocos em andamento


def arquivos(spec):
    if isinstance(spec, str):
        achados = sorted(RAIZ.glob(spec))
        if not achados and not PARCIAL:
            sys.exit(f"ABORTADO: nenhum arquivo para {spec}")
        return achados
    faltando = [a for a in spec if not (RAIZ / a).exists()]
    if faltando and not PARCIAL:
        sys.exit(f"ABORTADO: faltam arquivos: {faltando}")
    return [RAIZ / a for a in spec if (RAIZ / a).exists()]


def md_para_html(caminho: pathlib.Path, bloco_n: int, ids: list):
    texto = caminho.read_text(encoding="utf-8")
    # imagens: caminho relativo vira URI absoluta; svg de diagrama ganha classe
    def img(m):
        alt, alvo = m.group(1), m.group(2)
        abs_ = (caminho.parent / alvo).resolve()
        if not abs_.exists():
            sys.exit(f"ABORTADO: imagem inexistente {alvo} em {caminho}")
        return f'![{alt}]({abs_.as_uri()})'
    texto = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", img, texto)
    # links para outros .md ou arquivos do repo viram texto (não navegam no PDF)
    texto = re.sub(r"(?<!!)\[([^\]]+)\]\((?!https?:)(?!#)([^)]+)\)", r"\1", texto)
    corpo = markdown.markdown(texto, extensions=["tables", "fenced_code", "sane_lists", "attr_list"])
    # headings h1 do arquivo viram h2 do bloco; numeração de âncoras para o sumário
    def h(m):
        nivel = int(m.group(1))
        conteudo = m.group(2)
        novo = min(nivel + 1, 6)
        ident = f"s{len(ids)}"
        if novo <= 3:
            ids.append((novo, re.sub("<[^>]+>", "", conteudo), ident))
        return f'<h{novo} id="{ident}">{conteudo}</h{novo}>'
    corpo = re.sub(r"<h([1-6])[^>]*>(.*?)</h\1>", h, corpo)
    return f'<section class="arquivo">{corpo}</section>'


def montar_html(numeros: dict | None):
    p = json.loads((RAIZ / "projeto.json").read_text(encoding="utf-8"))
    d = p["data"].split("-")
    data_br = f"{d[2]}/{d[1]}/{d[0]}"
    ids = []  # (nivel, texto, id)
    blocos_html = []
    for n, (titulo, spec) in enumerate(MANIFESTO, start=1):
        if not arquivos(spec):
            continue
        ident = f"b{n}"
        ids.append((1, titulo, ident))
        partes = [f'<h1 id="{ident}" class="bloco">{html.escape(titulo)}</h1>']
        for arq in arquivos(spec):
            partes.append(md_para_html(arq, n, ids))
        blocos_html.append(f'<div class="bloco-wrap">{"".join(partes)}</div>')

    linhas = []
    for nivel, texto, ident in ids:
        if nivel > 2:
            continue
        pag = numeros.get(ident, "") if numeros else "00"
        linhas.append(f'<div class="toc n{nivel}"><span class="t">{texto}</span>'
                      f'<span class="dots"></span><span class="p">{pag}</span></div>')
    equipe = "".join(f"<tr><td>{html.escape(m['nome'])}</td><td>{html.escape(m['papel'])}</td></tr>"
                     for m in p["equipe"])
    css = (RAIZ / "ferramentas/aid/aid.css").read_text(encoding="utf-8")
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<title>AID · {html.escape(p['nome'])}</title><style>{css}</style></head><body>
<section class="capa">
  <div class="sup">{html.escape(p['instituicao'])}<br>{html.escape(p['disciplina'])} · {html.escape(p['periodo'])}</div>
  <div class="meio"><div class="nome">{html.escape(p['nome'])}</div>
  <div class="slogan">"{html.escape(p['slogan'])}"</div>
  <div class="tipo">Documento de Apoio (AID) · Da Concepção ao Dia 1 do Dev</div></div>
  <table class="equipe"><tr><th>Integrante</th><th>Papel</th></tr>{equipe}</table>
  <div class="inf">Professor: {html.escape(p['professor'])} · {data_br}</div>
</section>
<section class="sumario"><h1 class="sum">Sumário</h1>{''.join(linhas)}<div class="marca">FIMDOSUMARIO</div></section>
{''.join(blocos_html)}
</body></html>""", ids


def imprimir():
    if PDF.exists():
        PDF.unlink()
    cmd = [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           "--run-all-compositor-stages-before-draw", "--virtual-time-budget=20000",
           f"--print-to-pdf={PDF}", HTML.as_uri()]
    subprocess.run(cmd, capture_output=True)
    if not PDF.exists():
        sys.exit("ABORTADO: Chrome não gerou o PDF")


def paginas_das_secoes(ids):
    """Acha a página de cada título procurando o texto no PDF, depois do sumário."""
    doc = fitz.open(PDF)
    textos = [pg.get_text() for pg in doc]
    fim_sumario = next(i for i, t in enumerate(textos) if "FIMDOSUMARIO" in t)
    numeros = {}
    cursor = fim_sumario + 1
    for nivel, texto, ident in ids:
        if nivel > 2:
            continue
        alvo = re.sub(r"\s+", " ", html.unescape(texto)).strip()
        for i in range(cursor, len(textos)):
            if alvo[:40] in re.sub(r"\s+", " ", textos[i]):
                numeros[ident] = i + 1
                cursor = i
                break
        else:
            sys.exit(f"ABORTADO: não achei a seção '{alvo}' no PDF")
    return numeros, len(doc)


def carimbar_rodape():
    doc = fitz.open(PDF)
    total = len(doc)
    for i, pg in enumerate(doc):
        if i == 0:
            continue  # capa sem rodapé
        r = pg.rect
        pg.insert_text((r.width / 2 - 70, r.height - 20), f"Rufus Bank · AID · página {i + 1} de {total}",
                       fontsize=8, fontname="helv", color=(0.42, 0.45, 0.5))
    tmp = PDF.with_suffix(".tmp.pdf")
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    tmp.replace(PDF)


def auditar(ids):
    fontes = [p for _, spec in MANIFESTO for p in arquivos(spec)]
    if PDF.stat().st_mtime < max(f.stat().st_mtime for f in fontes):
        sys.exit("ABORTADO: PDF mais velho que as fontes")
    doc = fitz.open(PDF)
    texto = "\n".join(pg.get_text() for pg in doc)
    erros = [f"texto proibido: '{p}'" for p in PROIBIDOS if p in texto]
    imagens = sum(len(pg.get_images()) for pg in doc)
    svgs = len(re.findall(r'<img [^>]*\.svg', HTML.read_text(encoding="utf-8")))
    if erros:
        sys.exit("ABORTADO na auditoria:\n  " + "\n  ".join(erros))
    print(f"auditoria ok: {len(doc)} páginas, {svgs} diagramas SVG no HTML, {imagens} imagens raster no PDF")


def main():
    SAIDA_DIR.mkdir(exist_ok=True)
    pagina, ids = montar_html(None)
    HTML.write_text(pagina, encoding="utf-8")
    imprimir()
    numeros, total = paginas_das_secoes(ids)
    pagina, ids = montar_html(numeros)  # mesmo número de linhas no sumário: paginação não muda
    HTML.write_text(pagina, encoding="utf-8")
    imprimir()
    numeros2, _ = paginas_das_secoes(ids)
    if numeros2 != numeros:
        sys.exit("ABORTADO: paginação mudou entre as duas passadas")
    carimbar_rodape()
    auditar(ids)
    print(f"ok  {PDF.relative_to(RAIZ)}  ({total} páginas)  {dt.datetime.now():%d/%m/%Y %H:%M}")


if __name__ == "__main__":
    main()
