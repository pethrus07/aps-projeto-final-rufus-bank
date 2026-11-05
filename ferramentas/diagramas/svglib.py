"""Biblioteca mínima para desenhar diagramas em SVG com posição controlada.

Usada pelos scripts `*.svg.py` (C4, casos de uso, componentes, deployment).
Tudo é posicionado à mão: cada caixa recebe x, y, largura e as linhas de texto
já quebradas. Nada de quebra automática, para o texto nunca sair da forma.

Cada script faz:
    import svglib as s
    d = s.Desenho(largura, altura)
    d.caixa(...); d.seta(...)
    print(d.svg())
"""

import html

FONTE = "Arial, Helvetica, sans-serif"

# cores da convenção C4 (Simon Brown) e tons neutros para UML
C4_PESSOA = ("#08427B", "#073B6F", "#FFFFFF")
C4_SISTEMA = ("#1168BD", "#0B4884", "#FFFFFF")
C4_CONTAINER = ("#438DD5", "#3C7FC0", "#FFFFFF")
C4_COMPONENTE = ("#85BBF0", "#5D82A8", "#000000")
C4_EXTERNO = ("#999999", "#8A8A8A", "#FFFFFF")
C4_BANCO = ("#438DD5", "#3C7FC0", "#FFFFFF")
UML = ("#FFFFFF", "#374151", "#111827")
UML_SUAVE = ("#F9FAFB", "#374151", "#111827")
LINHA = "#4B5563"


def esc(t):
    return html.escape(str(t))


class Desenho:
    def __init__(self, largura, altura):
        self.w, self.h = largura, altura
        self.partes = []
        self.marcadores = set()

    # ---------- texto ----------
    def texto(self, x, y, linhas, tam=13, peso="400", cor="#111827", ancora="middle", italico=False, altura_linha=None):
        if isinstance(linhas, str):
            linhas = [linhas]
        al = altura_linha or round(tam * 1.3)
        est = ' font-style="italic"' if italico else ""
        for i, l in enumerate(linhas):
            self.partes.append(
                f'<text x="{x}" y="{y + i * al}" font-family="{FONTE}" font-size="{tam}" '
                f'font-weight="{peso}" fill="{cor}" text-anchor="{ancora}"{est}>{esc(l)}</text>')

    def rotulo(self, x, y, linhas, tam=11.5, cor="#374151", ancora="middle", fundo=True):
        """Rótulo de seta com fundo branco, para a linha nunca riscar o texto."""
        if isinstance(linhas, str):
            linhas = [linhas]
        al = round(tam * 1.3)
        larg = max(len(l) for l in linhas) * tam * 0.56 + 8
        alt = len(linhas) * al + 4
        if fundo:
            x0 = x - larg / 2 if ancora == "middle" else (x - 4 if ancora == "start" else x - larg + 4)
            self.partes.append(f'<rect x="{x0}" y="{y - tam - 2}" width="{larg}" height="{alt}" fill="#FFFFFF" fill-opacity="0.95"/>')
        self.texto(x, y, linhas, tam=tam, cor=cor, ancora=ancora)

    # ---------- formas ----------
    def caixa(self, x, y, w, h, titulo, linhas=(), cores=UML, raio=8, tipo=None, tam_titulo=14, tracejada=False):
        fundo, borda, tinta = cores
        traco = ' stroke-dasharray="6 4"' if tracejada else ""
        self.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{raio}" fill="{fundo}" stroke="{borda}" stroke-width="1.4"{traco}/>')
        cy = y + 24
        self.texto(x + w / 2, cy, titulo, tam=tam_titulo, peso="700", cor=tinta)
        cy += 17
        if tipo:
            self.texto(x + w / 2, cy, f"[{tipo}]", tam=11.5, cor=tinta)
            cy += 20
        if linhas:
            self.texto(x + w / 2, cy, list(linhas), tam=12, cor=tinta)

    def banco(self, x, y, w, h, titulo, linhas=(), cores=C4_BANCO, tipo=None):
        """Cilindro, notação usual de banco de dados."""
        fundo, borda, tinta = cores
        e = 12
        self.partes.append(
            f'<path d="M{x} {y + e} A{w / 2} {e} 0 0 1 {x + w} {y + e} V{y + h - e} A{w / 2} {e} 0 0 1 {x} {y + h - e} Z" '
            f'fill="{fundo}" stroke="{borda}" stroke-width="1.4"/>'
            f'<path d="M{x} {y + e} A{w / 2} {e} 0 0 0 {x + w} {y + e}" fill="none" stroke="{borda}" stroke-width="1.4"/>')
        cy = y + 2 * e + 20
        self.texto(x + w / 2, cy, titulo, tam=14, peso="700", cor=tinta)
        cy += 17
        if tipo:
            self.texto(x + w / 2, cy, f"[{tipo}]", tam=11.5, cor=tinta)
            cy += 20
        if linhas:
            self.texto(x + w / 2, cy, list(linhas), tam=12, cor=tinta)

    def pessoa(self, x, y, w, h, titulo, linhas=(), cores=C4_PESSOA):
        """Pessoa no estilo C4: cabeça redonda sobre caixa arredondada."""
        fundo, borda, tinta = cores
        r = 18
        self.partes.append(f'<circle cx="{x + w / 2}" cy="{y + r}" r="{r}" fill="{fundo}" stroke="{borda}" stroke-width="1.4"/>')
        self.caixa(x, y + 2 * r - 4, w, h - 2 * r + 4, titulo, linhas, cores=cores, raio=16, tipo="Pessoa")

    def fronteira(self, x, y, w, h, nome, tipo=None, cor="#6B7280", posicao="baixo-esq"):
        """posicao do rótulo: baixo-esq (padrão C4), baixo-dir, cima-esq ou cima-dir."""
        self.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" stroke="{cor}" stroke-width="1.2" stroke-dasharray="8 5"/>')
        rot = nome + (f"  [{tipo}]" if tipo else "")
        if posicao == "cima-esq":
            self.texto(x + 12, y + 20, rot, tam=12.5, peso="700", cor=cor, ancora="start")
        elif posicao == "cima-dir":
            self.texto(x + w - 12, y + 20, rot, tam=12.5, peso="700", cor=cor, ancora="end")
        elif posicao == "baixo-dir":
            self.texto(x + w - 12, y + h - 12, rot, tam=12.5, peso="700", cor=cor, ancora="end")
        else:
            self.texto(x + 12, y + h - 12, rot, tam=12.5, peso="700", cor=cor, ancora="start")

    def ator(self, cx, y, nome_linhas, tam=12.5):
        """Ator UML: boneco palito com nome embaixo."""
        s = LINHA
        self.partes.append(
            f'<circle cx="{cx}" cy="{y + 9}" r="9" fill="#FFFFFF" stroke="{s}" stroke-width="1.5"/>'
            f'<line x1="{cx}" y1="{y + 18}" x2="{cx}" y2="{y + 42}" stroke="{s}" stroke-width="1.5"/>'
            f'<line x1="{cx - 15}" y1="{y + 26}" x2="{cx + 15}" y2="{y + 26}" stroke="{s}" stroke-width="1.5"/>'
            f'<line x1="{cx}" y1="{y + 42}" x2="{cx - 12}" y2="{y + 60}" stroke="{s}" stroke-width="1.5"/>'
            f'<line x1="{cx}" y1="{y + 42}" x2="{cx + 12}" y2="{y + 60}" stroke="{s}" stroke-width="1.5"/>')
        self.texto(cx, y + 78, nome_linhas, tam=tam, peso="700", altura_linha=round(tam * 1.3))

    def ator_sistema(self, x, y, w, h, nome_linhas, tam=12.5):
        """Ator que é sistema externo: retângulo com estereótipo «sistema»."""
        self.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#F3F4F6" stroke="{LINHA}" stroke-width="1.4"/>')
        self.texto(x + w / 2, y + 18, "«sistema externo»", tam=tam - 1.5, cor="#4B5563", italico=True)
        self.texto(x + w / 2, y + 38, nome_linhas, tam=tam, peso="700")

    def caso(self, cx, cy, rx, ry, linhas, tam=12):
        self.partes.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#FFFFFF" stroke="{LINHA}" stroke-width="1.4"/>')
        if isinstance(linhas, str):
            linhas = [linhas]
        al = round(tam * 1.25)
        y0 = cy + tam / 3 - (len(linhas) - 1) * al / 2
        self.texto(cx, y0, linhas, tam=tam, altura_linha=al)

    def componente(self, x, y, w, h, nome_linhas, estereotipo="«component»", cores=UML):
        """Componente UML 2: retângulo com o ícone de componente no canto."""
        fundo, borda, tinta = cores
        self.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fundo}" stroke="{borda}" stroke-width="1.4"/>')
        ix, iy = x + w - 26, y + 8
        self.partes.append(
            f'<rect x="{ix}" y="{iy}" width="16" height="20" fill="#FFFFFF" stroke="{borda}" stroke-width="1.1"/>'
            f'<rect x="{ix - 4}" y="{iy + 4}" width="8" height="4" fill="#FFFFFF" stroke="{borda}" stroke-width="1.1"/>'
            f'<rect x="{ix - 4}" y="{iy + 12}" width="8" height="4" fill="#FFFFFF" stroke="{borda}" stroke-width="1.1"/>')
        self.texto(x + w / 2 - 8, y + 22, estereotipo, tam=11, cor="#4B5563", italico=True)
        self.texto(x + w / 2 - 8, y + 40, nome_linhas, tam=13, peso="700", cor=tinta)

    def no(self, x, y, w, h, nome_linhas, estereotipo="«device»"):
        """Nó UML de deployment: caixa 3D."""
        p = 10
        self.partes.append(
            f'<path d="M{x} {y + p} L{x + p} {y} H{x + w + p} V{y + h - p} L{x + w} {y + h}" fill="#E5E7EB" stroke="{LINHA}" stroke-width="1.3"/>'
            f'<path d="M{x + w} {y + p} L{x + w + p} {y}" stroke="{LINHA}" stroke-width="1.3"/>'
            f'<rect x="{x}" y="{y + p}" width="{w}" height="{h - p}" fill="#F9FAFB" stroke="{LINHA}" stroke-width="1.3"/>')
        self.texto(x + 12, y + p + 20, estereotipo, tam=11, cor="#4B5563", ancora="start", italico=True)
        self.texto(x + 12, y + p + 37, nome_linhas, tam=13, peso="700", ancora="start")

    def artefato(self, x, y, w, h, nome_linhas, estereotipo="«artifact»"):
        self.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{LINHA}" stroke-width="1.2"/>')
        fx = x + w - 16
        self.partes.append(f'<path d="M{fx} {y + 6} h6 l4 4 v10 h-10 z" fill="#FFFFFF" stroke="{LINHA}" stroke-width="1"/>')
        self.texto(x + (w - 14) / 2, y + 18, estereotipo, tam=10.5, cor="#4B5563", italico=True)
        self.texto(x + (w - 14) / 2, y + 35, nome_linhas, tam=12, peso="700")

    def pirulito(self, cx, cy, nome, lado="cima"):
        """Interface fornecida (lollipop): círculo com nome."""
        self.partes.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#FFFFFF" stroke="{LINHA}" stroke-width="1.4"/>')
        if lado == "cima":
            self.texto(cx, cy - 13, nome, tam=11, cor="#1F2937")
        elif lado == "baixo":
            self.texto(cx, cy + 22, nome, tam=11, cor="#1F2937")
        elif lado == "esq":
            self.texto(cx - 18, cy + 4, nome, tam=11, cor="#1F2937", ancora="end")
        else:
            self.texto(cx + 18, cy + 4, nome, tam=11, cor="#1F2937", ancora="start")

    def soquete(self, cx, cy, direcao="cima"):
        """Interface requerida (socket): meia-lua aberta voltada para o pirulito."""
        r = 11
        arcos = {
            "cima": f"M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}",
            "baixo": f"M{cx - r} {cy} A{r} {r} 0 0 0 {cx + r} {cy}",
            "esq": f"M{cx} {cy - r} A{r} {r} 0 0 0 {cx} {cy + r}",
            "dir": f"M{cx} {cy - r} A{r} {r} 0 0 1 {cx} {cy + r}",
        }
        self.partes.append(f'<path d="{arcos[direcao]}" fill="none" stroke="{LINHA}" stroke-width="1.4"/>')

    # ---------- linhas ----------
    def _marcador(self, tipo):
        self.marcadores.add(tipo)
        return f"url(#m-{tipo})"

    def seta(self, pontos, tracejada=False, ponta="cheia", cor=LINHA, largura=1.3):
        """Linha poligonal pelos pontos [(x,y),...]. ponta: cheia, aberta, nenhuma."""
        d = "M" + " L".join(f"{x} {y}" for x, y in pontos)
        traco = ' stroke-dasharray="6 4"' if tracejada else ""
        fim = f' marker-end="{self._marcador(ponta)}"' if ponta != "nenhuma" else ""
        self.partes.append(f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="{largura}"{traco}{fim}/>')

    def generalizacao(self, pontos):
        d = "M" + " L".join(f"{x} {y}" for x, y in pontos)
        self.partes.append(f'<path d="{d}" fill="none" stroke="{LINHA}" stroke-width="1.3" marker-end="{self._marcador("triangulo")}"/>')

    def linha(self, pontos, cor=LINHA, largura=1.3):
        self.seta(pontos, ponta="nenhuma", cor=cor, largura=largura)

    def svg(self):
        defs = []
        if "cheia" in self.marcadores:
            defs.append(f'<marker id="m-cheia" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{LINHA}"/></marker>')
        if "aberta" in self.marcadores:
            defs.append(f'<marker id="m-aberta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="none" stroke="{LINHA}" stroke-width="1.4"/></marker>')
        if "triangulo" in self.marcadores:
            defs.append(f'<marker id="m-triangulo" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="13" markerHeight="13" orient="auto-start-reverse"><path d="M0 0 L12 6 L0 12 z" fill="#FFFFFF" stroke="{LINHA}" stroke-width="1.2"/></marker>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
                f'<defs>{"".join(defs)}</defs><rect width="100%" height="100%" fill="#FFFFFF"/>'
                + "".join(self.partes) + "</svg>")


def legenda_c4(d, x, y, itens=None):
    """Legenda das cores C4, em uma linha horizontal (ocupa 20 px de altura)."""
    itens = itens or [("Pessoa", C4_PESSOA), ("Sistema do Rufus", C4_SISTEMA), ("Container", C4_CONTAINER),
                      ("Componente", C4_COMPONENTE), ("Sistema externo", C4_EXTERNO)]
    d.texto(x, y + 12, "Legenda:", tam=12, peso="700", ancora="start")
    xx = x + 66
    for nome, (f, b, _) in itens:
        d.partes.append(f'<rect x="{xx}" y="{y}" width="16" height="14" rx="3" fill="{f}" stroke="{b}"/>')
        d.texto(xx + 22, y + 12, nome, tam=11.5, ancora="start")
        xx += 22 + len(nome) * 6.6 + 22
