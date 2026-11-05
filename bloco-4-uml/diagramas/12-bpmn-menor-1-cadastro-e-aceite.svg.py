# titulo: BPMN 2.0 · Conta de menor, parte 1 de 2: cadastro, aceite do responsável e validação
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s
import bpmn as b

d = s.Desenho(1440, 990)

b.pool(d, 20, 20, 1400, 140, "Camila (menor)")
b.pool(d, 20, 190, 1400, 140, "Responsável")
b.pool(d, 20, 360, 1400, 440, "Rufus Bank")
b.raia(d, 54, 360, 1366, 90, "App")
b.raia(d, 54, 450, 1366, 350, "API e worker")
b.pool(d, 20, 830, 1400, 140, "Parceiro BaaS")

# Camila (y = 90)
b.evento(d, 100, 90, "inicio", ["Quer abrir", "conta"])
b.tarefa(d, 220, 90, ["Informar os dados", "(16 ou 17 anos)"], tipo="usuario")
b.tarefa(d, 390, 90, ["Enviar documento", "e selfie, ouvindo", "cada passo"], tipo="usuario")
b.tarefa(d, 560, 90, ["Informar CPF e", "celular do", "responsável"], tipo="usuario")
b.evento(d, 700, 90, "link_envia", ["continua na", "parte 2"])
b.fluxo(d, [(117, 90), (145, 90)])
b.fluxo(d, [(295, 90), (315, 90)])
b.fluxo(d, [(465, 90), (485, 90)])
b.fluxo(d, [(635, 90), (683, 90)])

# Responsável (y = 260)
b.evento(d, 810, 260, "inicio_msg", "Convite", lado="cima")
b.tarefa(d, 922, 260, ["Validar a própria", "identidade"], tipo="usuario")
b.tarefa(d, 1097, 260, ["Aceitar os termos", "e definir limites"], tipo="usuario")
b.evento(d, 1210, 260, "fim_msg")
b.fluxo(d, [(827, 260), (847, 260)])
b.fluxo(d, [(997, 260), (1022, 260)])
b.fluxo(d, [(1172, 260), (1193, 260)])

# App (y = 405)
b.evento(d, 560, 405, "inicio_msg", ["Cadastro", "recebido"], lado="dir")
b.fluxo(d, [(560, 422), (560, 586)])

# API e worker (linhas: 520, 620 e 730)
b.tarefa(d, 560, 620, ["Registrar cadastro", "e consentimentos"], tipo="servico")
b.gateway(d, 690, 620, "+")
b.fluxo(d, [(635, 620), (668, 620)])

# linha 1: convite ao responsável
b.tarefa(d, 810, 520, ["Enviar convite", "ao responsável"], tipo="servico")
b.gateway(d, 940, 520, "evento")
b.evento(d, 1210, 520, "msg", "Aceite")
b.fluxo(d, [(690, 598), (690, 520), (735, 520)])
b.fluxo(d, [(885, 520), (918, 520)])
b.fluxo(d, [(962, 520), (1193, 520)])
b.fluxo(d, [(1227, 520), (1280, 520), (1280, 598)])

# linha 2: convite vence em 7 dias
b.evento(d, 940, 620, "tempo", ["7 dias", "sem aceite"])
b.tarefa(d, 1060, 620, ["Cancelar e apagar", "os dados enviados"], tipo="servico")
b.evento(d, 1175, 620, "terminar", ["Pedido", "cancelado"])
b.fluxo(d, [(940, 542), (940, 603)])
b.fluxo(d, [(957, 620), (985, 620)])
b.fluxo(d, [(1135, 620), (1158, 620)])

# linha 3: validação da identidade do menor
b.tarefa(d, 810, 730, ["Pedir validação", "ao parceiro"], tipo="servico")
b.evento(d, 1040, 730, "msg", "Resultado", lado="cima")
b.gateway(d, 1140, 730, "x", "Aprovada?", lado="baixo")
b.evento(d, 1240, 730, "terminar", ["Pedido", "recusado"])
b.fluxo(d, [(690, 642), (690, 730), (735, 730)])
b.fluxo(d, [(885, 730), (1023, 730)])
b.fluxo(d, [(1057, 730), (1118, 730)])
b.fluxo(d, [(1162, 730), (1223, 730)], "não", (1167, 721))
b.fluxo(d, [(1140, 708), (1140, 680), (1280, 680), (1280, 642)], "sim", (1146, 700))

# junção: os dois caminhos terminaram bem
b.gateway(d, 1280, 620, "+")
b.evento(d, 1370, 620, "link_envia", ["C: continua", "na parte 2"])
b.fluxo(d, [(1302, 620), (1353, 620)])

# Parceiro BaaS (y = 900)
b.evento(d, 810, 900, "inicio_msg")
b.tarefa(d, 925, 900, ["Validar a", "identidade do menor"], tipo="servico")
b.evento(d, 1040, 900, "fim_msg")
b.fluxo(d, [(827, 900), (850, 900)])
b.fluxo(d, [(1000, 900), (1023, 900)])

# mensagens
b.mensagem(d, [(560, 124), (560, 388)], "dados, fotos e responsável", (566, 179))
b.mensagem(d, [(810, 486), (810, 277)], "convite por SMS", (816, 349))
b.mensagem(d, [(1210, 277), (1210, 503)], "aceite e limites", (1216, 349))
b.mensagem(d, [(810, 764), (810, 883)], "fotos do menor", (816, 819))
b.mensagem(d, [(1040, 883), (1040, 747)], "aprovada ou não", (1046, 819))

print(d.svg())
