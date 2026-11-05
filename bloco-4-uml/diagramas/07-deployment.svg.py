# titulo: Diagrama de Deployment · ambientes dev, homologação e produção
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1500, 1150)
NEUTRO = ("#F3F4F6", "#374151", "#111827")
def rot(x, y, t, a="start"): d.rotulo(x, y, t if isinstance(t, list) else [t], tam=10.5, ancora=a, fundo=False)

# dispositivos dos usuários
d.no(40, 20, 240, 110, ["Celular Android ou iOS"], "«device»")
d.artefato(60, 78, 200, 42, ["App Rufus"], "«artifact» React Native")
d.no(320, 20, 240, 110, ["Navegador do funcionário"], "«device»")
d.artefato(340, 78, 200, 42, ["Painéis internos"], "«artifact» React")

# desenvolvimento local
d.no(620, 20, 840, 240, ["Notebook do desenvolvedor"], "«device» Ambiente de desenvolvimento")
d.partes.append('<rect x="640" y="92" width="800" height="150" fill="#FFFFFF" stroke="#374151" stroke-width="1.1"/>')
d.texto(652, 112, "«executionEnvironment» Docker Compose", tam=11, cor="#4B5563", ancora="start", italico=True)
d.artefato(660, 130, 220, 46, ["api · porta 3000"], "«container»")
d.artefato(910, 130, 200, 46, ["worker"], "«container»")
d.artefato(1150, 130, 270, 46, ["postgres:17 · porta 5432"], "«container»")
d.seta([(1110, 153), (1150, 153)])
d.seta([(770, 176), (770, 200), (1285, 200), (1285, 176)])
rot(1000, 194, "TCP 5432", "middle")
d.texto(660, 228, "App no Expo aponta para http://IP-do-notebook:3000. Parceiro BaaS e voz usam adaptadores falsos (ADR-002).", tam=11, cor="#4B5563", ancora="start")

# região AWS
d.fronteira(20, 300, 1460, 700, "AWS sa-east-1 (São Paulo)", "«cloud»", cor="#B45309", posicao="cima-dir")
# produção
d.fronteira(40, 330, 960, 490, "«environment» Produção", None, cor="#1F2937", posicao="cima-dir")
d.no(300, 362, 460, 76, ["AWS WAF + Application Load Balancer"], "«node» HTTPS 443, TLS 1.2+")
d.fronteira(60, 470, 460, 330, "Zona de disponibilidade A", None, cor="#6B7280", posicao="baixo-dir")
d.fronteira(540, 470, 440, 330, "Zona de disponibilidade B", None, cor="#6B7280", posicao="baixo-esq")
d.no(100, 520, 170, 72, ["Tarefa API"], "«Fargate» :3000")
d.banco(340, 512, 160, 96, "Primário", [], cores=NEUTRO, tipo="RDS PostgreSQL 17")
d.no(100, 700, 170, 62, ["NAT Gateway"], "«node»")
d.no(340, 700, 160, 72, ["Tarefa worker"], "«Fargate»")
d.banco(580, 512, 160, 96, "Réplica", [], cores=NEUTRO, tipo="síncrona")
d.no(800, 520, 160, 72, ["Tarefa API"], "«Fargate» :3000")
d.no(800, 700, 160, 62, ["NAT Gateway"], "«node»")

# usuários -> ALB
d.seta([(160, 130), (160, 350), (400, 350), (400, 362)]); rot(168, 250, ["HTTPS 443", "api.rufusbank.com.br"])
d.seta([(470, 130), (470, 362)]); rot(478, 250, ["HTTPS 443 /admin", "(só IPs da empresa)"])
# ALB -> tarefas
d.seta([(330, 438), (330, 478), (185, 478), (185, 520)]); rot(193, 500, "HTTP 3000")
d.seta([(730, 438), (730, 478), (880, 478), (880, 520)]); rot(888, 500, "HTTP 3000")
# tarefas -> banco
d.seta([(270, 556), (340, 556)]); rot(305, 548, "5432", "middle")
d.seta([(840, 520), (840, 500), (450, 500), (450, 520)]); rot(645, 494, "TCP 5432 (TLS) para o primário", "middle")
d.seta([(420, 700), (420, 608)]); rot(428, 660, "5432")
d.seta([(500, 560), (580, 560)], ponta="cheia"); rot(660, 630, ["replicação síncrona", "a partir do primário"], "middle")
# saída para a internet
d.seta([(185, 592), (185, 700)]); rot(193, 650, "443")
d.seta([(340, 735), (270, 735)]); rot(305, 727, "443", "middle")
d.seta([(880, 592), (880, 700)]); rot(888, 650, "443")

# homologação
d.fronteira(1030, 330, 430, 490, "«environment» Homologação (1 zona)", None, cor="#1F2937")
d.no(1060, 362, 370, 62, ["Load Balancer + WAF"], "«node» HTTPS 443")
d.no(1060, 492, 170, 72, ["Tarefa API"], "«Fargate» :3000")
d.no(1260, 492, 170, 72, ["Tarefa worker"], "«Fargate»")
d.banco(1060, 640, 170, 96, "PostgreSQL 17", [], cores=NEUTRO, tipo="Single-AZ")
d.no(1260, 660, 170, 62, ["NAT Gateway"], "«node»")
d.seta([(1145, 424), (1145, 492)]); rot(1153, 462, "HTTP 3000")
d.seta([(1145, 564), (1145, 640)]); rot(1153, 606, "5432")
d.seta([(1300, 564), (1300, 600), (1205, 600), (1205, 640)])
d.seta([(1390, 564), (1390, 660)]); rot(1398, 616, "443")

# serviços gerenciados da região
d.partes.append('<rect x="1030" y="842" width="430" height="140" rx="6" fill="#FFFBEB" stroke="#B45309" stroke-width="1"/>')
d.texto(1046, 864, "Serviços gerenciados da região (fora da VPC)", tam=12, peso="700", ancora="start")
for i, nome in enumerate(["S3", "Amazon Polly", "Secrets Manager"]):
    d.artefato(1046 + i * 136, 878, 128, 42, [nome], "«service»")
for i, nome in enumerate(["CloudWatch", "ECR (imagens)"]):
    d.artefato(1046 + i * 136, 928, 128, 42, [nome], "«service»")
d.seta([(960, 820), (960, 912), (1030, 912)]); rot(968, 870, "HTTPS 443")

# sistemas externos
d.caixa(80, 1040, 220, 70, "Parceiro BaaS", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(770, 1040, 220, 70, "Expo Push", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.seta([(185, 762), (185, 1040)]); rot(193, 1020, "HTTPS 443")
d.seta([(880, 762), (880, 1040)]); rot(888, 1020, "HTTPS 443")
print(d.svg())
