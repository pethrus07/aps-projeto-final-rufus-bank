# titulo: Diagrama de Deployment, parte 1 de 2 · produção na AWS
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(1040, 980)
NEUTRO = ("#F3F4F6", "#374151", "#111827")
def rot(x, y, t, a="start"): d.rotulo(x, y, t if isinstance(t, list) else [t], tam=12, ancora=a, fundo=False)

# dispositivos dos usuários
d.no(40, 20, 240, 110, ["Celular Android ou iOS"], "«device»")
d.artefato(60, 78, 200, 42, ["App Rufus"], "«artifact» React Native")
d.no(320, 20, 240, 110, ["Navegador do funcionário"], "«device»")
d.artefato(340, 78, 200, 42, ["Painéis internos"], "«artifact» React")

# região AWS
d.fronteira(20, 170, 1000, 690, "AWS sa-east-1 (São Paulo)", "«cloud»", cor="#B45309", posicao="cima-dir")
# produção
d.fronteira(40, 200, 960, 490, "«environment» Produção", None, cor="#1F2937", posicao="cima-dir")
d.no(300, 232, 460, 76, ["AWS WAF + Application Load Balancer"], "«node» HTTPS 443, TLS 1.2+")
d.fronteira(60, 340, 460, 330, "Zona de disponibilidade A", None, cor="#6B7280", posicao="baixo-dir")
d.fronteira(540, 340, 440, 330, "Zona de disponibilidade B", None, cor="#6B7280", posicao="baixo-esq")
d.no(100, 390, 170, 72, ["Tarefa API"], "«Fargate» :3000")
d.banco(340, 382, 160, 96, "Primário", [], cores=NEUTRO, tipo="RDS PostgreSQL 17")
d.no(100, 570, 170, 62, ["NAT Gateway"], "«node»")
d.no(340, 570, 160, 72, ["Tarefa worker"], "«Fargate»")
d.banco(580, 382, 160, 96, "Réplica", [], cores=NEUTRO, tipo="síncrona")
d.no(800, 390, 160, 72, ["Tarefa API"], "«Fargate» :3000")
d.no(800, 570, 160, 62, ["NAT Gateway"], "«node»")

# usuários -> ALB
d.seta([(160, 130), (160, 220), (400, 220), (400, 232)]); rot(168, 154, "HTTPS 443 · api.rufusbank.com.br")
d.seta([(470, 130), (470, 232)]); rot(478, 154, "HTTPS 443 /admin · só IPs da empresa")
# ALB -> tarefas
d.seta([(330, 308), (330, 348), (185, 348), (185, 390)]); rot(193, 370, "HTTP 3000")
d.seta([(730, 308), (730, 348), (880, 348), (880, 390)]); rot(888, 370, "HTTP 3000")
# tarefas -> banco
d.seta([(270, 426), (340, 426)]); rot(305, 418, "5432", "middle")
d.seta([(840, 390), (840, 370), (450, 370), (450, 390)]); rot(645, 364, "TCP 5432 (TLS) para o primário", "middle")
d.seta([(420, 570), (420, 478)]); rot(428, 530, "5432")
d.seta([(500, 430), (580, 430)], ponta="cheia"); rot(660, 500, ["replicação síncrona", "a partir do primário"], "middle")
# saída para a internet
d.seta([(185, 462), (185, 570)]); rot(193, 520, "443")
d.seta([(340, 605), (270, 605)]); rot(305, 597, "443", "middle")
d.seta([(880, 462), (880, 570)]); rot(888, 520, "443")


# serviços gerenciados da região
d.partes.append('<rect x="260" y="712" width="500" height="138" rx="6" fill="#FFFBEB" stroke="#B45309" stroke-width="1"/>')
d.texto(276, 736, "Serviços gerenciados da região (fora da VPC)", tam=13, peso="700", ancora="start")
for i, nome in enumerate(["S3", "Amazon Polly", "Secrets Manager"]):
    d.artefato(276 + i * 158, 750, 150, 42, [nome], "«service»")
for i, nome in enumerate(["CloudWatch", "ECR (imagens)"]):
    d.artefato(276 + i * 158, 800, 150, 42, [nome], "«service»")
d.seta([(510, 690), (510, 712)]); rot(518, 706, "HTTPS 443")

# sistemas externos
d.caixa(80, 890, 220, 70, "Parceiro BaaS", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.caixa(770, 890, 220, 70, "Expo Push", [], cores=s.C4_EXTERNO, tipo="Sistema externo")
d.seta([(185, 632), (185, 890)]); rot(193, 882, "HTTPS 443")
d.seta([(880, 632), (880, 890)]); rot(888, 882, "HTTPS 443")
print(d.svg())
