# titulo: BPMN 2.0 · Conta de menor, parte 2 de 2: abertura da conta
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s
import bpmn as b

d = s.Desenho(940, 800)

b.pool(d, 20, 20, 900, 140, "Camila (menor)")
b.pool(d, 20, 190, 900, 290, "Rufus Bank")
b.raia(d, 54, 190, 866, 140, "App")
b.raia(d, 54, 330, 866, 150, "API e worker")
b.pool(d, 20, 510, 900, 140, "Parceiro BaaS")

# Camila (y = 90)
b.evento(d, 100, 90, "link_recebe", ["da parte 1"])
b.evento(d, 670, 90, "msg", "Conta ativa", lado="cima")
b.tarefa(d, 780, 90, ["Criar a senha e", "ativar a digital"], tipo="usuario")
b.evento(d, 885, 90, "fim")
b.fluxo(d, [(117, 90), (653, 90)])
b.fluxo(d, [(687, 90), (705, 90)])
b.fluxo(d, [(855, 90), (868, 90)])

# App (y = 260)
b.tarefa(d, 670, 260, ["Avisar por voz e", "push: conta ativa"], tipo="servico")
b.evento(d, 800, 260, "fim", "Fim")
b.fluxo(d, [(745, 260), (783, 260)])

# API e worker (y = 405)
b.evento(d, 100, 405, "link_recebe", "C")
b.tarefa(d, 250, 405, ["Criar o vínculo e", "pedir a abertura", "da conta"], tipo="servico")
b.evento(d, 420, 405, "msg", "Conta aberta", lado="cima")
b.tarefa(d, 560, 405, ["Criar a conta e a", "carteira principal"], tipo="servico")
b.fluxo(d, [(117, 405), (175, 405)])
b.fluxo(d, [(325, 405), (403, 405)])
b.fluxo(d, [(437, 405), (485, 405)])
b.fluxo(d, [(635, 405), (670, 405), (670, 294)])

# Parceiro BaaS (y = 580)
b.evento(d, 250, 580, "inicio_msg")
b.tarefa(d, 360, 580, ["Abrir a conta"], w=120, tipo="servico")
b.evento(d, 480, 580, "fim_msg")
b.fluxo(d, [(267, 580), (300, 580)])
b.fluxo(d, [(420, 580), (463, 580)])

# mensagens
b.mensagem(d, [(250, 439), (250, 563)], "pedido de abertura", (256, 497))
b.mensagem(d, [(480, 563), (480, 495), (426, 495), (426, 422)], "conta aberta", (486, 497))
b.mensagem(d, [(670, 226), (670, 107)], "conta ativa", (676, 179))

b.legenda(d, 40, 685, usados=["inicio", "msg", "tempo", "fim", "fim_msg", "terminar", "link", "x", "+", "evento"], largura=860)
print(d.svg())
