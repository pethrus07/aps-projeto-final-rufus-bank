"""Elementos de BPMN 2.0 (notação da OMG) sobre o svglib.

Pool e raia com o nome na faixa vertical; tarefa com cantos arredondados;
evento = círculo (início com borda fina, fim com borda grossa, intermediário
com borda dupla); gateway = losango (X exclusivo, + paralelo, círculo com
pentágono para "baseado em evento"); fluxo de sequência contínuo com seta
cheia; fluxo de mensagem tracejado, com círculo vazado na origem e seta
vazada no destino.

Uso em um script .svg.py:
    import svglib as s, bpmn as b
    d = s.Desenho(w, h)
    b.pool(d, ...); b.tarefa(d, ...); b.fluxo(d, [...]); b.mensagem(d, [...])
    print(d.svg())
"""

import math

from svglib import FONTE, esc

TINTA = "#1F2937"
MSG = "#334155"


def _vertical(d, x, y, h, nome, tam):
    d.partes.append(
        f'<text x="{x}" y="{y + h / 2}" font-family="{FONTE}" font-size="{tam}" font-weight="700" fill="#111827" '
        f'text-anchor="middle" transform="rotate(-90 {x} {y + h / 2})">{esc(nome)}</text>')


def pool(d, x, y, w, h, nome, faixa=34):
    d.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.6"/>')
    d.partes.append(f'<rect x="{x}" y="{y}" width="{faixa}" height="{h}" fill="#E2E8F0" stroke="{TINTA}" stroke-width="1.6"/>')
    _vertical(d, x + faixa / 2 + 5, y, h, nome, 13.5)


def raia(d, x, y, w, h, nome, faixa=30):
    d.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.1"/>')
    d.partes.append(f'<rect x="{x}" y="{y}" width="{faixa}" height="{h}" fill="#F1F5F9" stroke="{TINTA}" stroke-width="1.1"/>')
    _vertical(d, x + faixa / 2 + 4, y, h, nome, 12)


def tarefa(d, cx, cy, linhas, w=150, h=68, tipo=None):
    """tipo: None, 'usuario' (feita por pessoa), 'servico' (feita pelo sistema)."""
    x, y = cx - w / 2, cy - h / 2
    d.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.5"/>')
    if isinstance(linhas, str):
        linhas = [linhas]
    al = 16
    y0 = cy + 5 - (len(linhas) - 1) * al / 2 + (3 if tipo else 0)
    d.texto(cx, y0, linhas, tam=13, altura_linha=al)
    if tipo == "usuario":
        ix, iy = x + 8, y + 6
        d.partes.append(f'<circle cx="{ix + 5}" cy="{iy + 4}" r="3.2" fill="none" stroke="#374151" stroke-width="1.1"/>'
                        f'<path d="M{ix} {iy + 14} Q{ix + 5} {iy + 5} {ix + 10} {iy + 14} Z" fill="none" stroke="#374151" stroke-width="1.1"/>')
    elif tipo == "servico":
        ix, iy = x + 13, y + 12
        d.partes.append(f'<circle cx="{ix}" cy="{iy}" r="5.5" fill="none" stroke="#374151" stroke-width="2" stroke-dasharray="2.4 1.8"/>'
                        f'<circle cx="{ix}" cy="{iy}" r="2.2" fill="none" stroke="#374151" stroke-width="1.1"/>')


def _envelope(d, cx, cy, cheio):
    w, h = 14, 10
    x, y = cx - w / 2, cy - h / 2
    fundo, risco = ("#1F2937", "#FFFFFF") if cheio else ("#FFFFFF", "#1F2937")
    d.partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fundo}" stroke="#1F2937" stroke-width="1"/>'
                    f'<path d="M{x} {y} L{cx} {cy + 1} L{x + w} {y}" fill="none" stroke="{risco}" stroke-width="1"/>')


def evento(d, cx, cy, tipo="inicio", rotulo=None, lado="baixo", r=17):
    """tipo: inicio, inicio_msg, fim, fim_msg, terminar, msg (intermediário de captura), tempo,
    link_envia e link_recebe (evento de link: continua em outra parte do diagrama)."""
    if tipo in ("inicio", "inicio_msg"):
        d.partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.7"/>')
    elif tipo in ("fim", "fim_msg", "terminar"):
        d.partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{TINTA}" stroke-width="4"/>')
    else:
        d.partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.4"/>'
                        f'<circle cx="{cx}" cy="{cy}" r="{r - 3.5}" fill="none" stroke="{TINTA}" stroke-width="1.2"/>')
    if tipo in ("inicio_msg", "msg"):
        _envelope(d, cx, cy, cheio=False)
    elif tipo == "fim_msg":
        _envelope(d, cx, cy, cheio=True)
    elif tipo == "terminar":
        d.partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 7.5}" fill="{TINTA}"/>')
    elif tipo in ("link_envia", "link_recebe"):
        cheio = tipo == "link_envia"
        pts = [(cx - 7, cy - 3.5), (cx + 1, cy - 3.5), (cx + 1, cy - 8), (cx + 8, cy), (cx + 1, cy + 8), (cx + 1, cy + 3.5), (cx - 7, cy + 3.5)]
        d.partes.append(f'<polygon points="{" ".join(f"{a},{b_}" for a, b_ in pts)}" fill="{TINTA if cheio else "#FFFFFF"}" stroke="{TINTA}" stroke-width="1.1"/>')
    elif tipo == "tempo":
        rr = r - 6
        d.partes.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.1"/>'
                        f'<path d="M{cx} {cy - rr + 2} V{cy} L{cx + rr - 3} {cy}" fill="none" stroke="{TINTA}" stroke-width="1.2"/>')
    if rotulo:
        if isinstance(rotulo, str):
            rotulo = [rotulo]
        if lado == "baixo":
            d.texto(cx, cy + r + 16, rotulo, tam=12, cor="#111827", altura_linha=14)
        elif lado == "cima":
            d.texto(cx, cy - r - 8 - (len(rotulo) - 1) * 14, rotulo, tam=12, cor="#111827", altura_linha=14)
        elif lado == "dir":
            d.texto(cx + r + 6, cy + 4 - (len(rotulo) - 1) * 7, rotulo, tam=12, cor="#111827", ancora="start", altura_linha=14)
        else:
            d.texto(cx - r - 6, cy + 4 - (len(rotulo) - 1) * 7, rotulo, tam=12, cor="#111827", ancora="end", altura_linha=14)


def gateway(d, cx, cy, tipo="x", rotulo=None, lado="cima", t=22):
    """tipo: x (exclusivo), + (paralelo), evento (baseado em evento)."""
    d.partes.append(f'<path d="M{cx} {cy - t} L{cx + t} {cy} L{cx} {cy + t} L{cx - t} {cy} Z" fill="#FFFFFF" stroke="{TINTA}" stroke-width="1.6"/>')
    if tipo == "x":
        k = t * 0.32
        d.partes.append(f'<path d="M{cx - k} {cy - k} L{cx + k} {cy + k} M{cx + k} {cy - k} L{cx - k} {cy + k}" stroke="{TINTA}" stroke-width="2.6"/>')
    elif tipo == "+":
        k = t * 0.42
        d.partes.append(f'<path d="M{cx} {cy - k} V{cy + k} M{cx - k} {cy} H{cx + k}" stroke="{TINTA}" stroke-width="2.8"/>')
    elif tipo == "evento":
        d.partes.append(f'<circle cx="{cx}" cy="{cy}" r="{t * 0.5}" fill="none" stroke="{TINTA}" stroke-width="1.1"/>'
                        f'<circle cx="{cx}" cy="{cy}" r="{t * 0.39}" fill="none" stroke="{TINTA}" stroke-width="1.1"/>')
        pts = []
        for i in range(5):
            a = -math.pi / 2 + i * 2 * math.pi / 5
            pts.append(f"{cx + t * 0.24 * math.cos(a):.1f},{cy + t * 0.24 * math.sin(a):.1f}")
        d.partes.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{TINTA}" stroke-width="1.1"/>')
    if rotulo:
        if isinstance(rotulo, str):
            rotulo = [rotulo]
        if lado == "cima":
            d.texto(cx, cy - t - 8 - (len(rotulo) - 1) * 14, rotulo, tam=12.5, peso="700", cor="#111827", altura_linha=14)
        else:
            d.texto(cx, cy + t + 17, rotulo, tam=12.5, peso="700", cor="#111827", altura_linha=14)


def fluxo(d, pontos, rotulo=None, pos=None, ancora="start"):
    """Fluxo de sequência: linha contínua e seta cheia. Rótulo opcional em pos=(x, y)."""
    d.seta(pontos, ponta="cheia", cor=TINTA, largura=1.4)
    if rotulo:
        d.rotulo(pos[0], pos[1], rotulo if isinstance(rotulo, list) else [rotulo], tam=12, cor="#111827", ancora=ancora)


def mensagem(d, pontos, rotulo=None, pos=None, ancora="start"):
    """Fluxo de mensagem: tracejado, círculo vazado na origem e seta vazada no destino."""
    if "bpmn_msg" not in d.marcadores:
        d.marcadores.add("bpmn_msg")
        d.partes.insert(0,
            '<defs>'
            f'<marker id="b-msg-ini" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" markerHeight="9">'
            f'<circle cx="5" cy="5" r="3.6" fill="#FFFFFF" stroke="{MSG}" stroke-width="1.2"/></marker>'
            f'<marker id="b-msg-fim" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
            f'<path d="M0 0 L12 6 L0 12 z" fill="#FFFFFF" stroke="{MSG}" stroke-width="1.2"/></marker>'
            '</defs>')
    p = "M" + " L".join(f"{x} {y}" for x, y in pontos)
    d.partes.append(f'<path d="{p}" fill="none" stroke="{MSG}" stroke-width="1.3" stroke-dasharray="7 4" '
                    f'marker-start="url(#b-msg-ini)" marker-end="url(#b-msg-fim)"/>')
    if rotulo:
        d.rotulo(pos[0], pos[1], rotulo if isinstance(rotulo, list) else [rotulo], tam=11.5, cor=MSG, ancora=ancora)


def legenda(d, x, y, usados=None, largura=1250):
    """Legenda dos símbolos, em até duas linhas de no máximo ~1250 px.
    usados: lista de chaves (inicio, msg, tempo, fim, fim_msg, terminar, link, x, +, evento)."""
    catalogo = [
        ("inicio", "evento", "inicio", "início", 72), ("msg", "evento", "msg", "mensagem recebida", 160),
        ("tempo", "evento", "tempo", "tempo", 76), ("fim", "evento", "fim", "fim", 56),
        ("fim_msg", "evento", "fim_msg", "fim que envia mensagem", 196),
        ("terminar", "evento", "terminar", "fim que encerra o processo", 216),
        ("link", "evento", "link_envia", "continua na outra parte", 196),
        ("x", "gateway", "x", "decisão", 92), ("+", "gateway", "+", "paralelo", 96),
        ("evento", "gateway", "evento", "espera o 1º evento", 166),
    ]
    itens = [c for c in catalogo if usados is None or c[0] in usados]
    d.texto(x, y + 5, "Legenda:", tam=12.5, peso="700", ancora="start")
    xx, yy = x + 78, y
    for _, forma, tipo, nome, passo in itens:
        if xx + passo > x + largura:
            xx, yy = x + 78, yy + 30
        if forma == "evento":
            evento(d, xx, yy, tipo, r=10)
        else:
            gateway(d, xx, yy, tipo, t=12)
        d.texto(xx + 16, yy + 5, nome, tam=12, ancora="start")
        xx += passo
    if xx + 300 > x + largura:
        xx, yy = x + 78, yy + 30
    d.seta([(xx - 8, yy), (xx + 26, yy)], ponta="cheia", cor=TINTA, largura=1.4)
    d.texto(xx + 32, yy + 5, "sequência", tam=12, ancora="start")
    xx += 116
    mensagem(d, [(xx, yy), (xx + 40, yy)])
    d.texto(xx + 48, yy + 5, "mensagem", tam=12, ancora="start")
    return yy
