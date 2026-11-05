# Rufus Bank · Projeto Final de APS

**"Rufus, iluminando sua vida financeira."** Banco digital com interface simples e linguagem clara para quem os bancos atuais atendem mal: pessoas com pouca leitura, idosos e adolescentes.

Projeto final da disciplina Análise e Projeto de Sistemas (UNIPÊ, 2026.2), "Da Concepção ao Dia 1 do Dev". O trabalho não é implementar: é projetar e documentar o sistema inteiro antes do código, com toda decisão justificada. O enunciado está em [material/enunciado-projeto-final-aps.pdf](material/enunciado-projeto-final-aps.pdf).

## Equipe

| Papel | Responsável | Entrega |
| --- | --- | --- |
| Analista / PO | Pedro Oliveira | Visão, personas, requisitos, histórias, MoSCoW |
| Arquiteto de Software | Izaias Terto | ADR, C4, stack, padrões, diagramas UML |
| Engenheiro / DBA | Carlos Eduardo | Banco, infra cloud, CI/CD, segurança, custos |

Na arguição o professor pergunta qualquer parte para qualquer integrante. Todo mundo precisa saber explicar tudo.

## Blocos

| Bloco | Tema | Status |
| --- | --- | --- |
| 1 | [Concepção e Escopo](bloco-1-concepcao/) | Rascunho completo, em revisão pelo grupo |
| 2 | Requisitos | A fazer |
| 3 | Arquitetura de Software | A fazer |
| 4 | Diagramas UML | A fazer |
| 5 | Banco de Dados | A fazer |
| 6 | Infraestrutura e DevOps (opcional) | A fazer |
| 7 | Planejamento e Estimativas | A fazer |
| 8 | Documentação para o Dev | A fazer |
| 9 | Qualidade e Processo | A fazer |

Entrega extra: o Documento de Apoio (AID) em PDF, com sumário e os 9 blocos na ordem, vale até 1,5 ponto e precisa ser entregue antes do primeiro grupo apresentar.

## Estrutura

```
bloco-1-concepcao/       um arquivo por item do enunciado
ferramentas/custo-infra/ script que calcula o custo da AWS com preço oficial
material/                enunciado do professor
```

## Como recalcular o custo de infraestrutura

Precisa só de Python 3, sem bibliotecas extras.

```
cd ferramentas/custo-infra
python custo_infra.py --baixar
```

O script baixa a tabela oficial de preços da AWS para São Paulo (cerca de 300 MB, guardados em `cache/`, fora do git), pega a PTAX do dia no Banco Central e regrava `custo-gerado.md`. Para mudar a infraestrutura, mude as listas `PROD` e `HOMOLOG` no começo do script e rode de novo.
