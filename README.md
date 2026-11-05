# Rufus Bank · Projeto Final de APS

**"Rufus, iluminando sua vida financeira."** Banco digital com interface simples e linguagem clara para quem os bancos atuais atendem mal: pessoas com pouca leitura, idosos e adolescentes.

Projeto final da disciplina Análise e Projeto de Sistemas (UNIPÊ, 2026.2, Prof. Israel Cunha), "Da Concepção ao Dia 1 do Dev". O trabalho não é implementar: é projetar e documentar o sistema inteiro antes do código, com toda decisão justificada contra a alternativa descartada. O enunciado está em [material/enunciado-projeto-final-aps.pdf](material/enunciado-projeto-final-aps.pdf).

## Entregas

| Entrega | Arquivo |
| --- | --- |
| Documento de Apoio (AID), PDF com sumário e os 9 blocos | [entrega/AID-Rufus-Bank.pdf](entrega/AID-Rufus-Bank.pdf) |
| Apresentação (10 minutos), com notas de fala por integrante | [apresentacao/Rufus-Bank-Apresentacao.pptx](apresentacao/Rufus-Bank-Apresentacao.pptx) |
| Preparação para a arguição | [apresentacao/arguicao.md](apresentacao/arguicao.md) |
| O repositório que o dev recebe no dia 1 | [codigo/](codigo/) |

## Equipe

| Papel | Responsável | Apresenta |
| --- | --- | --- |
| Analista / PO | Pedro Oliveira | Produto, personas, requisitos, histórias, interface |
| Arquiteto de Software | Izaias Terto | ADR, C4, stack, padrões, diagramas UML e BPMN |
| Engenheiro / DBA | Carlos Eduardo | Banco, infraestrutura, custo, CI/CD, segurança |

Na arguição o professor pergunta qualquer parte para qualquer integrante. Todo mundo precisa saber explicar tudo. Os nomes ficam em [projeto.json](projeto.json) e entram em todos os diagramas.

## Conteúdo

| | Tema | O que tem |
| --- | --- | --- |
| | [A disciplina no projeto](00-a-disciplina-no-projeto.md) | Onde cada conceito das Aulas 01 a 05 aparece |
| 1 | [Concepção e Escopo](bloco-1-concepcao/) | Visão com dados oficiais, SWOT, 3 personas, 10 stakeholders, viabilidade com as 4 perguntas e custo real, 8 riscos |
| 2 | [Requisitos](bloco-2-requisitos/) | Processo de ER em 6 passos, 32 RF, 14 RNF classificados, 24 histórias em 7 épicos, 16 regras de negócio, design de interface com protótipos |
| 3 | [Arquitetura](bloco-3-arquitetura/) | 13 ADRs, C4 nos 4 níveis, stack, padrões, modelo de domínio e rotas |
| 4 | [UML e BPMN](bloco-4-uml/) | Os 9 diagramas UML exigidos e 2 processos em BPMN 2.0 |
| 5 | [Banco de Dados](bloco-5-banco/) | Decisão, conceitual, lógico, DDL testado em PostgreSQL 17, dicionário gerado, estratégia |
| 6 | [Infraestrutura e DevOps](bloco-6-infra/) | Diagrama com custo, CI/CD, containers, segurança OWASP, observabilidade |
| 7 | [Planejamento](bloco-7-planejamento/) | WBS, 221 SP em 9 sprints, equipe e custo com pesquisa salarial, 12 riscos |
| 8 | [Documentação para o Dev](bloco-8-dev/) | README do clone ao localhost, variáveis, OpenAPI 3.0, padrões, git workflow, Sprint 1 |
| 9 | [Qualidade e Processo](bloco-9-qualidade/) | Glossário, testes, cobertura, DoR, DoD, ciclo de vida e metodologia |
| | [Fontes e referências](fontes.md) | Toda fonte com link, as leis artigo por artigo e a bibliografia da disciplina |

## Nada é digitado à mão

Os números que vêm de dados são gerados por script, e cada script para com erro se um dado faltar:

| O quê | Script |
| --- | --- |
| Custo de infraestrutura, da tabela oficial da AWS e da PTAX do Banco Central | `ferramentas/custo-infra/custo_infra.py` |
| Estimativa, cronograma, equipe e custo total do projeto | `bloco-7-planejamento/ferramentas/planejamento.py` |
| Dicionário de dados, lido do catálogo do PostgreSQL | `bloco-5-banco/ferramentas/gerar_dicionario.py` |
| Diagramas, com título, autores e data | `ferramentas/diagramas/gerar.py` |
| Protótipos de interface | `bloco-2-requisitos/prototipos/src/gerar_prototipos.py` |
| AID em PDF, com auditoria de custos, textos proibidos e paginação | `ferramentas/aid/build.py` |
| Slides | `apresentacao/gerador/gerar-slides.js` |

Para gerar tudo de novo, na ordem certa (precisa de Python 3, Node, Google Chrome e, para o banco, Docker):

```
python -I ferramentas/gerar-tudo.py
```

## Estrutura

```
00-a-disciplina-no-projeto.md   mapa das aulas no projeto
bloco-1-concepcao/ … bloco-9-qualidade/   um arquivo por item do enunciado
codigo/                  esqueleto que roda: API NestJS, worker, docker-compose, CI/CD
apresentacao/            slides, gerador e preparação para a arguição
entrega/                 o AID em PDF
ferramentas/             scripts de custo, diagramas, AID e identidade visual
material/                enunciado do professor
fontes.md                todas as fontes
projeto.json             equipe e data, usados por todos os geradores
```
