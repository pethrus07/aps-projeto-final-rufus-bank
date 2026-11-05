# titulo: Diagrama de infraestrutura · produção na AWS sa-east-1 (São Paulo)
"""Desenho da infraestrutura de produção com posição fixa: as duas zonas de
disponibilidade lado a lado e, em cada uma, as três camadas de subnet
(pública, privada, dados). Gerado por ferramentas/diagramas/gerar.py."""
from html import escape

W, H = 1000, 820
FONTE = "Arial, Helvetica, sans-serif"
TINTA, CINZA, LINHA = "#111827", "#4B5563", "#6B7280"
partes = []


def caixa(x, y, w, h, titulo, linhas=(), fundo="#FFFFFF", borda="#9CA3AF", raio=6, negrito=True):
    partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{raio}" fill="{fundo}" stroke="{borda}" stroke-width="1.2"/>')
    cy = y + 22
    partes.append(f'<text x="{x + w / 2}" y="{cy}" text-anchor="middle" font-family="{FONTE}" font-size="13" '
                  f'font-weight="{700 if negrito else 400}" fill="{TINTA}">{escape(titulo)}</text>')
    for i, l in enumerate(linhas):
        partes.append(f'<text x="{x + w / 2}" y="{cy + 18 * (i + 1)}" text-anchor="middle" font-family="{FONTE}" '
                      f'font-size="12" fill="{CINZA}">{escape(l)}</text>')


def area(x, y, w, h, rotulo, fundo, borda, tracejado=False):
    dash = ' stroke-dasharray="6 4"' if tracejado else ""
    partes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fundo}" stroke="{borda}" stroke-width="1.4"{dash}/>')
    partes.append(f'<text x="{x + 12}" y="{y + 20}" font-family="{FONTE}" font-size="12.5" font-weight="700" fill="{borda}">{escape(rotulo)}</text>')


def seta(pontos, rotulo=None, pos=None, tracejada=False, ancora="start"):
    d = "M" + " L".join(f"{x} {y}" for x, y in pontos)
    dash = ' stroke-dasharray="5 4"' if tracejada else ""
    partes.append(f'<path d="{d}" fill="none" stroke="{LINHA}" stroke-width="1.3"{dash} marker-end="url(#seta)"/>')
    if rotulo:
        x, y = pos
        partes.append(f'<text x="{x}" y="{y}" text-anchor="{ancora}" font-family="{FONTE}" font-size="11.5" fill="{CINZA}">{escape(rotulo)}</text>')


# usuários e externos (fora da AWS)
caixa(250, 20, 260, 60, "App Rufus e painéis internos", ["Android e iOS · /admin só dos IPs da empresa"], fundo="#F9FAFB")
caixa(650, 20, 300, 60, "Serviços externos", ["Parceiro BaaS (conta, Pix, boleto) · Expo Push"], fundo="#F9FAFB")

# região
area(20, 110, 960, 692, "AWS · região sa-east-1 (São Paulo)", "#FFFBF2", "#B45309")
caixa(250, 140, 260, 56, "AWS WAF", ["5 regras gerenciadas + limite por IP"], fundo="#FEF3C7", borda="#D97706")

# VPC e zonas
area(40, 220, 920, 470, "VPC 10.0.0.0/16", "#F5F9FF", "#2563EB")
area(60, 250, 420, 420, "Zona sa-east-1a", "#FFFFFF", "#60A5FA", tracejado=True)
area(520, 250, 420, 420, "Zona sa-east-1b", "#FFFFFF", "#60A5FA", tracejado=True)

# camadas (x de cada coluna)
A, B, LW = 80, 540, 380
caixa(A, 285, LW, 66, "Subnet pública 10.0.0.0/24", ["Nó do Application Load Balancer (HTTPS 443)", "NAT Gateway A + IP público"], fundo="#ECFDF5", borda="#059669")
caixa(B, 285, LW, 66, "Subnet pública 10.0.1.0/24", ["Nó do Application Load Balancer (HTTPS 443)", "NAT Gateway B + IP público"], fundo="#ECFDF5", borda="#059669")
caixa(A, 415, LW, 84, "Subnet privada 10.0.10.0/24", ["ECS Fargate · API tarefa 1 (0,5 vCPU, 1 GB)", "ECS Fargate · Worker (0,25 vCPU, 0,5 GB)", "auto scaling da API: 2 a 6 tarefas"], fundo="#EFF6FF", borda="#2563EB")
caixa(B, 415, LW, 84, "Subnet privada 10.0.11.0/24", ["ECS Fargate · API tarefa 2 (0,5 vCPU, 1 GB)", "sem IP público", "auto scaling da API: 2 a 6 tarefas"], fundo="#EFF6FF", borda="#2563EB")
caixa(A, 565, LW, 66, "Subnet de dados 10.0.20.0/24", ["RDS PostgreSQL 17 · db.t4g.medium · PRIMÁRIO", "gp3 50 GB · backup com PITR de 35 dias"], fundo="#F5F3FF", borda="#7C3AED")
caixa(B, 565, LW, 66, "Subnet de dados 10.0.21.0/24", ["RDS PostgreSQL 17 · RÉPLICA em espera", "assume sozinha se a zona A cair"], fundo="#F5F3FF", borda="#7C3AED")

# serviços regionais
servicos = [("S3", "comprovantes, áudios"), ("Amazon Polly", "voz pt-BR"), ("Secrets Manager", "10 segredos"),
            ("CloudWatch", "logs, métricas, alarmes"), ("ECR", "imagens api e worker")]
for i, (t, l) in enumerate(servicos):
    caixa(48 + i * 186, 730, 172, 56, t, [l], fundo="#FFFFFF", borda="#B45309")
partes.append(f'<text x="500" y="718" text-anchor="middle" font-family="{FONTE}" font-size="12" fill="{CINZA}">'
              f'Serviços regionais, acessados pelas tarefas da subnet privada</text>')

# setas
seta([(380, 80), (380, 138)], "HTTPS 443", (388, 99))
seta([(340, 196), (340, 283)], "HTTPS 443", (348, 276))
seta([(460, 196), (700, 240), (700, 283)], "HTTPS 443", (708, 276))
seta([(270, 351), (270, 413)], "HTTP 3000", (278, 388))
seta([(730, 351), (730, 413)], "HTTP 3000", (738, 388))
seta([(270, 499), (270, 563)], "TCP 5432", (278, 536))
seta([(640, 499), (640, 530), (420, 530), (420, 563)], "TCP 5432 (sempre no primário)", (652, 524))
seta([(460, 610), (538, 610)], "replicação síncrona a partir do primário", (730, 652), tracejada=True, ancora="middle")
seta([(180, 413), (180, 353)], "saída", (140, 388))
seta([(860, 413), (860, 353)], "saída", (868, 388))
seta([(920, 318), (990, 318), (990, 50), (952, 50)], "saída pelos NAT (cada zona usa o seu), HTTPS 443", (982, 206), ancora="end")
seta([(700, 80), (700, 100), (512, 168)], "webhook do parceiro", (612, 146), tracejada=True)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<defs><marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       f'<path d="M0 0L10 5L0 10z" fill="{LINHA}"/></marker></defs>'
       f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>' + "".join(partes) + "</svg>")
print(svg)
