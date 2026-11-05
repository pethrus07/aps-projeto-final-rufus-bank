# titulo: Diagrama de Deployment, parte 2 de 2 · desenvolvimento local e homologação
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "ferramentas" / "diagramas"))
import svglib as s

d = s.Desenho(900, 830)
NEUTRO = ("#F3F4F6", "#374151", "#111827")
def rot(x, y, t, a="start"): d.rotulo(x, y, t if isinstance(t, list) else [t], tam=12, ancora=a, fundo=False)

# desenvolvimento local
d.no(20, 20, 840, 250, ["Notebook do desenvolvedor"], "«device» Ambiente de desenvolvimento")
d.partes.append('<rect x="40" y="92" width="800" height="160" fill="#FFFFFF" stroke="#374151" stroke-width="1.1"/>')
d.texto(52, 112, "«executionEnvironment» Docker Compose", tam=12, cor="#4B5563", ancora="start", italico=True)
d.artefato(60, 130, 220, 46, ["api · porta 3000"], "«container»")
d.artefato(310, 130, 200, 46, ["worker"], "«container»")
d.artefato(550, 130, 270, 46, ["postgres:17 · porta 5432"], "«container»")
d.seta([(510, 153), (550, 153)])
d.seta([(170, 176), (170, 200), (685, 200), (685, 176)])
rot(420, 194, "TCP 5432", "middle")
d.texto(60, 226, ["App no Expo aponta para http://IP-do-notebook:3000.", "Parceiro BaaS e voz usam adaptadores falsos (ADR-002)."], tam=12, cor="#4B5563", ancora="start")

# homologação na AWS
d.fronteira(20, 300, 840, 510, "AWS sa-east-1 (São Paulo)", "«cloud»", cor="#B45309", posicao="cima-dir")
d.fronteira(40, 340, 460, 450, "«environment» Homologação (1 zona)", None, cor="#1F2937")
d.no(70, 362, 400, 62, ["Load Balancer + WAF"], "«node» HTTPS 443")
d.no(70, 492, 180, 72, ["Tarefa API"], "«Fargate» :3000")
d.no(290, 492, 180, 72, ["Tarefa worker"], "«Fargate»")
d.banco(70, 640, 180, 96, "PostgreSQL 17", [], cores=NEUTRO, tipo="Single-AZ")
d.no(290, 660, 180, 62, ["NAT Gateway"], "«node»")
d.seta([(160, 424), (160, 492)]); rot(168, 462, "HTTP 3000")
d.seta([(160, 564), (160, 640)]); rot(168, 606, "5432")
d.seta([(330, 564), (330, 600), (215, 600), (215, 640)])
d.seta([(420, 564), (420, 660)]); rot(428, 616, "443")
d.texto(540, 400, ["Mesmo desenho da produção,", "numa zona só, com banco", "Single-AZ e um NAT.", "", "Custo no Bloco 1:", "US$ 207,50 por mês."], tam=12.5, cor="#374151", ancora="start")
print(d.svg())
