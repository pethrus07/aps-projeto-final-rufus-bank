"""Planejamento do Rufus Bank: backlog, capacidade, sprints, equipe e custo.

Gera, sem nenhum número digitado à mão nos documentos:
  - bloco-7-planejamento/02-estimativas.md
  - bloco-7-planejamento/03-equipe-e-custo.md
  - bloco-7-planejamento/diagramas/cronograma.mmd  (gantt, renderizado por ferramentas/diagramas/gerar.py)

Entradas:
  - as histórias e os pontos são lidos de bloco-2-requisitos/03-historias-de-usuario.md
  - o custo mensal de infraestrutura e o câmbio são lidos de ferramentas/custo-infra/custo-gerado.md
  - salários: tabela SALARIOS abaixo, cada um com a URL de onde saiu (consultada em 04/11/2026)

O script ABORTA se: uma história do Bloco 2 ficar fora do plano, um sprint passar
da capacidade, ou os pontos lidos do Bloco 2 não baterem com a soma do plano.

Uso: python -I bloco-7-planejamento/ferramentas/planejamento.py
"""

import datetime as dt
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
B7 = RAIZ / "bloco-7-planejamento"

# ---------------------------------------------------------------- calendário
INICIO = dt.date(2026, 11, 16)  # segunda-feira
DURACAO_SPRINT = 14  # dias corridos, 10 dias úteis
FERIADOS = {
    dt.date(2026, 11, 20): "Dia da Consciência Negra (feriado nacional)",
    dt.date(2026, 12, 25): "Natal",
    dt.date(2027, 1, 1): "Confraternização Universal",
    dt.date(2027, 2, 8): "Carnaval (segunda, ponto facultativo)",
    dt.date(2027, 2, 9): "Carnaval (terça, ponto facultativo)",
    dt.date(2027, 3, 26): "Sexta-feira Santa",
}

# ---------------------------------------------------------------- equipe
# salário mensal bruto (R$), mediana (50º percentil) da fonte, cidade de referência Recife
SALARIOS = {
    "Product Owner": (8750, "Robert Half, Guia Salarial 2027, Product Owner - PO, Recife, 50º percentil",
                      "https://www.roberthalf.com/br/pt/vagas-detalhes/product-owner-po/recife"),
    "Tech Lead (Back-End Sênior)": (14500, "Robert Half, Guia Salarial 2027, Desenvolvedor(a) Back-End Sênior, Recife, 50º percentil",
                                    "https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-senior/recife"),
    "Desenvolvedor Back-End Pleno": (11800, "Robert Half, Guia Salarial 2027, Desenvolvedor(a) Back-End Pleno, Recife, 50º percentil",
                                     "https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-pleno/recife"),
    "Desenvolvedor Mobile Pleno (React Native)": (13800, "Robert Half, Guia Salarial 2027, Desenvolvedor(a) Mobile Pleno, Recife, 50º percentil",
                                                  "https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-mobile-pleno/recife"),
    "Analista de Testes Pleno (QA)": (9100, "Robert Half, Guia Salarial 2027, Analista de Testes Pleno, Recife, 50º percentil",
                                      "https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-testes-pleno/recife"),
    "Analista de DevOps": (14600, "Robert Half, Guia Salarial 2027, Analista de DevOps, Recife, 50º percentil",
                           "https://www.roberthalf.com/br/pt/vagas-detalhes/analista-de-devops/recife"),
    "Designer UX/UI": (3344.38, "Salário.com.br, Designer de UX (CBO 2624-10), Recife-PE, média com dados do Novo CAGED, atualizado em 08/10/2026",
                       "https://www.salario.com.br/profissao/designer-ux-cbo-262410/recife-pe/"),
}
# (perfil, quantidade, alocação de 0 a 1, produz story points?)
EQUIPE = [
    ("Product Owner", 1, 1.0, False),
    ("Tech Lead (Back-End Sênior)", 1, 1.0, True),
    ("Desenvolvedor Back-End Pleno", 1, 1.0, True),
    ("Desenvolvedor Mobile Pleno (React Native)", 2, 1.0, True),
    ("Analista de DevOps", 1, 0.5, True),
    ("Analista de Testes Pleno (QA)", 1, 1.0, False),
    ("Designer UX/UI", 1, 1.0, False),
]
PAPEL_DO_PERFIL = {  # o que cada um faz no projeto
    "Product Owner": "Backlog, prioridade MoSCoW, aceite das histórias, contato com o parceiro BaaS",
    "Tech Lead (Back-End Sênior)": "Arquitetura, revisão de código, módulos de identidade, contas e pagamentos",
    "Desenvolvedor Back-End Pleno": "Módulos de família, antifraude, atendimento, notificação e integrações",
    "Desenvolvedor Mobile Pleno (React Native)": "App Android e iOS, acessibilidade, voz, câmera e biometria",
    "Analista de DevOps": "Terraform, pipeline, observabilidade, backup. Meio período: o trabalho pesado é no início e no lançamento",
    "Analista de Testes Pleno (QA)": "Testes automatizados de integração e E2E, teste de carga, testes com usuários junto com o UX",
    "Designer UX/UI": "Telas, linguagem simples, roteiro de áudio, teste de uso com pessoas do perfil a cada sprint",
}

# encargos sobre a folha, empresa no Lucro Presumido ou Real, sem desoneração (CPRB)
ENCARGOS = [
    ("INSS patronal", 0.20, "Lei 8.212/1991, art. 22, I"),
    ("RAT/SAT (risco leve, FAP 1,0)", 0.01, "Lei 8.212/1991, art. 22, II, a. Desenvolvimento de software é grau de risco leve"),
    ("Terceiros (Sistema S, salário-educação, INCRA)", 0.058, "Contribuições de terceiros da guia do INSS"),
    ("FGTS", 0.08, "Lei 8.036/1990, art. 15"),
]
PROVISOES = [
    ("13º salário", 1 / 12, "1 salário por ano, dividido em 12 meses"),
    ("Férias + 1/3", (1 / 12) * (4 / 3), "1 salário + 1/3 por ano, dividido em 12 meses"),
]

# ---------------------------------------------------------------- velocidade
VELOCIDADE_BASE = 34  # SP por sprint com a equipe completa e 10 dias úteis
RAMPA = {0: 0.6, 1: 0.8}  # sprint 0 e sprint 1 rendem menos (setup e adaptação)

# ---------------------------------------------------------------- backlog técnico (habilitadores)
TECNICAS = {
    "T01": ("Repositório, padrões de código, lint e estrutura de módulos", 3, "Plataforma"),
    "T02": ("Terraform: VPC, subnets, NAT, ALB e WAF", 8, "Plataforma"),
    "T03": ("Terraform: ECS Fargate, RDS Multi-AZ, Secrets Manager e ECR (homologação e produção)", 8, "Plataforma"),
    "T04": ("Pipeline de CI: lint, testes, build e varredura de segurança", 5, "Plataforma"),
    "T05": ("Pipeline de CD: homologação, smoke test, aprovação e produção", 5, "Plataforma"),
    "T06": ("Esqueleto da API NestJS: módulos, configuração, /health, log pino com correlação", 5, "Plataforma"),
    "T07": ("Migrações e razão contábil: carteiras, lançamentos e gatilho de soma zero", 8, "Plataforma"),
    "T08": ("Outbox transacional e worker com SKIP LOCKED e nova tentativa", 5, "Plataforma"),
    "T09": ("Porta bancária e adaptador falso do parceiro BaaS", 5, "Integrações"),
    "T10": ("Adaptador real do parceiro BaaS (sandbox) e webhooks com HMAC", 8, "Integrações"),
    "T11": ("Porta de voz: Amazon Polly, cache no S3 e voz do celular sem internet", 5, "Integrações"),
    "T12": ("Esqueleto do app Expo: navegação, tema acessível, botão Ouvir, cliente gerado do OpenAPI", 8, "Plataforma"),
    "T13": ("Esqueleto do painel interno (React e Vite) com login e TOTP", 5, "Plataforma"),
    "T14": ("Observabilidade: painéis e alarmes do RNF01, RNF03 e RNF13", 3, "Qualidade"),
    "T15": ("Segurança: revisão OWASP, teste de invasão externo e correções", 8, "Qualidade"),
    "T16": ("Teste de carga com k6 (RNF04)", 3, "Qualidade"),
    "T17": ("Auditoria de acessibilidade WCAG 2.2 AA (RNF09)", 5, "Qualidade"),
    "T18": ("Conciliação diária com o parceiro (RNF11)", 5, "Integrações"),
    "T19": ("Publicação nas lojas: contas, revisão da Apple e do Google", 3, "Implantação"),
    "T20": ("Teste de restauração de backup (RNF12)", 2, "Qualidade"),
}

# ---------------------------------------------------------------- plano: item -> sprint
PLANO = {
    0: ["T01", "T06", "T04", "T09"],
    1: ["T12", "T07", "US02", "T11"],
    2: ["US01", "US04", "T08", "T02"],
    3: ["T03", "T05", "US06", "US07", "US05"],
    4: ["US08", "US11", "US12", "US03", "T13", "US16"],
    5: ["T10", "US09", "US10", "US14", "US15", "T18"],
    6: ["US17", "US13", "US18", "US20", "US21", "US22", "US19"],
    7: ["T15", "T16", "T17", "T20", "T14", "US23", "US24", "T19"],
    8: [],  # beta fechado, correções e lançamento: capacidade inteira como reserva
}
OBJETIVOS = {
    0: "Fundação: repositório, pipeline de CI, esqueleto da API e parceiro falso",
    1: "Antônio entra com a digital num app que fala",
    2: "Antônio abre a conta sozinho e ouve o saldo",
    3: "Enviar e receber Pix sem duplicar, com infraestrutura de homologação e produção",
    4: "Boleto, proteção contra golpe e primeira fila do antifraude",
    5: "Conta da Camila e atendimento humano, já com o parceiro real",
    6: "Rede de apoio (contato de confiança, aprovação) e direitos LGPD",
    7: "Segurança, carga, acessibilidade e publicação nas lojas",
    8: "Beta fechado com 50 pessoas do perfil, correções e lançamento",
}
INICIO_PRODUCAO_SPRINT = 7  # o ambiente de produção passa a ser cobrado neste sprint (beta no sprint 8)


def ler_historias():
    txt = (RAIZ / "bloco-2-requisitos/03-historias-de-usuario.md").read_text(encoding="utf-8")
    hs = {}
    for m in re.finditer(r"^\| (US\d\d) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| (\w+'?\w*) \| (\d+) \|", txt, re.M):
        hs[m.group(1)] = (m.group(3).strip(), int(m.group(6)), m.group(5), m.group(2).strip())
    total = int(re.search(r"\*\*Total\*\* \| \| \| \*\*(\d+)\*\*", txt).group(1))
    if sum(h[1] for h in hs.values()) != total or len(hs) != 24:
        sys.exit(f"ABORTADO: li {len(hs)} histórias e {sum(h[1] for h in hs.values())} pontos; o Bloco 2 diz {total}")
    return hs


def ler_infra():
    txt = (RAIZ / "ferramentas/custo-infra/custo-gerado.md").read_text(encoding="utf-8")
    def valor(rotulo):
        m = re.search(rf"\| {rotulo} \| [\d.,]+ \| ([\d.,]+) \|", txt)
        return float(m.group(1).replace(".", "").replace(",", "."))
    cambio = float(re.search(r"R\$ ([\d,]+) por dólar", txt).group(1).replace(",", "."))
    total = float(re.search(r"\| \*\*Total\*\* \| \*\*[\d.,]+\*\* \| \*\*([\d.,]+)\*\* \|", txt).group(1).replace(".", "").replace(",", "."))
    unicos = float(re.search(r"Custos únicos \(antes do lançamento\): \*\*R\$ ([\d.,]+)\*\*", txt).group(1).replace(".", "").replace(",", "."))
    return valor("Produção"), valor("Homologação"), valor("Serviços fora da AWS"), cambio, total, unicos


def brl(v, casas=2):
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def dias_uteis(ini, fim):
    d, n, fer = ini, 0, []
    while d <= fim:
        if d.weekday() < 5:
            if d in FERIADOS:
                fer.append(f"{d:%d/%m} {FERIADOS[d]}")
            else:
                n += 1
        d += dt.timedelta(days=1)
    return n, fer


def main():
    hs = ler_historias()
    infra_prod, infra_hml, infra_ext, cambio, infra_total, infra_unicos = ler_infra()

    itens = {k: (v[0], v[1], "Técnica", v[2]) for k, v in TECNICAS.items()}
    for k, (titulo, sp, prio, persona) in hs.items():
        itens[k] = (f"{persona}: {titulo}", sp, prio, "Produto")

    planejados = [i for s in PLANO.values() for i in s]
    faltando = set(itens) - set(planejados)
    repetidos = {i for i in planejados if planejados.count(i) > 1}
    if faltando or repetidos:
        sys.exit(f"ABORTADO: fora do plano {sorted(faltando)}, repetidos {sorted(repetidos)}")

    sprints = []
    for n in sorted(PLANO):
        ini = INICIO + dt.timedelta(days=DURACAO_SPRINT * n)
        fim = ini + dt.timedelta(days=11)  # sexta da 2ª semana
        du, fer = dias_uteis(ini, fim)
        cap = VELOCIDADE_BASE * RAMPA.get(n, 1.0) * du / 10
        pts = sum(itens[i][1] for i in PLANO[n])
        if pts > cap:
            sys.exit(f"ABORTADO: sprint {n} tem {pts} SP e capacidade {cap:.1f}")
        sprints.append(dict(n=n, ini=ini, fim=fim, du=du, fer=fer, cap=cap, pts=pts, itens=PLANO[n]))

    total_sp = sum(v[1] for v in itens.values())
    sp_us = sum(h[1] for h in hs.values())
    sp_tec = sum(v[1] for v in TECNICAS.values())
    fim_projeto = sprints[-1]["fim"]
    semanas = (fim_projeto - INICIO).days / 7
    meses = semanas * 12 / 52
    cap_total_dev = sum(s["cap"] for s in sprints if s["itens"])
    devs_eq = sum(q * a for _, q, a, prod in EQUIPE if prod)

    # ---------------------------------------------------------- estimativas.md
    L = [
        "# 7.2 Estimativa de esforço e cronograma",
        "",
        "> Arquivo gerado por `ferramentas/planejamento.py`. Não editar à mão: mude o plano no script e rode de novo.",
        "",
        f"O MVP soma **{total_sp} story points**: {sp_us} das 24 histórias do Bloco 2 e {sp_tec} de tarefas técnicas. "
        f"Com a equipe do item 7.3, isso cabe em **{len(sprints)} sprints de 2 semanas**, de "
        f"{INICIO:%d/%m/%Y} a {fim_projeto:%d/%m/%Y} ({semanas:.0f} semanas). O último sprint não tem item novo: "
        "é a reserva para o beta fechado e as correções.",
        "",
        "## Velocidade da equipe",
        "",
        f"- Quem produz story points: 2 devs de back-end, 2 devs mobile e o DevOps em meio período, "
        f"**{brl(devs_eq, 1)} pessoas equivalentes**. PO, QA e UX não pontuam: o trabalho deles está dentro da Definition of Done de cada história.",
        f"- Velocidade de referência: **{VELOCIDADE_BASE} SP por sprint** com a equipe completa e 10 dias úteis, cerca de "
        f"{brl(VELOCIDADE_BASE / devs_eq, 1)} pontos por pessoa por sprint. A referência de tamanho é a US13 = 3 pontos (Bloco 2).",
        f"- Rampa: o sprint 0 rende {int(RAMPA[0] * 100)}% (montagem do ambiente, equipe nova) e o sprint 1 rende {int(RAMPA[1] * 100)}%.",
        "- Feriados e pontos facultativos reduzem a capacidade na proporção dos dias úteis perdidos.",
        "- A velocidade é uma hipótese. Depois do sprint 2 ela é recalculada pela média dos sprints anteriores e o plano é refeito.",
        "",
        "## Sprints",
        "",
        "| Sprint | Período | Dias úteis | Capacidade (SP) | Planejado (SP) | Uso | Objetivo |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in sprints:
        uso = f"{100 * s['pts'] / s['cap']:.0f}%" if s["itens"] else "reserva"
        L.append(f"| {s['n']} | {s['ini']:%d/%m/%Y} a {s['fim']:%d/%m/%Y} | {s['du']} | {brl(s['cap'], 1)} | {s['pts']} | {uso} | {OBJETIVOS[s['n']]} |")
    L += [
        f"| **Total** | | | **{brl(sum(s['cap'] for s in sprints), 1)}** | **{total_sp}** | | |",
        "",
        f"Nos sprints com itens (0 a {len(sprints) - 2}), a capacidade é de {brl(cap_total_dev, 1)} SP para {total_sp} planejados: "
        f"uso de {100 * total_sp / cap_total_dev:.0f}%, com folga para imprevisto. O sprint {len(sprints) - 1} inteiro é reserva.",
        "",
        "Feriados considerados: " + "; ".join(f"{d:%d/%m/%Y} {n}" for d, n in FERIADOS.items()) + ".",
        "",
        "![Cronograma em sprints](diagramas/img/cronograma.svg)",
        "",
        "## O que entra em cada sprint",
        "",
        "Ordem: primeiro o que destrava os outros (plataforma, razão contábil, parceiro falso), depois os Must na ordem do fluxo do cliente, depois os Should e por fim os Could. Todo Must termina até o sprint 6.",
        "",
    ]
    for s in sprints:
        L.append(f"### Sprint {s['n']} · {s['ini']:%d/%m} a {s['fim']:%d/%m/%Y} · {OBJETIVOS[s['n']]}")
        L.append("")
        if not s["itens"]:
            L += ["Sem item novo. Beta fechado com 50 pessoas do perfil das personas, correção do que aparecer, lançamento controlado.", ""]
            continue
        L += ["| Item | Descrição | Tipo | Prioridade | SP |", "| --- | --- | --- | --- | --- |"]
        for i in s["itens"]:
            desc, sp, prio, tipo = itens[i]
            L.append(f"| {i} | {desc} | {tipo} | {prio} | {sp} |")
        L += [f"| | **Total** | | | **{s['pts']}** |", ""]
    L += [
        "## Tarefas técnicas",
        "",
        "| ID | Tarefa | Grupo da WBS | SP | Sprint |",
        "| --- | --- | --- | --- | --- |",
    ]
    onde = {i: s["n"] for s in sprints for i in s["itens"]}
    for k, (desc, sp, grupo) in TECNICAS.items():
        L.append(f"| {k} | {desc} | {grupo} | {sp} | {onde[k]} |")
    L += [f"| | **Total** | | **{sp_tec}** | |", ""]
    L += [
        "## Histórias por prioridade",
        "",
        "| Prioridade | Histórias | SP | Último sprint |",
        "| --- | --- | --- | --- |",
    ]
    for prio in ("Must", "Should", "Could"):
        ids = [k for k, h in hs.items() if h[2] == prio]
        L.append(f"| {prio} | {len(ids)} | {sum(hs[k][1] for k in ids)} | {max(onde[k] for k in ids)} |")
    (B7 / "02-estimativas.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------------------------------------------------------- cronograma.mmd
    G = ["%% titulo: Cronograma do MVP em sprints de 2 semanas",
         "%%{init: {'gantt': {'leftPadding': 210, 'useWidth': 1500, 'rightPadding': 40, 'barHeight': 26, 'barGap': 8, 'fontSize': 14, 'sectionFontSize': 14}}}%%",
         "gantt", "    dateFormat YYYY-MM-DD",
         "    axisFormat %d/%m", "    tickInterval 2week", "    todayMarker off"]
    secoes = [("Fundação e plataforma", [0, 1]), ("Fluxo do cliente (Must)", [2, 3, 4, 5]),
              ("Rede de apoio e LGPD", [6]), ("Qualidade e lojas", [7]), ("Beta e lançamento", [8])]
    for nome, ns in secoes:
        G.append(f"    section {nome}")
        for n in ns:
            s = sprints[n]
            G.append(f"    S{n} {s['pts']} SP :s{n}, {s['ini']:%Y-%m-%d}, {s['fim']:%Y-%m-%d}" if s["itens"]
                     else f"    S{n} reserva :crit, s{n}, {s['ini']:%Y-%m-%d}, {s['fim']:%Y-%m-%d}")
    G.append(f"    Lançamento :milestone, m1, {fim_projeto:%Y-%m-%d}, 0d")
    (B7 / "diagramas").mkdir(exist_ok=True)
    (B7 / "diagramas/cronograma.mmd").write_text("\n".join(G) + "\n", encoding="utf-8")

    # ---------------------------------------------------------- equipe-e-custo.md
    fator_enc = sum(e[1] for e in ENCARGOS)
    fator_prov = sum(p[1] for p in PROVISOES)
    fator = (1 + fator_prov) * (1 + fator_enc)
    linhas_eq, mensal = [], 0.0
    for perfil, q, aloc, _ in EQUIPE:
        sal = SALARIOS[perfil][0]
        custo = sal * fator * q * aloc
        mensal += custo
        linhas_eq.append((perfil, q, aloc, sal, custo))
    custo_equipe = mensal * meses
    meses_prod = (fim_projeto - sprints[INICIO_PRODUCAO_SPRINT]["ini"]).days / 7 * 12 / 52
    custo_infra_hml = infra_hml * meses
    custo_infra_prod = infra_prod * meses_prod
    custo_ext = infra_ext * meses
    total = custo_equipe + custo_infra_hml + custo_infra_prod + custo_ext + infra_unicos

    E = [
        "# 7.3 Composição da equipe e custo do projeto",
        "",
        "> Arquivo gerado por `ferramentas/planejamento.py`. Não editar à mão.",
        "",
        f"A equipe tem **{sum(q for _, q, _, _ in EQUIPE)} pessoas** e custa **R$ {brl(mensal)} por mês** com encargos. "
        f"O projeto dura {brl(meses, 2)} meses ({INICIO:%d/%m/%Y} a {fim_projeto:%d/%m/%Y}) e custa "
        f"**R$ {brl(total)}** no total, somando equipe, infraestrutura do Bloco 1, serviços fora da AWS e custos únicos (conta do Google Play e teste de invasão).",
        "",
        "## Pesquisa salarial: de onde vêm os números",
        "",
        "- **Glassdoor (exigido no enunciado):** tentamos abrir as páginas de salário do glassdoor.com.br em 04/11/2026 "
        "e o site recusou o acesso automático (HTTP 403, exige login). Por isso nenhum valor desta tabela é do Glassdoor. "
        "A coluna de conferência abaixo fica para o grupo preencher abrindo o Glassdoor logado.",
        "- **Robert Half, Guia Salarial 2027:** fonte principal. Usamos a **mediana (50º percentil) de Recife**, a cidade com página no guia mais próxima de João Pessoa, onde a equipe trabalha.",
        "- **Designer UX/UI:** o guia da Robert Half não tem o cargo em Recife. Usamos a média do Novo CAGED para Designer de UX em Recife (Salário.com.br). "
        "É a média de todos os níveis com carteira assinada e provavelmente fica abaixo de um pleno: é o número mais fraco da tabela.",
        "",
        "| Perfil | Salário mensal (R$) | Fonte | Glassdoor (conferência do grupo) |",
        "| --- | --- | --- | --- |",
    ]
    for perfil, _, _, _ in EQUIPE:
        sal, desc, url = SALARIOS[perfil]
        E.append(f"| {perfil} | {brl(sal)} | [{desc}]({url}) | a preencher |")
    E += [
        "",
        "## Perfis, quantidade e por quê",
        "",
        "| Perfil | Qtd. | Alocação | O que faz no projeto |",
        "| --- | --- | --- | --- |",
    ]
    for perfil, q, aloc, _ in EQUIPE:
        E.append(f"| {perfil} | {q} | {int(aloc * 100)}% | {PAPEL_DO_PERFIL[perfil]} |")
    E += [
        "",
        "Por que este tamanho: o ADR-001 (monolito modular) foi pensado para **2 devs de back-end**, e o app em React Native (ADR-005) para **2 devs mobile** cobrirem Android e iOS. "
        "Sem QA dedicado, os testes de integração e com usuários (RNF08) ficariam com os devs e a velocidade cairia. "
        "O UX é tempo integral porque a interface é o produto: cada tela passa por teste de uso com pessoas do perfil das personas.",
        "",
        "## Encargos CLT: a conta",
        "",
        "Empresa no Lucro Presumido ou Real, sem a desoneração da folha (CPRB). Encargos sobre o salário:",
        "",
        "| Encargo | Alíquota | Base legal |",
        "| --- | --- | --- |",
    ]
    for nome, aliq, base in ENCARGOS:
        E.append(f"| {nome} | {brl(aliq * 100, 1)}% | {base} |")
    E += [f"| **Total de encargos** | **{brl(fator_enc * 100, 1)}%** | |", "", "Provisões mensais:", "",
          "| Provisão | % do salário por mês | Conta |", "| --- | --- | --- |"]
    for nome, p, conta in PROVISOES:
        E.append(f"| {nome} | {brl(p * 100, 2)}% | {conta} |")
    E += [
        f"| **Total de provisões** | **{brl(fator_prov * 100, 2)}%** | |",
        "",
        "Os encargos também incidem sobre o 13º e as férias, então o fator é:",
        "",
        f"**custo mensal = salário x (1 + {brl(fator_prov, 4)}) x (1 + {brl(fator_enc, 3)}) = salário x {brl(fator, 4)}**",
        "",
        "## Custo mensal da equipe",
        "",
        "| Perfil | Qtd. | Alocação | Salário (R$) | Custo mensal com encargos (R$) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for perfil, q, aloc, sal, custo in linhas_eq:
        E.append(f"| {perfil} | {q} | {int(aloc * 100)}% | {brl(sal)} | {brl(custo)} |")
    E += [
        f"| **Total** | **{sum(q for _, q, _, _ in EQUIPE)}** | | | **{brl(mensal)}** |",
        "",
        "## Custo total do projeto",
        "",
        "| Item | Conta | R$ |",
        "| --- | --- | --- |",
        f"| Equipe | R$ {brl(mensal)} x {brl(meses, 2)} meses | {brl(custo_equipe)} |",
        f"| Infra de homologação (Bloco 1) | R$ {brl(infra_hml)} x {brl(meses, 2)} meses | {brl(custo_infra_hml)} |",
        f"| Infra de produção (Bloco 1), a partir do sprint {INICIO_PRODUCAO_SPRINT} | R$ {brl(infra_prod)} x {brl(meses_prod, 2)} meses | {brl(custo_infra_prod)} |",
        f"| Serviços fora da AWS (Bloco 1, item 4.4: Expo, GitHub, domínio, conta Apple) | R$ {brl(infra_ext)} x {brl(meses, 2)} meses | {brl(custo_ext)} |",
        f"| Custos únicos (Bloco 1, item 4.4: conta do Google Play e teste de invasão) | valor único | {brl(infra_unicos)} |",
        f"| **Total** | | **{brl(total)}** |",
        "",
        "Meses = semanas do projeto x 12 / 52. Câmbio: a mesma PTAX do Bloco 1.",
        "",
        "## Fora deste valor (precisa de cotação)",
        "",
        "- Benefícios (vale-refeição, plano de saúde) e provisão de multa rescisória do FGTS.",
        "- Cotação formal do teste de invasão (tarefa T15): o total usa o teto da faixa de mercado, R$ 25.000.",
        "- Tarifa do parceiro BaaS por conta e por transação: depende de contrato (Bloco 1).",
        "- Equipamentos, licenças de software e espaço de trabalho.",
        "",
        f"Depois do lançamento, a operação custa por mês a infraestrutura do Bloco 1 (R$ {brl(infra_total)}) mais a equipe que ficar para evoluir o produto.",
    ]
    (B7 / "03-equipe-e-custo.md").write_text("\n".join(E) + "\n", encoding="utf-8")

    print(f"SP {total_sp} ({sp_us} US + {sp_tec} técnicas) | {len(sprints)} sprints | fim {fim_projeto:%d/%m/%Y} | "
          f"{meses:.2f} meses | equipe R$ {brl(mensal)}/mês | total R$ {brl(total)}")


if __name__ == "__main__":
    main()
