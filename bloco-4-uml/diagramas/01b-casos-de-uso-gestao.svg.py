# titulo: Diagrama de Casos de Uso, parte 2 de 2 · responsável legal, SAC, antifraude e administração
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1000, 660)
CX, RX, RY, T = 500, 125, 26, 14

d.partes.append('<rect x="290" y="30" width="420" height="610" fill="#FFFFFF" stroke="#374151" stroke-width="1.5"/>')
d.texto(500, 60, "Rufus Bank", tam=16, peso="700")

C = {
    "decidir": (110, ["Decidir pedido", "de aprovação"]), "aceitar": (180, ["Aceitar vínculo", "do menor"]),
    "limites": (250, ["Definir limites", "do menor"]),
    "responder": (370, ["Responder chamado"]), "analisar": (480, ["Analisar Pix retido"]),
    "funcionario": (590, ["Cadastrar funcionário"]),
}
for y, l in C.values(): d.caso(CX, y, RX, RY, l, tam=T)
def esq(k): return (CX - RX, C[k][0])
def dir_(k): return (CX + RX, C[k][0])

d.ator(140, 150, ["Responsável", "legal"], tam=14)
for k in ("decidir", "aceitar", "limites"):
    d.linha([(158, 180), esq(k)])
d.texto(140, 320, ["O pedido vem do caso", "Pedir aprovação ao", "responsável (parte 1)"], tam=12, cor="#4B5563")

d.ator(860, 335, ["Atendente", "do SAC"], tam=14); d.linha([(843, 365), dir_("responder")])
d.ator(860, 445, ["Analista", "antifraude"], tam=14); d.linha([(843, 475), dir_("analisar")])
d.ator(860, 555, ["Administrador"], tam=14); d.linha([(843, 585), dir_("funcionario")])
print(d.svg())
