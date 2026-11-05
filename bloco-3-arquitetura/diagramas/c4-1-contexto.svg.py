# titulo: C4 nível 1 · Contexto do sistema Rufus Bank
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1120, 700)
P = 150  # altura das pessoas
d.pessoa(40, 20, 230, P, "Cliente titular", ["Antônio, Dona Marlene.", "Usa a conta por ícones,", "áudio e Pix"])
d.pessoa(310, 20, 230, P, "Cliente menor", ["Camila, 16 ou 17 anos.", "Conta com limites", "do responsável"])
d.pessoa(580, 20, 230, P, "Responsável legal", ["e contato de confiança.", "Autoriza, limita e", "recebe avisos"])
d.pessoa(850, 20, 230, P, "Funcionários", ["Atendente do SAC,", "analista antifraude,", "administrador"])

d.caixa(110, 290, 900, 84, "Rufus Bank", ["Conta digital com interface simples, voz em toda tela e proteção contra golpe"],
        cores=s.C4_SISTEMA, tipo="Sistema de software", tam_titulo=16)

for cx, rot in [(155, ["Usa o app", "[HTTPS]"]), (425, ["Usa o app", "[HTTPS]"]),
                (695, ["Aceita vínculo, define", "limites, aprova [HTTPS]"]), (965, ["Usa os painéis", "internos [HTTPS]"])]:
    d.seta([(cx, 20 + P), (cx, 290)])
    d.rotulo(cx + 8, 222, rot, ancora="start", fundo=False)

d.caixa(110, 520, 330, 110, "Parceiro BaaS", ["Instituição autorizada pelo BC:", "conta, Pix, boleto e", "validação de identidade"],
        cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(500, 520, 240, 110, "Amazon Polly", ["Transforma texto em fala"], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(790, 520, 220, 110, "Expo Push", ["Notificação no celular", "via FCM e APNs"], cores=s.C4_EXTERNO, tipo="Sistema externo")

d.seta([(200, 374), (200, 520)])
d.rotulo(192, 422, ["Abre conta, envia Pix,", "paga boleto", "[HTTPS/JSON]"], ancora="end", fundo=False)
d.seta([(330, 520), (330, 374)])
d.rotulo(338, 422, ["Avisa Pix recebido", "e confirmações", "[webhook HTTPS]"], ancora="start", fundo=False)
d.seta([(620, 374), (620, 520)])
d.rotulo(628, 450, ["Pede áudio [HTTPS]"], ancora="start", fundo=False)
d.seta([(900, 374), (900, 520)])
d.rotulo(908, 440, ["Envia notificação", "[HTTPS]"], ancora="start", fundo=False)

s.legenda_c4(d, 40, 660, [("Pessoa", s.C4_PESSOA), ("Sistema do Rufus", s.C4_SISTEMA), ("Sistema externo", s.C4_EXTERNO)])
d.texto(1080, 672, "Sem atendimento presencial (fora do escopo)", tam=11, cor="#6B7280", ancora="end", italico=True)
print(d.svg())
