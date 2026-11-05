# titulo: Diagrama de Componentes · API do Rufus Bank e sistemas externos
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1250, 960)
W, H = 190, 90
X = [90, 380, 670, 960]
R1, R2, R3 = 236, 446, 606

def uso(pts, nome=None, pos=None, ancora="middle"):
    d.seta(pts, tracejada=True, ponta="aberta")
    if nome:
        d.rotulo(pos[0], pos[1], [nome], tam=10.5, ancora=ancora, fundo=False)

# clientes da API
d.componente(345, 24, 240, 70, ["App mobile"])
d.componente(655, 24, 240, 70, ["Painéis internos"])
# componente API (contém os módulos)
d.partes.append('<rect x="50" y="170" width="1140" height="560" fill="#FAFAFA" stroke="#374151" stroke-width="1.6"/>')
d.texto(70, 194, "«component»  API (Node.js 22, NestJS)", tam=13, peso="700", ancora="start")
# interfaces fornecidas pela API no topo
d.linha([(465, 170), (465, 157)]); d.pirulito(465, 150, "REST /v1", lado="esq")
d.linha([(775, 170), (775, 157)]); d.pirulito(775, 150, "REST /v1/admin", lado="dir")
d.soquete(465, 150, "cima"); d.linha([(465, 94), (465, 139)])
d.soquete(775, 150, "cima"); d.linha([(775, 94), (775, 139)])

# linha 1 e 2: módulos
for x, n in zip(X, ["identidade", "contas", "pagamentos", "antifraude"]):
    d.componente(x, R1, W, H, [n])
for x, n in zip(X, ["backoffice", "atendimento", "familia", "notificacao"]):
    d.componente(x, R2, W, H, [n])

# dependências entre módulos (interfaces públicas de cada módulo)
uso([(670, 290), (570, 290)], "ServicoContas", (620, 282))
uso([(860, 290), (960, 290)], "MotorAntifraude", (910, 282))
uso([(765, 326), (765, 446)], "ServicoFamilia", (773, 392), "start")
uso([(475, 446), (475, 326)], "ServicoContas", (483, 392), "start")
uso([(380, 500), (280, 500)], "Auditoria", (330, 492))

# linha 3: persistência e adaptadores
d.componente(90, R3, 320, 84, ["Persistência"])
d.texto(242, R3 + 58, ["Repositórios e UnidadeDeTrabalho,", "usados por todos os módulos"], tam=10.5, cor="#4B5563")
d.componente(500, R3, 230, 84, ["AdaptadorBaasHttp"])
d.componente(770, R3, 180, 84, ["AdaptadorPolly"])
d.componente(990, R3, 180, 84, ["AdaptadorExpoPush"])
# portas (interfaces fornecidas pelos adaptadores)
for cx, nome, lado in [(545, "PortaIdentidade", "esq"), (650, "PortaBancaria", "dir"), (860, "PortaVoz", "dir"), (1080, "PortaNotificacao", "dir")]:
    d.linha([(cx, R3), (cx, R3 - 14)]); d.pirulito(cx, R3 - 21, nome, lado=lado)
# módulos que requerem as portas
uso([(150, 326), (150, 360), (70, 360), (70, 566), (545, 566), (545, 574)])
uso([(700, 326), (700, 380), (650, 380), (650, 574)])
uso([(1080, 536), (1080, 574)])
uso([(990, 536), (990, 556), (860, 556), (860, 574)])

# externos
d.banco(110, 790, 280, 100, "PostgreSQL 17", [], cores=("#F3F4F6", "#374151", "#111827"), tipo="RDS Multi-AZ")
d.componente(500, 800, 230, 80, ["Parceiro BaaS"], estereotipo="«sistema externo»", cores=s.UML_SUAVE)
d.componente(770, 800, 180, 80, ["Amazon Polly"], estereotipo="«sistema externo»", cores=s.UML_SUAVE)
d.componente(990, 800, 180, 80, ["Expo Push"], estereotipo="«sistema externo»", cores=s.UML_SUAVE)
d.seta([(250, 690), (250, 790)]); d.rotulo(258, 760, ["SQL, porta 5432"], tam=10.5, ancora="start", fundo=False)
d.seta([(615, 690), (615, 800)]); d.rotulo(623, 760, ["HTTPS/JSON"], tam=10.5, ancora="start", fundo=False)
d.seta([(860, 690), (860, 800)]); d.rotulo(868, 760, ["HTTPS"], tam=10.5, ancora="start", fundo=False)
d.seta([(1080, 690), (1080, 800)]); d.rotulo(1088, 760, ["HTTPS"], tam=10.5, ancora="start", fundo=False)

d.texto(50, 930, "Legenda: ○ interface fornecida · ◡ interface requerida · seta tracejada = dependência «use» da interface", tam=11, cor="#4B5563", ancora="start")
print(d.svg())
