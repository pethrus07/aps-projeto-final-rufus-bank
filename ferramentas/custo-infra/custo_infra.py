"""Custo mensal de infraestrutura do Rufus Bank na AWS (sa-east-1, Sao Paulo).

Baixa a tabela de precos OFICIAL da AWS (Price List API publica, sem login),
le o preco unitario de cada item, multiplica pelas premissas de uso abaixo e
gera custo-gerado.md. Converte para reais pela PTAX de venda do Banco Central.

Se algum preco nao for encontrado, o script ABORTA: nenhum numero e inventado.

Uso:
    python custo_infra.py            # usa o cache se existir
    python custo_infra.py --baixar   # baixa as tabelas de novo

Conferencia manual: os mesmos itens e quantidades podem ser lancados em
https://calculator.aws (regiao South America (Sao Paulo)); o link salvo da
estimativa vai no README deste bloco.
"""

import datetime as dt
import json
import pathlib
import sys
import urllib.request

AQUI = pathlib.Path(__file__).parent
CACHE = AQUI / "cache"
SAIDA = AQUI / "custo-gerado.md"
URL = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{s}/current/sa-east-1/index.json"
HORAS = 730  # horas em um mes, padrao da propria calculadora da AWS

# (servico, usagetype, trecho obrigatorio na descricao ou None)
PRECOS = {
    "fargate_vcpu": ("AmazonECS", "SAE1-Fargate-ARM-vCPU-Hours:perCPU", None),
    "fargate_gb": ("AmazonECS", "SAE1-Fargate-ARM-GB-Hours", None),
    "rds_medium_maz": ("AmazonRDS", "SAE1-Multi-AZUsage:db.t4g.medium", "running PostgreSQL"),
    "rds_small": ("AmazonRDS", "SAE1-InstanceUsage:db.t4g.small", "running PostgreSQL"),
    "rds_gp3_maz": ("AmazonRDS", "SAE1-RDS:Multi-AZ-GP3-Storage", "running PostgreSQL"),
    "rds_gp3": ("AmazonRDS", "SAE1-RDS:GP3-Storage", "running PostgreSQL"),
    "rds_backup": ("AmazonRDS", "SAE1-RDS:ChargedBackupUsage", "running PostgreSQL"),
    "alb_hora": ("AWSELB", "SAE1-LoadBalancerUsage", "Application"),
    "alb_lcu": ("AWSELB", "SAE1-LCUUsage", "used Application load balancer"),
    "nat_hora": ("AmazonEC2", "SAE1-NatGateway-Hours", None),
    "nat_gb": ("AmazonEC2", "SAE1-NatGateway-Bytes", None),
    "saida_internet_gb": ("AmazonEC2", "SAE1-DataTransfer-Out-Bytes", "remainder of first 10 TB"),
    "ipv4_hora": ("AmazonVPC", "SAE1-PublicIPv4:InUseAddress", None),
    "waf_acl": ("awswaf", "SAE1-WebACLV2", None),
    "waf_regra": ("awswaf", "SAE1-RuleV2", None),
    "waf_req": ("awswaf", "SAE1-RequestV2-Tier1", None),
    "segredo": ("AWSSecretsManager", "SAE1-AWSSecretsManager-Secrets", None),
    "log_gb": ("AmazonCloudWatch", "SAE1-DataProcessing-Bytes", "Standard log class"),
    "log_armazenado_gb": ("AmazonCloudWatch", "SAE1-TimedStorage-ByteHrs", None),
    "alarme": ("AmazonCloudWatch", "SAE1-CW:AlarmMonitorUsage", None),
    "metrica": ("AmazonCloudWatch", "SAE1-CW:MetricMonitorUsage", "first 10,000"),
    "s3_gb": ("AmazonS3", "SAE1-TimedStorage-ByteHrs", "first 50 TB"),
    "ecr_gb": ("AmazonECR", "SAE1-TimedStorage-ByteHrs", None),
    "polly_char": ("AmazonPolly", "SAE1-SynthesizeSpeech-Characters", None),
}

# Premissas de uso. Toda quantidade aqui e citada no 04-viabilidade.md.
# (rotulo, chave de preco, quantidade, unidade legivel)
PROD = [
    ("API: 2 tarefas Fargate ARM (1 por zona), 0,5 vCPU cada", "fargate_vcpu", 2 * 0.5 * HORAS, "vCPU-h"),
    ("API: memória das 2 tarefas, 1 GB cada", "fargate_gb", 2 * 1 * HORAS, "GB-h"),
    ("Worker (filas e notificações): 1 tarefa, 0,25 vCPU", "fargate_vcpu", 0.25 * HORAS, "vCPU-h"),
    ("Worker: memória, 0,5 GB", "fargate_gb", 0.5 * HORAS, "GB-h"),
    ("PostgreSQL RDS db.t4g.medium Multi-AZ", "rds_medium_maz", HORAS, "h"),
    ("Disco do banco: 50 GB gp3 Multi-AZ", "rds_gp3_maz", 50, "GB-mês"),
    ("Backup além da cota grátis (retenção de 35 dias)", "rds_backup", 50, "GB-mês"),
    ("Application Load Balancer", "alb_hora", HORAS, "h"),
    ("ALB: capacidade media de 1 LCU", "alb_lcu", HORAS, "LCU-h"),
    ("NAT Gateway: 2, um por zona", "nat_hora", 2 * HORAS, "h"),
    ("NAT: tráfego de saída para o parceiro BaaS", "nat_gb", 20, "GB"),
    ("Saída para a internet (respostas da API)", "saida_internet_gb", 120, "GB"),
    ("IPv4 público: 2 do ALB e 2 dos NAT", "ipv4_hora", 4 * HORAS, "IP-h"),
    ("WAF: 1 web ACL", "waf_acl", 1, "ACL"),
    ("WAF: 5 regras", "waf_regra", 5, "regras"),
    ("WAF: requisições inspecionadas", "waf_req", 6_000_000, "req"),
    ("Secrets Manager: 10 segredos", "segredo", 10, "segredos"),
    ("CloudWatch Logs: ingestão", "log_gb", 20, "GB"),
    ("CloudWatch Logs: armazenamento (90 dias)", "log_armazenado_gb", 60, "GB-mês"),
    ("CloudWatch: 10 alarmes", "alarme", 10, "alarmes"),
    ("CloudWatch: 20 métricas de negócio", "metrica", 20, "métricas"),
    ("S3: comprovantes, documentos e cache de áudio", "s3_gb", 50, "GB-mês"),
    ("ECR: imagens dos containers", "ecr_gb", 5, "GB-mês"),
    ("Polly: leitura em voz alta (12 mi caracteres)", "polly_char", 12_000_000, "caracteres"),
]

HOMOLOG = [
    ("API: 1 tarefa Fargate ARM, 0,5 vCPU", "fargate_vcpu", 0.5 * HORAS, "vCPU-h"),
    ("API: memória, 1 GB", "fargate_gb", 1 * HORAS, "GB-h"),
    ("Worker: 1 tarefa, 0,25 vCPU", "fargate_vcpu", 0.25 * HORAS, "vCPU-h"),
    ("Worker: memória, 0,5 GB", "fargate_gb", 0.5 * HORAS, "GB-h"),
    ("PostgreSQL RDS db.t4g.small Single-AZ", "rds_small", HORAS, "h"),
    ("Disco do banco: 20 GB gp3", "rds_gp3", 20, "GB-mês"),
    ("Application Load Balancer", "alb_hora", HORAS, "h"),
    ("ALB: capacidade mínima", "alb_lcu", 0.1 * HORAS, "LCU-h"),
    ("NAT Gateway: 1", "nat_hora", HORAS, "h"),
    ("NAT: tráfego", "nat_gb", 2, "GB"),
    ("IPv4 público: 2 do ALB e 1 do NAT", "ipv4_hora", 3 * HORAS, "IP-h"),
    ("Secrets Manager: 10 segredos", "segredo", 10, "segredos"),
    ("CloudWatch Logs: ingestão", "log_gb", 3, "GB"),
    ("S3", "s3_gb", 5, "GB-mês"),
    ("Polly: testes (1 mi caracteres)", "polly_char", 1_000_000, "caracteres"),
]


def baixar(servico, forcar):
    CACHE.mkdir(exist_ok=True)
    arq = CACHE / f"{servico}.json"
    if forcar or not arq.exists():
        print(f"baixando {servico}...", file=sys.stderr)
        urllib.request.urlretrieve(URL.format(s=servico), arq)
    return arq


def precos_unitarios(forcar):
    por_servico = {}
    for chave, (serv, _, _) in PRECOS.items():
        por_servico.setdefault(serv, []).append(chave)
    achados = {}
    for serv, chaves in por_servico.items():
        dados = json.loads(baixar(serv, forcar).read_text(encoding="utf-8"))
        od = dados["terms"]["OnDemand"]
        versao = dados.get("publicationDate", "?")
        for chave in chaves:
            _, usagetype, trecho = PRECOS[chave]
            valores = set()
            for sku, prod in dados["products"].items():
                if prod.get("attributes", {}).get("usagetype") != usagetype:
                    continue
                for termo in od.get(sku, {}).values():
                    for dim in termo["priceDimensions"].values():
                        if trecho and trecho not in dim["description"]:
                            continue
                        valores.add(float(dim["pricePerUnit"]["USD"]))
            if len(valores) != 1:
                sys.exit(f"ABORTADO: {chave} ({usagetype}) deu {sorted(valores)}; esperado 1 preco")
            achados[chave] = (valores.pop(), versao)
    return achados


def ptax():
    fim = dt.date.today()
    ini = fim - dt.timedelta(days=10)
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        f"?@dataInicial='{ini:%m-%d-%Y}'&@dataFinalCotacao='{fim:%m-%d-%Y}'"
        "&$format=json&$select=cotacaoVenda,dataHoraCotacao"
    )
    with urllib.request.urlopen(url) as r:
        ultima = json.load(r)["value"][-1]
    return ultima["cotacaoVenda"], ultima["dataHoraCotacao"][:10]


def brl(v, casas=2):
    """Numero no formato brasileiro: 1.234,56."""
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def unitario(v):
    """Preco unitario sem notacao cientifica: 0,0000006 em vez de 6e-07."""
    txt = f"{v:.8f}".rstrip("0").rstrip(".")
    return txt.replace(".", ",")


def tabela(nome, itens, p, cambio):
    linhas = [f"### {nome}", "", "| Item | Quantidade | Preço unitário (USD) | Total (USD) |", "| --- | --- | --- | --- |"]
    total = 0.0
    for rotulo, chave, qtd, un in itens:
        unit = p[chave][0]
        sub = unit * qtd
        total += sub
        linhas.append(f"| {rotulo} | {brl(qtd, 0)} {un} | {unitario(unit)} | {brl(sub)} |")
    linhas.append(f"| **Total** | | | **{brl(total)}** |")
    linhas += ["", f"Em reais: **R$ {brl(total * cambio)} por mês**.", ""]
    return linhas, total


def main():
    p = precos_unitarios("--baixar" in sys.argv)
    cambio, data_cambio = ptax()
    versoes = sorted({v for _, v in p.values()})
    out = [
        "# Custo mensal de infraestrutura (gerado)",
        "",
        "Arquivo gerado por `custo_infra.py`. Não editar à mão: mude as premissas no script e rode de novo.",
        "",
        f"- Região: AWS sa-east-1 (São Paulo), preço sob demanda, sem desconto de reserva.",
        f"- Tabelas de preço AWS publicadas entre {versoes[0][:10]} e {versoes[-1][:10]}.",
        f"- Câmbio: PTAX de venda de {data_cambio}, R$ {brl(cambio, 4)} por dólar (Banco Central).",
        f"- Gerado em {dt.date.today():%d/%m/%Y}.",
        "",
    ]
    t1, prod = tabela("Produção", PROD, p, cambio)
    t2, hml = tabela("Homologação (staging)", HOMOLOG, p, cambio)
    out += t1 + t2
    out += [
        "### Resumo por ambiente",
        "",
        "| Ambiente | USD por mês | R$ por mês |",
        "| --- | --- | --- |",
        f"| Produção | {brl(prod)} | {brl(prod * cambio)} |",
        f"| Homologação | {brl(hml)} | {brl(hml * cambio)} |",
        "| Desenvolvimento | 0,00 | 0,00 (Docker Compose na máquina do dev) |",
        f"| **Total** | **{brl(prod + hml)}** | **{brl((prod + hml) * cambio)}** |",
        "",
    ]
    SAIDA.write_text("\n".join(out), encoding="utf-8")
    print(f"producao USD {prod:.2f} | homolog USD {hml:.2f} | total R$ {brl((prod + hml) * cambio)}")


if __name__ == "__main__":
    main()
