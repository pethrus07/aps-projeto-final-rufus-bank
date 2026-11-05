# titulo: BPMN 2.0 · Envio de Pix, parte 2 de 2: análise, liquidação e estorno
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s
import bpmn as b

d = s.Desenho(1250, 905)

b.pool(d, 20, 20, 1210, 140, "Cliente")
b.pool(d, 20, 190, 1210, 530, "Rufus Bank")
b.raia(d, 54, 190, 1176, 140, "Analista antifraude")
b.raia(d, 54, 330, 1176, 140, "App")
b.raia(d, 54, 470, 1176, 250, "API e worker")
b.pool(d, 20, 750, 1210, 140, "Parceiro BaaS")

# Cliente (y = 90)
b.evento(d, 110, 90, "link_recebe", ["da parte 1"])
b.evento(d, 1020, 90, "msg", "Resultado", lado="cima")
b.evento(d, 1130, 90, "fim", "Fim")
b.fluxo(d, [(127, 90), (1003, 90)])
b.fluxo(d, [(1037, 90), (1113, 90)])

# Analista antifraude (y = 260)
b.evento(d, 110, 260, "link_recebe", "B")
b.tarefa(d, 250, 260, ["Analisar o", "Pix retido"], tipo="usuario")
b.gateway(d, 400, 260, "x", "Decisão")
b.tarefa(d, 550, 260, ["Bloquear a conta", "e estornar", "a reserva"], tipo="servico")
b.evento(d, 690, 260, "fim_msg", "Cliente avisado")
b.fluxo(d, [(127, 260), (175, 260)])
b.fluxo(d, [(325, 260), (378, 260)])
b.fluxo(d, [(422, 260), (475, 260)], "recusar", (427, 251))
b.fluxo(d, [(625, 260), (673, 260)])

# App (y = 400)
b.tarefa(d, 1020, 400, ["Mostrar e falar", "o resultado"], tipo="servico")
b.evento(d, 1150, 400, "fim", "Fim")
b.fluxo(d, [(1095, 400), (1133, 400)])

# API e worker (linha 1: y = 545, linha 2: y = 650)
b.evento(d, 110, 545, "link_recebe", "A")
b.tarefa(d, 400, 545, ["Enviar ao parceiro", "(nova tentativa", "idempotente)"], tipo="servico")
b.gateway(d, 520, 545, "evento")
b.evento(d, 610, 545, "msg", ["Resposta do", "parceiro"], lado="cima")
b.gateway(d, 710, 545, "x", "Aceito?")
b.tarefa(d, 860, 545, ["Confirmar os", "lançamentos", "(CONCLUIDA)"], tipo="servico")
b.gateway(d, 1020, 545, "x")
b.evento(d, 520, 650, "tempo", ["5 tentativas", "sem resposta"])
b.gateway(d, 710, 650, "x")
b.tarefa(d, 860, 650, ["Estornar a reserva", "(compensação", "da saga)"], tipo="servico")

b.fluxo(d, [(127, 545), (325, 545)])
b.fluxo(d, [(400, 282), (400, 511)], "liberar", (406, 312))
b.fluxo(d, [(475, 545), (498, 545)])
b.fluxo(d, [(542, 545), (593, 545)])
b.fluxo(d, [(627, 545), (688, 545)])
b.fluxo(d, [(732, 545), (785, 545)], "sim", (737, 536))
b.fluxo(d, [(710, 567), (710, 628)], "não", (716, 602))
b.fluxo(d, [(520, 567), (520, 633)])
b.fluxo(d, [(537, 650), (688, 650)])
b.fluxo(d, [(732, 650), (785, 650)])
b.fluxo(d, [(935, 650), (1020, 650), (1020, 567)])
b.fluxo(d, [(935, 545), (998, 545)])
b.fluxo(d, [(1020, 523), (1020, 434)])

# Parceiro BaaS (y = 820)
b.evento(d, 400, 820, "inicio_msg")
b.tarefa(d, 500, 820, ["Liquidar o Pix", "no SPI"], w=120, tipo="servico")
b.evento(d, 610, 820, "fim_msg")
b.fluxo(d, [(417, 820), (440, 820)])
b.fluxo(d, [(560, 820), (593, 820)])

# mensagens
b.mensagem(d, [(400, 579), (400, 803)], "pedido de Pix", (406, 739))
b.mensagem(d, [(610, 803), (610, 562)], "aceito ou recusado", (616, 739))
b.mensagem(d, [(1028, 366), (1028, 106)], "resultado", (1034, 214))
b.mensagem(d, [(690, 243), (690, 176), (1012, 176), (1012, 106)], "Pix recusado", (698, 214))

print(d.svg())
