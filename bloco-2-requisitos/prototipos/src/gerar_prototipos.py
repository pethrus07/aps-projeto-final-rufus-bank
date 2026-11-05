"""Gera os protótipos do Rufus em três níveis (Aula 05 da disciplina).

Uma única descrição de cada tela vira três desenhos:
  - conceito   (sketch): traço de caneta, sem cor, só a ideia
  - baixa      (baixa fidelidade): preto e branco, caixas e símbolos
  - alta       (alta fidelidade): identidade do Rufus, Material Design

Assim o wireframe e a tela final nunca divergem de layout: o que muda é só o
acabamento. Cores e fontes saem de ferramentas/identidade/identidade.json;
autores e data de projeto.json.

Saída em bloco-2-requisitos/prototipos/img/:
  baixa-<tela>.png, alta-<tela>.png, conceito-<tela>.png (1 por tela, 720x1560)
  prancha-conceito.png, prancha-baixa.png, prancha-alta.png (todas as telas lado a lado)

Uso:  python -I bloco-2-requisitos/prototipos/src/gerar_prototipos.py
Precisa do Google Chrome (headless). Para com erro se algum PNG não sair.
"""

import html
import json
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
IMG = AQUI.parent / "img"
TMP = AQUI / "_html"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
W, H = 360, 780  # tela de celular em dp (1 dp = 1 px CSS)

ID = json.loads((RAIZ / "ferramentas/identidade/identidade.json").read_text(encoding="utf-8"))
PROJ = json.loads((RAIZ / "projeto.json").read_text(encoding="utf-8"))
C = {k: "#" + v for k, v in ID["cores"].items()}

# ------------------------------------------------------------------ ícones
# traços simples, 24x24, no estilo dos ícones do Material Design
ICONES = {
    "ouvir": '<path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "voltar": '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    "pix": '<path d="M12 2.5l9.5 9.5-9.5 9.5L2.5 12z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M8 12l4-4 4 4-4 4z"/>',
    "receber": '<rect x="3" y="3" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/><rect x="14" y="3" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="14" width="7" height="7" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 14h3v3h-3zM18 18h3v3h-3zM18 14h3M14 21h2"/>',
    "boleto": '<path d="M3 5v14M6 5v14M8.5 5v14M12 5v14M14 5v14M17 5v14M21 5v14" stroke="currentColor" stroke-width="1.8"/>',
    "extrato": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 8h6M9 12h6M9 16h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8 9.5h8M8 12.5h5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "cadeado": '<rect x="5" y="10.5" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="15.5" r="1.6"/>',
    "escudo": '<path d="M12 2.5l8 3v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10v-6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.5 12l2.5 2.5 4.5-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    "camera": '<path d="M4 7h3.5l1.5-2.5h6L16.5 7H20v12H4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.5" fill="none" stroke="currentColor" stroke-width="2"/>',
    "teclado": '<rect x="3" y="6" width="18" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6.5 10h1M10 10h1M13.5 10h1M17 10h1M8 14h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "meta": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="1.8"/>',
    "notebook": '<rect x="5" y="5" width="14" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M2.5 18.5h19" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
    "pessoa": '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2"/><path d="M4.5 20.5c1-4 4-6 7.5-6s6.5 2 7.5 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "microfone": '<rect x="9" y="3" width="6" height="11" rx="3" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
    "whatsapp": '<path d="M5 19l1.2-3.6A7.5 7.5 0 1 1 9 18.3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9.5 9.5c.3 2 1.8 3.6 4 4.5l1-1.2 1.8.9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "relogio": '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5.5l3.5 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    "inicio": '<path d="M3.5 11L12 4l8.5 7M6 9.5V20h12V9.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>',
    "alerta": '<path d="M12 3l10 18H2z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M12 10v5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="18" r="1.3"/>',
    "rufus": '<path d="M7.5 7.5C8.5 5 10 4 12 4s3.5 1 4.5 3.5V13c0 3.6-2 6.5-4.5 6.5S7.5 16.6 7.5 13z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 6.5C5.5 6 3.5 7.5 3.2 10.5c-.2 2 .6 3.6 2.3 4.3L7.5 12M16 6.5c2.5-.5 4.5 1 4.8 4 .2 2-.6 3.6-2.3 4.3L16.5 12"/><circle cx="10.2" cy="10.6" r="1.15"/><circle cx="13.8" cy="10.6" r="1.15"/><path d="M10.4 14.2h3.2l-1.6 1.9z"/><path d="M12 16.1v1.2" stroke="currentColor" stroke-width="1.4"/>',
}


def ic(nome, modo, tam=24, cls=""):
    """Ícone real na alta fidelidade e no conceito; caixa com X na baixa fidelidade."""
    if modo == "baixa":
        return (f'<span class="ic ph {cls}" style="width:{tam}px;height:{tam}px"><svg viewBox="0 0 24 24" '
                f'width="{tam}" height="{tam}"><rect x="2" y="2" width="20" height="20" fill="none" '
                f'stroke="currentColor" stroke-width="1.6"/><path d="M2 2l20 20M22 2L2 22" stroke="currentColor" '
                f'stroke-width="1.2"/></svg></span>')
    return (f'<span class="ic {cls}"><svg viewBox="0 0 24 24" width="{tam}" height="{tam}" fill="currentColor">'
            f'{ICONES[nome]}</svg></span>')


def e(t):
    return html.escape(t).replace("R$ ", "R$&nbsp;")


# ------------------------------------------------------------------ peças
def barra_status(modo):
    return ('<div class="status"><span>14:12</span><span class="st-dir">'
            '<i class="sig"></i><i class="sig s2"></i><i class="sig s3"></i><i class="bat"></i></span></div>')


def barra_topo(titulo, modo, voltar=True, escura=False):
    v = f'<button class="tb-btn" aria-label="Voltar">{ic("voltar", modo)}</button>' if voltar else \
        f'<span class="logo">{ic("rufus", modo, 28, "logo-ic")}<b>Rufus</b></span>'
    tit = f'<h1 class="tb-tit">{e(titulo)}</h1>' if titulo else '<span class="tb-tit"></span>'
    return (f'<header class="topo{" escura" if escura else ""}">{v}{tit}'
            f'<button class="ouvir">{ic("ouvir", modo, 22)}<span>Ouvir</span></button></header>')


def aviso_nunca_liga(modo, curto=True):
    txt = "O Rufus nunca liga para você." if curto else \
        "O Rufus nunca liga pedindo senha, código ou para mandar dinheiro. Se alguém ligou, desligue."
    return f'<div class="aviso">{ic("escudo", modo, 22)}<span>{e(txt)}</span></div>'


def botao(texto, modo, tipo="primario", icone=None):
    i = ic(icone, modo, 24) if icone else ""
    return f'<button class="btn {tipo}">{i}<span>{e(texto)}</span></button>'


# ------------------------------------------------------------------ telas
def tela_inicio(m):
    tiles = [("pix", "Mandar Pix"), ("receber", "Receber"), ("boleto", "Pagar conta"), ("extrato", "Ver extrato")]
    grade = "".join(f'<button class="tile"><span class="circ">{ic(i, m, 28)}</span><b>{e(t)}</b></button>'
                    for i, t in tiles)
    return f"""
    {barra_topo("", m, voltar=False)}
    <main class="conteudo">
      <p class="ola">Olá, Antônio</p>
      <section class="saldo">
        <span class="rot">Dinheiro que você tem</span>
        <span class="valor">R$ 412,50</span>
        <button class="ouvir-grande">{ic("ouvir", m, 24)}<span>Ouvir o saldo</span></button>
      </section>
      <div class="grade">{grade}</div>
      <div class="ultimo">{ic("check", m, 20, "ok")}<span>Recebeu <b>R$ 150,00</b> de Carlos Mendes, hoje</span></div>
      <div class="linha-btns">
        <button class="btn secundario meio">{ic("chat", m, 22)}<span>Falar com uma pessoa</span></button>
        <button class="btn perigo-contorno meio">{ic("cadeado", m, 22)}<span>Bloquear tudo</span></button>
      </div>
      {aviso_nunca_liga(m)}
    </main>"""


def tela_pix_confirmar(m):
    return f"""
    {barra_topo("Confira antes de mandar", m)}
    <main class="conteudo">
      <div class="falando">{ic("ouvir", m, 20)}<span>Lendo em voz alta: para quem vai e quanto</span></div>
      <section class="cartao destaque">
        <span class="rot">Vai mandar</span>
        <span class="valor">R$ 120,00</span>
        <hr>
        <div class="par"><span class="rot">Para</span><b>Maria das Graças Lima</b></div>
        <div class="par"><span class="rot">Banco</span><b>Caixa Econômica Federal</b></div>
        <div class="par"><span class="rot">CPF</span><b>***.456.789-**</b></div>
      </section>
      <div class="nota">{ic("alerta", m, 22)}<span>Primeira vez que você manda para esta pessoa. Até amanhã, o limite é de <b>R$ 300,00</b> por Pix.</span></div>
      <div class="espaco"></div>
      {botao("Mandar com a digital", m, "primario", "check")}
      {botao("Voltar e corrigir", m, "secundario")}
      {aviso_nunca_liga(m)}
    </main>"""


def tela_pix_enviado(m):
    return f"""
    {barra_topo("Pix enviado", m)}
    <main class="conteudo centro">
      <div class="selo-ok">{ic("check", m, 56)}</div>
      <p class="grande">Pronto! O Pix foi enviado.</p>
      <section class="cartao">
        <div class="par"><span class="rot">Valor</span><b>R$ 120,00</b></div>
        <div class="par"><span class="rot">Para</span><b>Maria das Graças Lima</b></div>
        <div class="par"><span class="rot">Quando</span><b>04/11/2026, 14:12</b></div>
      </section>
      <div class="espaco"></div>
      {botao("Ouvir o comprovante", m, "secundario", "ouvir")}
      {botao("Mandar pelo WhatsApp", m, "secundario", "whatsapp")}
      {botao("Voltar ao início", m, "primario", "inicio")}
    </main>"""


def tela_boleto(m):
    return f"""
    {barra_topo("Pagar conta", m, escura=True)}
    <main class="conteudo camera">
      <p class="instr">Aponte a câmera para o código de barras</p>
      <div class="visor"><div class="mira">{ic("boleto", m, 64)}</div><span class="lido">Código lido</span></div>
      <section class="cartao folha">
        <div class="par"><span class="rot">Conta de luz</span><b>Distribuidora de Energia</b></div>
        <div class="par"><span class="rot">Vence em</span><b>10/11/2026</b></div>
        <div class="valor-linha"><span class="rot">Total</span><span class="valor">R$ 187,43</span></div>
        {botao("Pagar com a digital", m, "primario", "check")}
        <button class="link">{ic("teclado", m, 22)}<span>Prefiro digitar o código</span></button>
      </section>
    </main>"""


def tela_camila(m):
    return f"""
    {barra_topo("", m, voltar=False)}
    <main class="conteudo">
      <p class="ola">Olá, Camila</p>
      <section class="saldo compacto">
        <span class="rot">Dinheiro que você tem</span>
        <span class="valor">R$ 236,00</span>
      </section>
      <section class="cartao meta">
        <div class="meta-topo">{ic("notebook", m, 40, "foto")}<div><b class="meta-nome">Meu notebook</b><span class="rot">Meta para 31/03/2027</span></div></div>
        <div class="barra"><i style="width:37%"></i></div>
        <div class="par"><span><b>R$ 1.180,00</b> de R$ 3.200,00</span><b>37%</b></div>
        <span class="rot">Faltam R$ 2.020,00</span>
        {botao("Guardar na meta", m, "primario", "meta")}
      </section>
      <section class="cartao limite">
        <div class="par"><span class="rot">Ainda pode gastar hoje</span><b>R$ 20,00</b></div>
        <div class="barra fina"><i style="width:60%"></i></div>
        <span class="rot">Já usou R$ 30,00 do limite de R$ 50,00 por dia, combinado com seu pai, Sérgio</span>
        <button class="btn secundario">{ic("pessoa", m, 22)}<span>Pedir para liberar mais</span></button>
      </section>
    </main>"""


def tela_responsavel(m):
    return f"""
    {barra_topo("Pedido da Camila", m)}
    <main class="conteudo">
      <div class="falando">{ic("pessoa", m, 20)}<span>Você é o responsável pela conta da Camila</span></div>
      <section class="cartao destaque">
        <span class="rot">Camila pediu para liberar</span>
        <span class="valor">R$ 120,00</span>
        <hr>
        <div class="par"><span class="rot">Para</span><b>Papelaria Central</b></div>
        <div class="par col"><span class="rot">O que ela escreveu</span><b>"Material do curso de aprendiz"</b></div>
      </section>
      <div class="nota">{ic("alerta", m, 22)}<span>Passa do limite de hoje, que é de <b>R$ 50,00</b>.</span></div>
      <div class="nota neutra">{ic("relogio", m, 22)}<span>Responda até amanhã, 14:12. Depois disso o pedido é cancelado.</span></div>
      <div class="espaco"></div>
      {botao("Aprovar", m, "sucesso", "check")}
      {botao("Recusar", m, "secundario")}
    </main>"""


def tela_bloquear(m):
    return f"""
    {barra_topo("Bloquear tudo", m)}
    <main class="conteudo centro">
      <div class="selo-perigo">{ic("cadeado", m, 56)}</div>
      <p class="grande">Bloquear tudo agora?</p>
      <p class="texto">Nenhum dinheiro vai sair da sua conta. Você continua podendo receber.</p>
      <p class="texto">Seu neto <b>Lucas</b> vai receber um aviso.</p>
      <div class="aviso forte">{ic("escudo", m, 26)}<span>O Rufus nunca liga pedindo senha, código ou para mandar dinheiro. Se alguém ligou, desligue.</span></div>
      <div class="espaco"></div>
      {botao("Sim, bloquear tudo", m, "perigo", "cadeado")}
      {botao("Não, voltar", m, "secundario")}
      <p class="rodape">Para desbloquear depois: selfie e 1 hora de espera.</p>
    </main>"""


def tela_chat(m):
    return f"""
    {barra_topo("Falar com uma pessoa", m)}
    <main class="conteudo chat">
      <div class="aviso">{ic("escudo", m, 22)}<span>Você está falando com o Rufus de verdade. A conversa começou dentro do app.</span></div>
      <div class="msg dela"><b class="quem">Juliana, do Rufus</b>Oi, Antônio! Já sei quem você é. Não precisa dizer senha nem código. Como posso ajudar?</div>
      <div class="msg minha audio">{ic("ouvir", m, 22)}<span class="onda"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span><span>0:12</span></div>
      <div class="msg dela"><b class="quem">Juliana, do Rufus</b>O Pix de ontem para o José foi concluído às 18:40. Quer ouvir o comprovante?</div>
      <div class="espaco"></div>
      <div class="entrada"><span class="campo">Escrever</span><button class="mic">{ic("microfone", m, 30)}</button></div>
      <p class="rodape">Segure o microfone para mandar áudio</p>
    </main>"""


TELAS = [
    ("01-inicio", "Início com saldo e Ouvir", tela_inicio),
    ("02-pix-confirmar", "Enviar Pix: confirmação falada", tela_pix_confirmar),
    ("03-pix-enviado", "Pix enviado e comprovante", tela_pix_enviado),
    ("04-boleto-camera", "Pagar conta pela câmera", tela_boleto),
    ("05-conta-camila", "Conta da Camila: meta e limite", tela_camila),
    ("06-responsavel", "Responsável aprova o pedido", tela_responsavel),
    ("07-bloquear-tudo", "Bloquear tudo agora", tela_bloquear),
    ("08-falar-com-pessoa", "Falar com uma pessoa", tela_chat),
]

# ------------------------------------------------------------------ estilos
BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:360px;height:780px;overflow:hidden}
body{font-family:Roboto,Arial,Helvetica,sans-serif;font-size:18px;line-height:1.35;-webkit-font-smoothing:antialiased}
button{font:inherit;border:0;background:none;color:inherit}
.tela{width:360px;height:780px;display:flex;flex-direction:column;position:relative;overflow:hidden}
.status{height:28px;display:flex;justify-content:space-between;align-items:center;padding:0 18px;font-size:13px;font-weight:700}
.st-dir{display:flex;gap:3px;align-items:flex-end}
.sig{display:inline-block;width:4px;height:6px;background:currentColor;border-radius:1px}.s2{height:9px}.s3{height:12px}
.bat{display:inline-block;width:20px;height:10px;border:2px solid currentColor;border-radius:3px;margin-left:6px}
.topo{height:64px;display:flex;align-items:center;gap:6px;padding:0 18px 0 6px}
.tb-btn{width:48px;height:48px;display:flex;align-items:center;justify-content:center;border-radius:24px}
.tb-tit{flex:1;font-size:20px;font-weight:700;line-height:1.2;padding-left:2px}
.logo{display:flex;align-items:center;gap:8px;flex:0 0 auto;padding-left:10px;font-size:22px}
.logo + .tb-tit{flex:1}
.ouvir{height:48px;padding:0 16px 0 12px;border-radius:24px;display:flex;align-items:center;gap:6px;font-weight:700;font-size:17px}
.ic{display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto}
.conteudo{flex:1;display:flex;flex-direction:column;gap:14px;padding:6px 18px 18px}
.centro{align-items:stretch;text-align:center}
.ola{font-size:22px;font-weight:700;margin-top:2px}
.rot{font-size:16px}
.valor{font-size:40px;font-weight:700;line-height:1.1;letter-spacing:-.5px}
.saldo{border-radius:12px;padding:18px 18px 16px;display:flex;flex-direction:column;gap:6px}
.saldo.compacto{padding:14px 18px}
.saldo.compacto .valor{font-size:34px}
.ouvir-grande{margin-top:8px;height:52px;border-radius:26px;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:700}
.grade{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tile{height:112px;border-radius:12px;display:flex;flex-direction:column;align-items:flex-start;justify-content:space-between;padding:14px;text-align:left}
.tile b{font-size:18px}
.circ{width:48px;height:48px;border-radius:24px;display:flex;align-items:center;justify-content:center}
.ultimo{display:flex;align-items:center;gap:10px;font-size:16px;padding:12px 14px;border-radius:12px}
.linha-btns{display:flex;gap:10px}
.btn{min-height:56px;width:100%;border-radius:14px;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:700;font-size:18px;padding:0 14px}
.btn.meio{font-size:16px;line-height:1.15;padding:6px 10px;gap:6px}
.aviso{display:flex;align-items:center;gap:10px;font-size:16px;padding:12px 14px;border-radius:12px;text-align:left}
.aviso.forte{font-size:17px;font-weight:700;padding:14px}
.falando{display:flex;align-items:center;gap:8px;font-size:15px;padding:8px 12px;border-radius:20px;align-self:flex-start}
.cartao{border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:10px;text-align:left}
.cartao hr{border:0;height:1px;margin:2px 0}
.par{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.par b{text-align:right}
.par.col{flex-direction:column;align-items:flex-start;gap:2px}.par.col b{text-align:left}
.nota{display:flex;gap:10px;align-items:flex-start;font-size:16px;padding:12px 14px;border-radius:12px;text-align:left}
.espaco{flex:1}
.selo-ok,.selo-perigo{width:96px;height:96px;border-radius:48px;display:flex;align-items:center;justify-content:center;align-self:center;margin-top:10px}
.grande{font-size:24px;font-weight:700;line-height:1.25}
.texto{font-size:18px}
.rodape{font-size:15px;text-align:center}
.camera{padding:0;gap:0}
.instr{font-size:18px;font-weight:700;text-align:center;padding:10px 18px 12px}
.visor{flex:1;position:relative;display:flex;align-items:center;justify-content:center}
.mira{width:270px;height:150px;border-radius:12px;display:flex;align-items:center;justify-content:center}
.lido{position:absolute;bottom:18px;left:50%;transform:translateX(-50%);font-size:15px;font-weight:700;padding:6px 14px;border-radius:16px}
.folha{border-radius:20px 20px 0 0;padding:18px 18px 16px;gap:10px}
.valor-linha{display:flex;justify-content:space-between;align-items:baseline}
.valor-linha .valor{font-size:32px}
.link{height:48px;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:700;font-size:17px}
.meta-topo{display:flex;gap:12px;align-items:center}
.foto{width:64px;height:64px;border-radius:12px}
.meta-nome{display:block;font-size:20px}
.barra{height:14px;border-radius:7px;overflow:hidden}.barra i{display:block;height:100%;border-radius:7px}
.barra.fina{height:10px}
.chat{gap:12px}
.msg{max-width:86%;padding:12px 14px;border-radius:16px;font-size:17px;text-align:left}
.msg .quem{display:block;font-size:14px;margin-bottom:4px}
.msg.dela{align-self:flex-start;border-bottom-left-radius:4px}
.msg.minha{align-self:flex-end;border-bottom-right-radius:4px}
.audio{display:flex;align-items:center;gap:10px}
.onda{display:flex;gap:3px;align-items:center}.onda i{display:block;width:4px;border-radius:2px;height:10px}
.onda i:nth-child(2n){height:20px}.onda i:nth-child(3n){height:15px}
.entrada{display:flex;gap:10px;align-items:center}
.campo{flex:1;height:56px;border-radius:28px;display:flex;align-items:center;padding:0 20px;font-size:17px}
.mic{width:72px;height:72px;border-radius:36px;display:flex;align-items:center;justify-content:center}
"""

ALTA = f"""
body{{background:{C['fundo']};color:{C['texto']}}}
.status{{color:{C['texto']}}}
.topo.escura,.camera .instr,.visor{{background:#151112;color:#FFFFFF}}
.topo.escura + .conteudo .instr{{color:#FFFFFF}}
.tb-btn{{color:{C['grafite']}}}.topo.escura .tb-btn{{color:#FFFFFF}}
.logo b{{color:{C['vermelho']}}}
.logo-ic{{width:40px;height:40px;border-radius:20px;background:{C['vermelho']};color:#FFFFFF}}
.ouvir{{background:{C['vermelho']};color:#FFFFFF}}
.rot{{color:{C['texto_2']}}}
.saldo{{background:{C['grafite']};color:#FFFFFF}}.saldo .rot{{color:#E4DCDD}}
.ouvir-grande{{background:{C['vermelho']};color:#FFFFFF}}
.tile{{background:{C['superficie']};color:{C['grafite']};border:1px solid {C['borda']}}}
.circ{{background:{C['vermelho_suave']};color:{C['vermelho']}}}
.ultimo{{background:{C['superficie']};color:{C['texto']}}}.ok{{color:{C['sucesso']}}}
.btn.primario{{background:{C['vermelho']};color:#FFFFFF}}
.btn.secundario{{background:#FFFFFF;color:{C['grafite']};border:2px solid {C['grafite']}}}
.btn.sucesso{{background:{C['sucesso']};color:#FFFFFF}}
.btn.perigo{{background:{C['perigo']};color:#FFFFFF}}
.btn.perigo-contorno{{background:#FFFFFF;color:{C['perigo']};border:2px solid {C['perigo']}}}
.aviso{{background:{C['vermelho_suave']};color:{C['grafite']}}}.aviso .ic{{color:{C['vermelho']}}}
.falando{{background:{C['vermelho_suave']};color:{C['grafite']}}}
.cartao{{background:#FFFFFF;border:1px solid {C['borda']}}}
.cartao.destaque{{background:{C['superficie']};border:0}}
.cartao hr{{background:{C['borda']}}}
.nota{{background:#FDF1E4;color:#6B3305}}.nota .ic{{color:{C['alerta']}}}
.nota.neutra{{background:{C['superficie']};color:{C['texto']}}}.nota.neutra .ic{{color:{C['texto_2']}}}
.selo-ok{{background:{C['sucesso']};color:#FFFFFF}}
.selo-perigo{{background:#FBE7E5;color:{C['perigo']}}}
.rodape{{color:{C['texto_2']}}}
.mira{{border:3px solid #FFFFFF;color:rgba(255,255,255,.85)}}
.lido{{background:{C['sucesso']};color:#FFFFFF}}
.folha{{border:0;box-shadow:0 -6px 20px rgba(0,0,0,.25)}}
.link{{color:{C['vermelho']}}}
.foto{{background:{C['vermelho_suave']};color:{C['vermelho']}}}
.barra{{background:{C['borda']}}}.barra i{{background:{C['sucesso']}}}
.limite .barra i{{background:{C['grafite']}}}
.msg.dela{{background:{C['superficie']};color:{C['texto']}}}.msg .quem{{color:{C['texto_2']}}}
.msg.minha{{background:{C['grafite']};color:#FFFFFF}}.onda i{{background:{C['vermelho_suave']}}}
.campo{{background:{C['superficie']};color:{C['texto_2']};border:1px solid {C['borda']}}}
.mic{{background:{C['vermelho']};color:#FFFFFF}}
"""

BAIXA = """
body{background:#FFFFFF;color:#1A1A1A}
.topo,.status{color:#1A1A1A}
.topo{border-bottom:1.5px solid #1A1A1A}
.ouvir,.ouvir-grande{border:1.5px solid #1A1A1A;background:#E6E6E6}
.saldo,.tile,.ultimo,.cartao,.aviso,.falando,.nota,.campo,.msg{border:1.5px solid #1A1A1A;background:#FFFFFF}
.cartao.destaque,.saldo{background:#F0F0F0}
.circ,.foto{border:1.5px dashed #1A1A1A}
.btn{border:1.5px solid #1A1A1A;background:#FFFFFF}
.btn.primario,.btn.sucesso,.btn.perigo{background:#1A1A1A;color:#FFFFFF}
.cartao hr{background:#1A1A1A}
.selo-ok,.selo-perigo,.mic{border:2px solid #1A1A1A}
.visor,.instr{background:#D9D9D9}
.mira{border:2px dashed #1A1A1A}
.lido{border:1.5px solid #1A1A1A;background:#FFFFFF}
.folha{border-top:2px solid #1A1A1A}
.barra{border:1.5px solid #1A1A1A;background:#FFFFFF}.barra i{background:#8C8C8C}
.onda i{background:#8C8C8C}
.logo-ic{width:40px;height:40px}
.rot,.rodape{color:#444}
"""

CONCEITO = """
body{background:#FFFDF6;color:#2A2A2A;font-family:'Segoe Print','Comic Sans MS',cursive;font-size:17px}
.valor{font-size:34px}
.topo{border-bottom:2px solid #2A2A2A}
.ouvir,.ouvir-grande,.saldo,.tile,.ultimo,.cartao,.aviso,.falando,.nota,.campo,.msg,.btn,.circ,.foto,.mira,.selo-ok,.selo-perigo,.mic,.barra,.lido{
  border:2px solid #2A2A2A;background:transparent;border-radius:255px 18px 225px 18px/18px 225px 18px 255px}
.btn.primario,.btn.sucesso,.btn.perigo{border-width:3px}
.cartao hr{background:#2A2A2A}
.visor,.instr{background:transparent}
.barra i{background:repeating-linear-gradient(45deg,#2A2A2A 0 2px,transparent 2px 7px)}
.onda i{background:#2A2A2A}
.status{opacity:.5}
"""

MODOS = {"alta": ALTA, "baixa": BAIXA, "conceito": CONCEITO}


def pagina_tela(fn, modo):
    corpo = fn(modo)
    corpo = corpo.replace("R$ ", "R$&nbsp;")
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{BASE}{MODOS[modo]}</style>'
            f'</head><body><div class="tela">{barra_status(modo)}{corpo}</div></body></html>')


def chrome_png(html_path, png_path, w, h, escala=2):
    if png_path.exists():
        png_path.unlink()
    cmd = [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", f"--force-device-scale-factor={escala}",
           f"--window-size={w},{h}", "--virtual-time-budget=3000", f"--screenshot={png_path}", html_path.as_uri()]
    subprocess.run(cmd, capture_output=True)
    if not png_path.exists():
        sys.exit(f"ABORTADO: PNG não gerado: {png_path}")


NOMES_NIVEL = {
    "conceito": ("Protótipo conceito (sketch)", "Traço de caneta: a primeira versão da solução, sem cor nem detalhe."),
    "baixa": ("Protótipo de baixa fidelidade (wireframe)", "Preto e branco, caixas e símbolos: valida layout, conteúdo e fluxo."),
    "alta": ("Protótipo de alta fidelidade", "Identidade do Rufus, Material Design, contraste WCAG AA e áreas de toque de 48 dp ou mais."),
}


def prancha(modo):
    titulo, sub = NOMES_NIVEL[modo]
    autores = ", ".join(m["nome"] for m in PROJ["equipe"])
    d = PROJ["data"].split("-")
    data_br = f"{d[2]}/{d[1]}/{d[0]}"
    cards = "".join(
        f'<figure><img src="{(IMG / f"{modo}-{slug}.png").as_uri()}" width="{W}" height="{H}">'
        f'<figcaption><b>{i + 1}</b> {e(nome)}</figcaption></figure>'
        for i, (slug, nome, _) in enumerate(TELAS))
    largura = 4 * W + 3 * 36 + 2 * 56
    altura = 150 + 2 * (H + 64) + 40
    fundo = "#FFFDF6" if modo == "conceito" else (C["superficie"] if modo == "alta" else "#F2F2F2")
    borda = "2px solid #2A2A2A" if modo != "alta" else f"1px solid {C['borda']}"
    pagina = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{largura}px;height:{altura}px;overflow:hidden}}
body{{background:{fundo};font-family:Arial,Helvetica,sans-serif;color:{C['texto']};padding:36px 56px}}
header{{height:110px}}
h1{{font-size:30px;font-weight:700}}
.sub{{font-size:17px;color:{C['texto_2']};margin-top:6px}}
.autoria{{font-size:14px;color:{C['texto_2']};margin-top:8px}}
.grade{{display:grid;grid-template-columns:repeat(4,{W}px);gap:28px 36px}}
figure{{display:flex;flex-direction:column;gap:12px}}
img{{display:block;border-radius:28px;border:{borda};box-shadow:0 10px 28px rgba(20,33,61,.12);background:#fff}}
figcaption{{font-size:17px;font-weight:700}}
figcaption b{{display:inline-flex;width:28px;height:28px;border-radius:14px;align-items:center;justify-content:center;
  background:{C['vermelho'] if modo == 'alta' else '#1A1A1A'};color:#fff;font-size:15px;margin-right:6px}}
</style></head><body>
<header><h1>{e(titulo)} · {e(PROJ['nome'])}</h1><div class="sub">{e(sub)}</div>
<div class="autoria">Autores: {e(autores)} · {data_br}</div></header>
<div class="grade">{cards}</div></body></html>"""
    caminho = TMP / f"prancha-{modo}.html"
    caminho.write_text(pagina, encoding="utf-8")
    chrome_png(caminho, IMG / f"prancha-{modo}.png", largura, altura, escala=1.5)
    return largura, altura


def main():
    IMG.mkdir(exist_ok=True)
    TMP.mkdir(exist_ok=True)
    for modo in ("conceito", "baixa", "alta"):
        for slug, _, fn in TELAS:
            h = TMP / f"{modo}-{slug}.html"
            h.write_text(pagina_tela(fn, modo), encoding="utf-8")
            chrome_png(h, IMG / f"{modo}-{slug}.png", W, H)
        w, hh = prancha(modo)
        print(f"ok  {modo}: 8 telas + prancha ({w}x{hh})")


if __name__ == "__main__":
    main()
