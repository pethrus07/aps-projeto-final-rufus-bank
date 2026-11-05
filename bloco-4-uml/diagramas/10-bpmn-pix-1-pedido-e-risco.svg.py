# titulo: BPMN 2.0 · Envio de Pix, parte 1 de 2: do pedido à nota de risco
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s
import bpmn as b

d = s.Desenho(1350, 620)

b.pool(d, 20, 20, 1310, 140, "Cliente")
b.pool(d, 20, 190, 1310, 300, "Rufus Bank")
b.raia(d, 54, 190, 1276, 140, "App")
b.raia(d, 54, 330, 1276, 160, "API e worker")

# Cliente (y = 90)
b.evento(d, 100, 90, "inicio", ["Precisa", "pagar"])
b.tarefa(d, 220, 90, ["Informar", "chave e valor"], tipo="usuario")
b.tarefa(d, 590, 90, ["Ouvir nome, banco", "e valor e confirmar", "com a digital"], tipo="usuario")
b.evento(d, 760, 90, "link_envia", ["continua na", "parte 2"])
b.fluxo(d, [(117, 90), (145, 90)])
b.fluxo(d, [(295, 90), (515, 90)])
b.fluxo(d, [(665, 90), (743, 90)])

# App (y = 260)
b.evento(d, 220, 260, "inicio_msg", "Pedido recebido")
b.tarefa(d, 420, 260, ["Consultar a chave", "e falar nome,", "banco e valor"], tipo="servico")
b.evento(d, 630, 260, "msg", "Confirmação")
b.tarefa(d, 780, 260, ["Enviar o pedido", "com chave de", "idempotência"], tipo="servico")
b.fluxo(d, [(237, 260), (345, 260)])
b.fluxo(d, [(495, 260), (613, 260)])
b.fluxo(d, [(647, 260), (705, 260)])
b.fluxo(d, [(780, 294), (780, 376)])

# API e worker (y = 410)
b.tarefa(d, 780, 410, ["Reservar o saldo", "e gravar o Pix", "PENDENTE"], tipo="servico")
b.tarefa(d, 960, 410, ["Calcular a nota", "de risco"], tipo="servico")
b.gateway(d, 1100, 410, "x", "Nota ≥ 70?", lado="baixo")
b.evento(d, 1230, 410, "link_envia", ["A: envio", "ao parceiro"])
b.evento(d, 1230, 355, "link_envia", ["B: análise", "do analista"], lado="dir")
b.fluxo(d, [(855, 410), (885, 410)])
b.fluxo(d, [(1035, 410), (1078, 410)])
b.fluxo(d, [(1122, 410), (1213, 410)], "não", (1128, 401))
b.fluxo(d, [(1100, 388), (1100, 355), (1213, 355)], "sim", (1106, 347))

# mensagens
b.mensagem(d, [(220, 124), (220, 243)], "chave e valor", (226, 179))
b.mensagem(d, [(420, 226), (420, 176), (560, 176), (560, 124)], "fala nome, banco e valor", (426, 212))
b.mensagem(d, [(630, 124), (630, 243)], "confirma com a digital", (636, 179))

b.legenda(d, 40, 530, usados=["inicio", "msg", "tempo", "fim", "fim_msg", "link", "x", "evento"])
print(d.svg())
