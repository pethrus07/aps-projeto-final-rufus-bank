# titulo: Diagrama de Casos de Uso, parte 1 de 2 · Cliente e sistemas externos
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1300, 900)
AX, BX, RX, RY, T = 470, 830, 118, 24, 14   # colunas A e B, raios das elipses, fonte

d.partes.append('<rect x="300" y="30" width="700" height="840" fill="#FFFFFF" stroke="#374151" stroke-width="1.5"/>')
d.texto(650, 60, "Rufus Bank", tam=16, peso="700")

A = {  # casos do cliente (coluna A), um a cada 60 px
    "entrar": (100, ["Entrar no app"]), "saldo": (160, ["Ver saldo e extrato"]),
    "chaves": (220, ["Gerenciar chaves Pix"]), "meta": (280, ["Criar meta de economia"]),
    "pix": (340, ["Enviar Pix"]), "receber": (400, ["Receber Pix"]), "boleto": (460, ["Pagar boleto"]),
    "abrir": (520, ["Abrir conta"]), "trocar": (580, ["Trocar de celular"]),
    "bloquear": (640, ["Bloquear tudo agora"]), "contato": (700, ["Cadastrar contato", "de confiança"]),
    "chat": (760, ["Falar com atendente"]), "dados": (820, ["Baixar dados e", "encerrar conta"]),
}
B = {  # casos incluídos e extensões (coluna B)
    "ouvir": (100, ["Ouvir a tela"]), "avisar": (220, ["Avisar contato", "de confiança"]),
    "pedir": (280, ["Pedir aprovação", "ao responsável"]), "confirmar": (340, ["Confirmar recebedor", "por voz"]),
    "risco": (400, ["Avaliar risco", "do Pix"]), "liquidar": (460, ["Liquidar no", "parceiro"]),
    "validar": (550, ["Validar identidade"]),
}
for y, l in A.values(): d.caso(AX, y, RX, RY, l, tam=T)
for y, l in B.values(): d.caso(BX, y, RX, RY, l, tam=T)

def esq(col, k):
    y = (A if col == "A" else B)[k][0]; return ((AX if col == "A" else BX) - RX, y)
def dir_(col, k):
    y = (A if col == "A" else B)[k][0]; return ((AX if col == "A" else BX) + RX, y)
def include(base, alvo): d.seta([dir_("A", base), esq("B", alvo)], tracejada=True, ponta="aberta")
def extend(base, ext): d.seta([esq("B", ext), dir_("A", base)], tracejada=True, ponta="aberta")
def rot(x, y, t): d.rotulo(x, y, [t], tam=12, cor="#374151")

# extend: a seta sai da extensão e aponta para o caso base
extend("saldo", "ouvir"); rot(668, 122, "«extend»")
extend("pix", "avisar"); rot(676, 256, "«extend»")
extend("pix", "pedir"); rot(690, 300, "«extend»")
# include: a seta sai do caso base e aponta para o incluído
include("pix", "confirmar"); rot(650, 334, "«include»")
include("pix", "risco"); rot(690, 381, "«include»")
include("pix", "liquidar"); rot(624, 373, "«include»")
include("receber", "liquidar"); rot(612, 432, "«include»")
include("boleto", "liquidar"); rot(650, 478, "«include»")
include("abrir", "validar"); rot(650, 527, "«include»")
include("trocar", "validar"); rot(650, 590, "«include»")

# ator Cliente (abstrato) e especializações
d.ator(150, 380, ["Cliente"], tam=14)
for k in A:
    d.linha([(168, 410), (AX - RX, A[k][0])])
d.ator(95, 640, ["Cliente", "titular"], tam=14)
d.ator(215, 640, ["Cliente", "menor"], tam=14)
d.generalizacao([(95, 640), (95, 610), (140, 610), (140, 500)])
d.generalizacao([(215, 640), (215, 610), (160, 610), (160, 500)])
d.texto(155, 780, ["Generalização: titular", "e menor são tipos", "de Cliente"], tam=12, cor="#4B5563")

# atores à direita (todos ligados a casos da coluna B)
def assoc(pt, k): d.linha([pt, dir_("B", k)])
d.ator_sistema(1060, 72, 200, 58, ["Serviço de voz"], tam=14); assoc((1060, 100), "ouvir")
d.ator(1160, 168, ["Contato de", "confiança"], tam=14); assoc((1143, 198), "avisar")
d.ator_sistema(1060, 290, 200, 58, ["Serviço de notificação"], tam=14); assoc((1060, 312), "avisar")
d.ator_sistema(1060, 470, 200, 58, ["Parceiro BaaS"], tam=14)
assoc((1060, 488), "liquidar"); assoc((1060, 512), "validar")
d.texto(1160, 610, ["Responsável, SAC,", "antifraude e", "administrador:", "parte 2"], tam=12, cor="#4B5563")
print(d.svg())
