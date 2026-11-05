"""Gera de novo tudo o que é derivado de dados, na ordem certa, e para no primeiro erro.

  1. custo de infraestrutura (tabela oficial da AWS + PTAX)       ferramentas/custo-infra
  2. planejamento: estimativa, equipe e custo total do projeto    bloco-7-planejamento
  3. banco: testes do schema e dicionário de dados (precisa do Docker; pule com --sem-banco)
  4. protótipos de interface (Chrome headless)                    bloco-2-requisitos/prototipos
  5. diagramas com título, autores e data                         */diagramas
  6. AID em PDF, com auditoria                                    entrega/AID-Rufus-Bank.pdf
  7. slides da apresentação                                       apresentacao/Rufus-Bank-Apresentacao.pptx

Uso:  python -I ferramentas/gerar-tudo.py [--sem-banco] [--baixar]
"""

import pathlib
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PY = [sys.executable, "-I"]
sem_banco = "--sem-banco" in sys.argv
baixar = ["--baixar"] if "--baixar" in sys.argv else []

ETAPAS = [
    ("custo de infraestrutura", PY + ["ferramentas/custo-infra/custo_infra.py", *baixar]),
    ("planejamento", PY + ["bloco-7-planejamento/ferramentas/planejamento.py"]),
]
if not sem_banco:
    ETAPAS += [
        ("testes do schema no PostgreSQL", ["bash", "bloco-5-banco/testes/testar-schema.sh"]),
        ("dicionário de dados", PY + ["bloco-5-banco/ferramentas/gerar_dicionario.py"]),
    ]
ETAPAS += [
    ("protótipos de interface", PY + ["bloco-2-requisitos/prototipos/src/gerar_prototipos.py"]),
    ("diagramas", PY + ["ferramentas/diagramas/gerar.py"]),
    ("AID em PDF", PY + ["ferramentas/aid/build.py"]),
    ("slides", ["node", "apresentacao/gerador/gerar-slides.js"]),
]

for nome, cmd in ETAPAS:
    print(f"== {nome}", flush=True)
    r = subprocess.run(cmd, cwd=RAIZ)
    if r.returncode != 0:
        sys.exit(f"ABORTADO na etapa: {nome}")
print("tudo gerado")
