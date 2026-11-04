"""Gera todos os diagramas do projeto com cabeçalho de título, autores e data.

O enunciado exige em CADA diagrama: título, nomes dos integrantes e data.
Este script garante isso de um jeito só: ele procura fontes em qualquer pasta
`diagramas/` do repositório e gera, ao lado, a pasta `diagramas/img/` com:

  - <nome>.svg  diagrama final com faixa de cabeçalho (vai para o AID em PDF)
  - <nome>.png  mesmo diagrama em imagem (vai para os slides)

Fontes aceitas:
  - <nome>.mmd  Mermaid. A 1ª linha deve ser:  %% titulo: Diagrama de ...
  - <nome>.svg.py  script Python que imprime um SVG no stdout (usado para
    notação UML que o Mermaid não tem: casos de uso e componentes).
    A 1ª linha deve ser:  # titulo: Diagrama de ...

Autores e data saem de projeto.json, na raiz. Mudou a equipe, rode de novo.

Uso:  python ferramentas/diagramas/gerar.py            (todos)
      python ferramentas/diagramas/gerar.py bloco-4-uml (só uma pasta)

Precisa de: Node (npx @mermaid-js/mermaid-cli) e Google Chrome (para o PNG).
"""

import html
import json
import pathlib
import re
import subprocess
import sys
import tempfile

RAIZ = pathlib.Path(__file__).resolve().parents[2]
AQUI = pathlib.Path(__file__).resolve().parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CONFIG_MERMAID = AQUI / "mermaid-config.json"
FAIXA = 64  # altura do cabeçalho em px
MARGEM = 24


def projeto():
    return json.loads((RAIZ / "projeto.json").read_text(encoding="utf-8"))


def titulo_de(fonte: pathlib.Path) -> str:
    primeira = fonte.read_text(encoding="utf-8").splitlines()[0]
    m = re.match(r"\s*(?:%%|#)\s*titulo:\s*(.+)", primeira)
    if not m:
        sys.exit(f"ABORTADO: {fonte} não começa com a linha de titulo")
    return m.group(1).strip()


def svg_mermaid(fonte: pathlib.Path) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        saida = pathlib.Path(tmp) / "d.svg"
        cmd = ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", str(fonte), "-o", str(saida),
               "-b", "white", "-c", str(CONFIG_MERMAID)]
        r = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform == "win32"))
        if r.returncode != 0 or not saida.exists():
            sys.exit(f"ABORTADO: mermaid falhou em {fonte}\n{r.stdout}\n{r.stderr}")
        return saida.read_text(encoding="utf-8")


def svg_python(fonte: pathlib.Path) -> str:
    r = subprocess.run([sys.executable, "-I", str(fonte)], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0 or "<svg" not in r.stdout:
        sys.exit(f"ABORTADO: {fonte} falhou\n{r.stderr}")
    return r.stdout


def dimensoes(svg: str):
    m = re.search(r'viewBox="\s*([-\d.]+)[ ,]+([-\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)"', svg)
    if not m:
        sys.exit("ABORTADO: SVG sem viewBox")
    return [float(x) for x in m.groups()]


def envolver(svg: str, titulo: str, p: dict) -> tuple[str, int, int]:
    vx, vy, vw, vh = dimensoes(svg)
    autores = ", ".join(m["nome"] for m in p["equipe"])
    d = p["data"].split("-")
    data_br = f"{d[2]}/{d[1]}/{d[0]}"
    linha2 = f"{p['nome']} · Autores: {autores} · {data_br}"
    # largura mínima para o cabeçalho caber: ~10 px por caractere no título (17 px, negrito)
    # e ~7 px na linha de autores (12 px)
    minimo = max(len(titulo) * 10, len(linha2) * 7)
    largura = int(max(vw, minimo, 640) + 2 * MARGEM)
    altura = int(vh + FAIXA + 2 * MARGEM)
    # o SVG interno vira um <svg> aninhado, posicionado abaixo da faixa
    interno = re.sub(r"^<\?xml[^>]*>", "", svg.strip())
    interno = re.sub(r"<svg\b", f'<svg x="{MARGEM + (largura - 2 * MARGEM - vw) / 2}" y="{FAIXA + MARGEM}" '
                     f'width="{vw}" height="{vh}"', interno, count=1)
    interno = re.sub(r'\s(width|height)="100%"', "", interno)
    interno = re.sub(r'style="max-width:[^"]*"', "", interno, count=1)
    cab = (
        f'<rect x="0" y="0" width="{largura}" height="{FAIXA}" fill="#F3F4F6"/>'
        f'<line x1="0" y1="{FAIXA}" x2="{largura}" y2="{FAIXA}" stroke="#D1D5DB"/>'
        f'<text x="{MARGEM}" y="27" font-family="Arial, Helvetica, sans-serif" font-size="17" '
        f'font-weight="700" fill="#111827">{html.escape(titulo)}</text>'
        f'<text x="{MARGEM}" y="49" font-family="Arial, Helvetica, sans-serif" font-size="12" '
        f'fill="#4B5563">{html.escape(linha2)}</text>'
    )
    final = (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">'
        f'<rect width="100%" height="100%" fill="#FFFFFF"/>{cab}{interno}</svg>'
    )
    return final, largura, altura


def png(svg_final: pathlib.Path, largura: int, altura: int):
    destino = svg_final.with_suffix(".png")
    html_tmp = svg_final.with_suffix(".tmp.html")
    html_tmp.write_text(
        f'<!doctype html><html><body style="margin:0;background:#fff">'
        f'<img src="{svg_final.name}" width="{largura}" height="{altura}"></body></html>', encoding="utf-8")
    cmd = [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
           f"--window-size={largura},{altura}", f"--screenshot={destino}", html_tmp.as_uri()]
    subprocess.run(cmd, capture_output=True)
    html_tmp.unlink(missing_ok=True)
    if not destino.exists():
        sys.exit(f"ABORTADO: PNG não gerado para {svg_final}")


def main():
    p = projeto()
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    fontes = sorted(
        f for f in RAIZ.rglob("diagramas/*")
        if f.is_file() and (f.suffix == ".mmd" or f.name.endswith(".svg.py"))
        and filtro in str(f.relative_to(RAIZ)).replace("\\", "/")
        and "node_modules" not in f.parts
    )
    if not fontes:
        sys.exit("nenhuma fonte encontrada")
    for f in fontes:
        titulo = titulo_de(f)
        svg = svg_mermaid(f) if f.suffix == ".mmd" else svg_python(f)
        final, w, h = envolver(svg, titulo, p)
        nome = f.name.removesuffix(".svg.py").removesuffix(".mmd")
        saida = f.parent / "img" / f"{nome}.svg"
        saida.parent.mkdir(exist_ok=True)
        saida.write_text(final, encoding="utf-8")
        png(saida, w, h)
        print(f"ok  {saida.relative_to(RAIZ)}  ({w}x{h})")


if __name__ == "__main__":
    main()
