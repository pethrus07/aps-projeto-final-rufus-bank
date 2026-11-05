# titulo: Diagrama de Casos de Uso · Rufus Bank
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1360, 1400)
AX, BX, RX, RY = 470, 830, 112, 25   # centros das colunas A e B, raios das elipses

d.partes.append('<rect x="300" y="60" width="680" height="1310" fill="#FFFFFF" stroke="#374151" stroke-width="1.5"/>')
d.texto(640, 88, "Rufus Bank", tam=15, peso="700")

A = {  # casos do cliente (coluna A)
    "entrar": (130, ["Entrar no app"]), "saldo": (195, ["Ver saldo e extrato"]),
    "chaves": (260, ["Gerenciar chaves Pix"]), "meta": (325, ["Criar meta de economia"]),
    "pix": (400, ["Enviar Pix"]), "receber": (475, ["Receber Pix"]), "boleto": (545, ["Pagar boleto"]),
    "abrir": (615, ["Abrir conta"]), "trocar": (685, ["Trocar de celular"]),
    "bloquear": (755, ["Bloquear tudo agora"]), "contato": (825, ["Cadastrar contato", "de confiança"]),
    "chat": (895, ["Falar com atendente"]), "dados": (965, ["Baixar dados e", "encerrar conta"]),
}
B = {  # casos incluídos, extensões e casos dos outros atores (coluna B)
    "ouvir": (130, ["Ouvir a tela"]), "avisar": (240, ["Avisar contato", "de confiança"]),
    "pedir": (310, ["Pedir aprovação", "ao responsável"]), "confirmar": (400, ["Confirmar recebedor", "por voz"]),
    "risco": (470, ["Avaliar risco", "do Pix"]), "liquidar": (545, ["Liquidar no", "parceiro"]),
    "validar": (615, ["Validar identidade"]),
    "decidir": (755, ["Decidir pedido", "de aprovação"]), "aceitar": (825, ["Aceitar vínculo", "do menor"]),
    "limites": (895, ["Definir limites", "do menor"]),
    "responder": (1010, ["Responder chamado"]), "analisar": (1135, ["Analisar Pix retido"]),
    "funcionario": (1260, ["Cadastrar funcionário"]),
}
for y, l in A.values(): d.caso(AX, y, RX, RY, l)
for y, l in B.values(): d.caso(BX, y, RX, RY, l)

def esq(col, k):  # ponto da borda esquerda da elipse
    y = (A if col == "A" else B)[k][0]; return ((AX if col == "A" else BX) - RX, y)
def dir_(col, k):
    y = (A if col == "A" else B)[k][0]; return ((AX if col == "A" else BX) + RX, y)

def rel(base, alvo, tipo):
    """include: base (A) -> alvo (B). extend: extensão (B) -> base (A)."""
    if tipo == "include":
        p0, p1 = dir_("A", base), esq("B", alvo)
        d.seta([p0, p1], tracejada=True, ponta="aberta")
    else:
        p0, p1 = esq("B", alvo), dir_("A", base)
        d.seta([p0, p1], tracejada=True, ponta="aberta")
    return p0, p1

def rot(x, y, t): d.rotulo(x, y, [t], tam=10.5, cor="#374151")

# extend (seta da extensão para o caso base)
rel("saldo", "ouvir", "extend"); rot(650, 157, "«extend»")
rel("pix", "avisar", "extend"); rot(650, 300, "«extend»")
rel("pix", "pedir", "extend"); rot(675, 345, "«extend»")
# include (seta do caso base para o incluído)
rel("pix", "confirmar", "include"); rot(650, 396, "«include»")
rel("pix", "risco", "include"); rot(675, 440, "«include»")
rel("pix", "liquidar", "include"); rot(745, 505, "«include»")
rel("receber", "liquidar", "include"); rot(640, 498, "«include»")
rel("boleto", "liquidar", "include"); rot(650, 562, "«include»")
rel("abrir", "validar", "include"); rot(650, 632, "«include»")
rel("trocar", "validar", "include"); rot(650, 668, "«include»")
d.texto(830, 365 - 15, "", tam=1)

# ator Cliente (abstrato) e especializações
d.ator(150, 470, ["Cliente"])
for k in A:
    y = A[k][0]
    d.linha([(168, 500), (AX - RX, y)])
d.ator(95, 1080, ["Cliente", "titular"])
d.ator(215, 1080, ["Cliente", "menor"])
d.generalizacao([(95, 1080), (95, 1040), (140, 1040), (140, 595)])
d.generalizacao([(215, 1080), (215, 1040), (160, 1040), (160, 595)])
d.texto(150, 1200, ["Generalização: titular e", "menor são tipos de Cliente"], tam=10.5, cor="#4B5563")

# atores à direita
def assoc(pt, k): d.linha([pt, dir_("B", k)])
d.ator_sistema(1060, 96, 190, 58, ["Serviço de voz"]); assoc((1060, 128), "ouvir")
d.ator(1155, 196, ["Contato de", "confiança"]); assoc((1138, 230), "avisar")
d.ator_sistema(1060, 300, 190, 58, ["Serviço de notificação"]); assoc((1060, 322), "avisar")
d.ator_sistema(1060, 520, 190, 58, ["Parceiro BaaS"])
assoc((1060, 545), "liquidar"); assoc((1060, 566), "validar")
d.ator(1155, 760, ["Responsável", "legal"])
for k in ("decidir", "aceitar", "limites"): assoc((1138, 790), k)
d.ator(1155, 975, ["Atendente", "do SAC"]); assoc((1138, 1005), "responder")
d.ator(1155, 1100, ["Analista", "antifraude"]); assoc((1138, 1130), "analisar")
d.ator(1155, 1225, ["Administrador"]); assoc((1138, 1255), "funcionario")
print(d.svg())
