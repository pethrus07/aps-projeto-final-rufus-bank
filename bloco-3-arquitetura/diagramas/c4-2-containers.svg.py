# titulo: C4 nível 2 · Containers do Rufus Bank
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1440, 960)
d.pessoa(110, 20, 260, 150, "Clientes", ["Titular, menor, responsável", "e contato de confiança"])
d.pessoa(450, 20, 260, 150, "Funcionários", ["SAC, antifraude e", "administração"])
d.fronteira(40, 200, 1020, 700, "Rufus Bank", "Sistema de software")

d.caixa(90, 240, 300, 118, "App mobile", ["Telas com ícone e botão Ouvir,", "biometria, câmera de boleto"],
        cores=s.C4_CONTAINER, tipo="Container: React Native, Expo")
d.caixa(430, 240, 300, 118, "Painéis internos", ["SAC, fila antifraude e", "cadastro de funcionários"],
        cores=s.C4_CONTAINER, tipo="Container: React, Vite")
d.caixa(380, 470, 320, 124, "API", ["Monolito modular: regras de conta,", "Pix, família, antifraude. Porta 3000"],
        cores=s.C4_CONTAINER, tipo="Container: Node.js 22, NestJS")
d.banco(100, 690, 280, 130, "Banco de dados", ["Clientes, razão contábil,", "transações, outbox"],
        tipo="Container: PostgreSQL 17, RDS")
d.caixa(440, 690, 240, 120, "Arquivos", ["Documentos, comprovantes", "e cache de áudio"],
        cores=s.C4_CONTAINER, tipo="Container: Amazon S3")
d.caixa(760, 690, 280, 120, "Worker", ["Lê o outbox: envia Pix,", "notifica, concilia"],
        cores=s.C4_CONTAINER, tipo="Container: Node.js 22")

d.caixa(1160, 250, 250, 100, "Amazon Polly", ["Texto para fala"], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(1160, 440, 250, 120, "Parceiro BaaS", ["Conta, Pix, boleto,", "validação de identidade"], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(1160, 760, 250, 100, "Expo Push", ["FCM e APNs"], cores=s.C4_EXTERNO, tipo="Sistema externo")

# pessoas -> front-ends
d.seta([(240, 170), (240, 240)]); d.rotulo(232, 189, ["Usa [HTTPS]"], ancora="end", fundo=False)
d.seta([(580, 170), (580, 240)]); d.rotulo(572, 189, ["Usa [HTTPS]"], ancora="end", fundo=False)
# front-ends -> API
d.seta([(240, 358), (240, 425), (440, 425), (440, 470)])
d.rotulo(248, 384, ["Chama /v1", "[HTTPS/JSON, 443]"], ancora="start", fundo=False)
d.seta([(580, 358), (580, 470)])
d.rotulo(588, 400, ["Chama /v1/admin", "[HTTPS/JSON, 443]"], ancora="start", fundo=False)
# API -> externos
d.seta([(700, 482), (1110, 482), (1110, 300), (1160, 300)])
d.rotulo(905, 474, ["Pede áudio [HTTPS]"], fundo=False)
d.seta([(700, 520), (1160, 520)])
d.rotulo(880, 512, ["Consulta chave Pix e boleto [HTTPS/JSON]"], fundo=False)
d.seta([(1160, 548), (700, 548)])
d.rotulo(880, 568, ["Webhook do parceiro [HTTPS, assinatura HMAC]"], fundo=False)
# API -> dados
d.seta([(420, 594), (420, 645), (240, 645), (240, 690)])
d.rotulo(330, 636, ["Lê e grava [SQL, 5432]"], fundo=False)
d.seta([(560, 594), (560, 690)])
d.rotulo(568, 648, ["Grava arquivos", "[HTTPS]"], ancora="start", fundo=False)
# worker
d.seta([(900, 810), (900, 860), (240, 860), (240, 820)])
d.rotulo(570, 880, ["Lê o outbox e grava o resultado [SQL, 5432]"], fundo=False)
d.seta([(1040, 712), (1285, 712), (1285, 560)])
d.rotulo(1293, 630, ["Envia Pix,", "paga boleto", "[HTTPS/JSON]"], ancora="start", fundo=False)
d.seta([(1040, 790), (1160, 790)])
d.rotulo(1110, 812, ["Envia push", "[HTTPS]"], fundo=False)

s.legenda_c4(d, 40, 925, [("Pessoa", s.C4_PESSOA), ("Container", s.C4_CONTAINER), ("Sistema externo", s.C4_EXTERNO)])
print(d.svg())
