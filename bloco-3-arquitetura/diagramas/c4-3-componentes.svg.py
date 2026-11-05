# titulo: C4 nível 3 · Componentes do container API
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1400, 1010)
CMP = s.C4_COMPONENTE
d.caixa(300, 20, 260, 84, "App mobile", [], cores=s.C4_CONTAINER, tipo="Container: React Native")
d.caixa(840, 20, 260, 84, "Painéis internos", [], cores=s.C4_CONTAINER, tipo="Container: React, Vite")
d.fronteira(40, 150, 1320, 680, "API", "Container: Node.js 22, NestJS")

d.caixa(100, 186, 1200, 90, "Controladores REST e guardas",
        ["Rotas /v1 e /v1/admin (inclui o webhook do parceiro com HMAC), validação de entrada,",
         "JWT de 15 minutos, papéis de funcionário (RBAC) e vínculo menor e responsável (ABAC)"],
        cores=CMP, tipo="Componente: NestJS Controllers e Guards")
d.seta([(430, 104), (430, 186)]); d.rotulo(438, 132, ["HTTPS/JSON"], ancora="start", fundo=False)
d.seta([(970, 104), (970, 186)]); d.rotulo(978, 132, ["HTTPS/JSON"], ancora="start", fundo=False)

# grupo dos módulos
d.partes.append('<rect x="100" y="320" width="1200" height="300" rx="6" fill="#F3F8FD" stroke="#9DB7D3" stroke-width="1"/>')
d.texto(116, 342, "Módulos de domínio (monolito modular, ADR-001). Cada um só escreve nas próprias tabelas", tam=12, peso="700", cor="#1F4E79", ancora="start")
d.seta([(700, 276), (700, 320)]); d.rotulo(708, 304, ["chama o serviço público do módulo"], ancora="start", fundo=False)

X = [130, 430, 730, 1030]; W = 240
mods_a = [("contas", ["Conta, carteiras e razão", "com partidas dobradas"]),
          ("pagamentos", ["Pix, boleto e metas.", "Saga do envio de Pix"]),
          ("antifraude", ["Nota de risco por regra", "(Strategy), Pix retido"]),
          ("atendimento", ["Chamados e mensagens", "do SAC"])]
mods_b = [("identidade", ["Cadastro, login, aparelho", "vinculado, consentimentos"]),
          ("familia", ["Vínculo com responsável,", "limites, contato de confiança"]),
          ("notificacao", ["Push, falas (voz),", "lembretes e outbox"]),
          ("backoffice", ["Funcionários, papéis", "e auditoria"])]
for x, (n, l) in zip(X, mods_a):
    d.caixa(x, 360, W, 104, n, l, cores=CMP, tipo="Componente: módulo NestJS")
for x, (n, l) in zip(X, mods_b):
    d.caixa(x, 496, W, 104, n, l, cores=CMP, tipo="Componente: módulo NestJS")
# dependências principais entre módulos
d.seta([(430, 412), (370, 412)]); d.rotulo(400, 404, ["lança"], fundo=False)
d.seta([(670, 412), (730, 412)]); d.rotulo(700, 404, ["avalia"], fundo=False)
d.seta([(550, 464), (550, 496)]); d.rotulo(558, 484, ["checa limite do menor"], ancora="start", fundo=False)

# camada de infraestrutura
d.caixa(100, 676, 400, 110, "Persistência", ["Repositórios, UnidadeDeTrabalho", "e gravação no outbox"], cores=CMP, tipo="Componente: Kysely")
d.caixa(560, 676, 240, 110, "AdaptadorBaasHttp", ["implementa PortaBancaria", "e PortaIdentidade"], cores=CMP, tipo="Componente: adaptador")
d.caixa(840, 676, 220, 110, "AdaptadorPolly", ["implementa PortaVoz"], cores=CMP, tipo="Componente: adaptador")
d.caixa(1100, 676, 200, 110, "AdaptadorExpoPush", ["implementa", "PortaNotificacao"], cores=CMP, tipo="Componente: adaptador")
d.seta([(300, 620), (300, 676)]); d.rotulo(308, 652, ["lê e grava"], ancora="start", fundo=False)
d.seta([(680, 620), (680, 676)]); d.rotulo(688, 652, ["usa PortaBancaria"], ancora="start", fundo=False)
d.seta([(950, 620), (950, 676)]); d.rotulo(958, 652, ["usa PortaVoz"], ancora="start", fundo=False)
d.seta([(1200, 620), (1200, 676)]); d.rotulo(1208, 652, ["usa PortaNotificacao"], ancora="start", fundo=False)

# externos ao container
d.banco(150, 880, 300, 96, "Banco de dados", [], tipo="Container: PostgreSQL 17")
d.caixa(560, 890, 240, 70, "Parceiro BaaS", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(840, 890, 220, 70, "Amazon Polly", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(1100, 890, 200, 70, "Expo Push", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.seta([(300, 786), (300, 880)]); d.rotulo(308, 856, ["SQL, 5432"], ancora="start", fundo=False)
d.seta([(680, 786), (680, 890)]); d.rotulo(688, 856, ["HTTPS/JSON"], ancora="start", fundo=False)
d.seta([(950, 786), (950, 890)]); d.rotulo(958, 856, ["HTTPS"], ancora="start", fundo=False)
d.seta([(1200, 786), (1200, 890)]); d.rotulo(1208, 856, ["HTTPS"], ancora="start", fundo=False)

s.legenda_c4(d, 40, 986, [("Container", s.C4_CONTAINER), ("Componente", s.C4_COMPONENTE), ("Sistema externo", s.C4_EXTERNO)])
print(d.svg())
