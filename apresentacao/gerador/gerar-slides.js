// Gera apresentacao/Rufus-Bank-Apresentacao.pptx a partir do repositório.
//
// Ordem e donos seguem o slide 17 do enunciado: PO, Arquiteto, DBA, todos.
// Números (custo, sprints, equipe, riscos, testes) são LIDOS dos arquivos gerados
// pelos scripts do projeto, nunca digitados aqui. Falta um dado = o script para.
//
// Uso: node apresentacao/gerador/gerar-slides.js

const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const RAIZ = path.resolve(__dirname, "..", "..");
const SAIDA = path.join(RAIZ, "apresentacao", "Rufus-Bank-Apresentacao.pptx");
const APLICAR_TEMA = path.join(__dirname, "aplicar-tema.js"); // escreve as cores do tema no .pptx

const ler = (rel) => fs.readFileSync(path.join(RAIZ, rel), "utf8");
const projeto = JSON.parse(ler("projeto.json"));
const id = JSON.parse(ler("ferramentas/identidade/identidade.json")).cores;

function achar(texto, regex, nome) {
  const m = texto.match(regex);
  if (!m) { console.error(`ABORTADO: não achei ${nome}`); process.exit(1); }
  return m;
}

// ---------------------------------------------------------------- dados
const custo = ler("ferramentas/custo-infra/custo-gerado.md");
const linhaCusto = (r) => achar(custo, new RegExp(`\\| ${r} \\| ([\\d.,]+) \\| ([\\d.,]+) \\|`), r);
const C_PROD = linhaCusto("Produção"), C_HML = linhaCusto("Homologação"), C_EXT = linhaCusto("Serviços fora da AWS");
const C_TOT = achar(custo, /\| \*\*Total\*\* \| \*\*([\d.,]+)\*\* \| \*\*([\d.,]+)\*\* \|/, "total mensal");
const C_UNI = achar(custo, /Custos únicos \(antes do lançamento\): \*\*R\$ ([\d.,]+)\*\*/, "custos únicos")[1];

const est = ler("bloco-7-planejamento/02-estimativas.md");
const SP = achar(est, /\*\*(\d+) story points\*\*/, "SP")[1];
const SPRINTS = achar(est, /\*\*(\d+) sprints de 2 semanas\*\*/, "sprints")[1];
const VEL = achar(est, /\*\*(\d+) SP por sprint\*\*/, "velocidade")[1];
const PERIODO = achar(est, /de (\d\d\/\d\d\/\d{4}) a (\d\d\/\d\d\/\d{4})/, "período");

const eq = ler("bloco-7-planejamento/03-equipe-e-custo.md");
const PESSOAS = achar(eq, /\*\*(\d+) pessoas\*\*/, "pessoas")[1];
const EQ_MES = achar(eq, /custa \*\*R\$ ([\d.,]+) por mês\*\*/, "custo da equipe")[1];
const PROJ_TOT = achar(eq, /\| \*\*Total\*\* \| \| \*\*([\d.,]+)\*\* \|/, "total do projeto")[1];

const riscos = [...ler("bloco-7-planejamento/04-matriz-de-riscos.md").matchAll(/^\| (R\d\d) \| ([^|]+) \| ([^|]+) \| (\d) \| (\d) \|/gm)]
  .map((m) => ({ id: m[1], nome: m[2].trim(), cat: m[3].trim(), p: +m[4], i: +m[5] }));
if (riscos.length < 8) { console.error("ABORTADO: menos de 8 riscos"); process.exit(1); }

const TESTES_BD = achar(ler("bloco-5-banco/testes/resultado.txt"), /Resultado: (\d+) caso\(s\) como esperado, (\d+) diferente/, "testes do banco");
const TABELAS = achar(ler("bloco-5-banco/testes/resultado.txt"), /Tabelas criadas: (\d+)/, "tabelas")[1];

// ---------------------------------------------------------------- imagens
function tamanhoPng(arq) {
  const b = fs.readFileSync(arq);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}
function imagem(slide, rel, caixa, opc = {}) {
  const arq = path.join(RAIZ, rel);
  if (!fs.existsSync(arq)) { console.error(`ABORTADO: imagem ausente ${rel}`); process.exit(1); }
  const { w, h } = tamanhoPng(arq);
  const s = Math.min(caixa.w / w, caixa.h / h);
  const W = w * s, H = h * s;
  slide.addImage({ path: arq, x: caixa.x + (caixa.w - W) / 2, y: caixa.y + (caixa.h - H) / 2, w: W, h: H,
    altText: opc.alt || rel, objectName: opc.nome || path.basename(rel) });
}

// Várias partes de um mesmo diagrama (ex.: 02a, 02b...): acha pelo prefixo e distribui
// em grade dentro da caixa, escolhendo o número de colunas que deixa as imagens maiores.
function imagens(slide, pasta, prefixo, caixa, alt) {
  const dir = path.join(RAIZ, pasta);
  const casa = (f) => (prefixo.startsWith("~") ? f.includes(prefixo.slice(1)) : f.startsWith(prefixo));
  const arqs = fs.readdirSync(dir).filter((f) => casa(f) && f.endsWith(".png")).sort();
  if (!arqs.length) { console.error(`ABORTADO: nenhuma imagem ${pasta}/${prefixo}*`); process.exit(1); }
  const tams = arqs.map((f) => tamanhoPng(path.join(dir, f)));
  const gap = 0.2;
  let melhor = null;
  for (let cols = 1; cols <= arqs.length; cols++) {
    const lins = Math.ceil(arqs.length / cols);
    const cw = (caixa.w - gap * (cols - 1)) / cols, ch = (caixa.h - gap * (lins - 1)) / lins;
    const area = tams.reduce((a, t) => { const k = Math.min(cw / t.w, ch / t.h); return a + t.w * k * t.h * k; }, 0);
    if (!melhor || area > melhor.area) melhor = { cols, lins, cw, ch, area };
  }
  arqs.forEach((f, i) => {
    const c = i % melhor.cols, l = Math.floor(i / melhor.cols);
    imagem(slide, `${pasta}/${f}`, { x: caixa.x + c * (melhor.cw + gap), y: caixa.y + l * (melhor.ch + gap), w: melhor.cw, h: melhor.ch },
      { alt: `${alt} (${i + 1} de ${arqs.length})` });
  });
}

// ---------------------------------------------------------------- tema e layouts
const THEME = {
  name: "Rufus Bank", headFontFace: "Arial", bodyFontFace: "Arial",
  colors: { dk1: id.grafite, lt1: "FFFFFF", dk2: id.vermelho_escuro, lt2: id.superficie, accent1: id.vermelho, accent2: id.vermelho_escuro,
    accent3: id.sucesso, accent4: id.alerta, accent5: id.grafite, accent6: id.texto_2, hlink: id.vermelho_escuro, folHlink: id.texto_2 },
};
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13,333 x 7,5 pol
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };
pres.title = `${projeto.nome} · Projeto Final de APS`;
pres.author = projeto.equipe.map((m) => m.nome).join(", ");
pres.company = projeto.instituicao;
const C = pres.SchemeColor;
const W = 13.333, H = 7.5, M = 0.6;

pres.defineSlideMaster({
  title: "CONTEUDO", background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "titulo", type: "title", x: M, y: 0.4, w: W - 2 * M - 2.2, h: 0.8, fontSize: 28, bold: true, color: C.text1, valign: "top", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "rotulo", type: "body", x: W - M - 2.2, y: 0.45, w: 2.2, h: 0.35, fontSize: 11, color: C.text2, align: "right", margin: 0 }, text: "" } },
    { text: { text: `${projeto.nome} · Projeto Final de APS`, options: { x: M, y: H - 0.42, w: 6, h: 0.3, fontSize: 9, color: id.texto_2, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.6, y: H - 0.42, w: 0.6, h: 0.3, fontSize: 9, color: id.texto_2, align: "right" },
});
pres.defineSlideMaster({
  title: "ESCURO", background: { color: id.vermelho_escuro },
  objects: [],
  slideNumber: { x: W - M - 0.6, y: H - 0.42, w: 0.6, h: 0.3, fontSize: 9, color: "F3D9DB", align: "right" },
});

// ---------------------------------------------------------------- helpers de composição
function novo(secao, titulo, rotulo, notas) {
  const s = pres.addSlide({ masterName: "CONTEUDO", sectionTitle: secao });
  s.addText(titulo, { placeholder: "titulo" });
  s.addText(rotulo, { placeholder: "rotulo" });
  if (notas) s.addNotes(notas);
  return s;
}
function sol(s, x, y, d, cor = id.vermelho, nome = "sol") {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: cor }, line: { color: cor }, objectName: nome });
}
function cartao(s, x, y, w, h, nome, fundo = id.superficie) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fundo }, line: { color: id.borda, width: 0.75 }, objectName: nome });
}
function texto(s, t, o) { s.addText(t, { isTextBox: true, margin: 0, color: id.texto, fontSize: 14, valign: "top", ...o }); }
function numero(s, x, y, n) {
  sol(s, x, y, 0.42, id.vermelho, `num-${n}`);
  texto(s, String(n), { x, y, w: 0.42, h: 0.42, fontSize: 14, bold: true, align: "center", valign: "middle", color: "FFFFFF" });
}
const membro = (papel) => projeto.equipe.find((m) => m.papel.startsWith(papel)).nome;
const PO = membro("Analista"), ARQ = membro("Arquiteto"), DBA = membro("Engenheiro");

// ================================================================ 1 capa
pres.addSection({ title: "Abertura" });
{
  const s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "Abertura" });
  sol(s, 8.6, 1.3, 4.2, "FFFFFF", "sol-grande");
  sol(s, 9.5, 2.2, 2.4, id.vermelho, "miolo");
  texto(s, "R", { x: 9.5, y: 2.2, w: 2.4, h: 2.4, fontSize: 96, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  texto(s, `${projeto.instituicao} · ${projeto.disciplina}`, { x: M, y: 0.6, w: 8, h: 0.4, fontSize: 12, color: "F3D9DB" });
  texto(s, projeto.nome, { x: M, y: 2.0, w: 7.6, h: 1.2, fontSize: 60, bold: true, color: "FFFFFF" });
  texto(s, `"${projeto.slogan}"`, { x: M, y: 3.25, w: 7.6, h: 0.5, fontSize: 20, italic: true, color: id.vermelho_suave });
  texto(s, "Da Concepção ao Dia 1 do Dev", { x: M, y: 3.9, w: 7.6, h: 0.4, fontSize: 16, color: "FFFFFF" });
  texto(s, projeto.equipe.map((m) => ({ text: `${m.nome} · ${m.papel}`, options: { breakLine: true } })),
    { x: M, y: 5.2, w: 7, h: 1.1, fontSize: 13, color: "FFFFFF", paraSpaceAfter: 4 });
  const d = projeto.data.split("-");
  texto(s, `Prof. ${projeto.professor} · ${d[2]}/${d[1]}/${d[0]}`, { x: M, y: 6.6, w: 6, h: 0.3, fontSize: 11, color: "F3D9DB" });
  s.addNotes(`${PO} abre (20 s): "Somos o Rufus Bank. Um banco digital para quem os bancos atuais atendem mal: quem lê com dificuldade, idosos e adolescentes. Vamos mostrar o projeto inteiro, da concepção até o dev poder começar amanhã."`);
}

// ================================================================ PO
pres.addSection({ title: `PO · ${PO}` });
{
  const s = novo(`PO · ${PO}`, "O acesso já existe. O que falta é conseguir usar", "Bloco 1 · Problema",
    `${PO} (40 s): o problema não é ter conta, é usar a conta sozinho e com segurança. Os quatro números vêm de fontes oficiais, com link no AID.`);
  const stats = [
    ["21,1 mi", "adultos sem usar nenhum produto financeiro em 2024", "Banco Central, Relatório de Cidadania Financeira 2025"],
    ["29%", "da população de 15 a 64 anos é analfabeta funcional (51% entre 50 e 64)", "Inaf 2024"],
    ["87%", "erraram uma conta simples de juros", "Banco Central, pesquisa OCDE/INFE 2023"],
    ["139 mil", "golpes da falsa central no 1º semestre de 2025, alta de 195,7%", "Febraban"],
  ];
  const cw = (W - 2 * M - 3 * 0.3) / 4;
  stats.forEach(([n, t, f], i) => {
    const x = M + i * (cw + 0.3);
    cartao(s, x, 1.6, cw, 4.6, `stat-${i}`);
    sol(s, x + 0.3, 1.9, 0.5, id.vermelho, `stat-sol-${i}`);
    texto(s, n, { x: x + 0.3, y: 2.6, w: cw - 0.6, h: 1.0, fontSize: 44, bold: true, color: id.grafite });
    texto(s, t, { x: x + 0.3, y: 3.7, w: cw - 0.6, h: 1.4, fontSize: 15, color: id.texto });
    texto(s, f, { x: x + 0.3, y: 5.4, w: cw - 0.6, h: 0.6, fontSize: 10, color: id.texto_2 });
  });
}
{
  const s = novo(`PO · ${PO}`, "Três pessoas reais por trás dos requisitos", "Bloco 1 · Personas",
    `${PO} (40 s): cada persona representa um grupo mal atendido. Cada dor virou requisito: Antônio é o áudio e os ícones, Camila é a conta com responsável, Dona Marlene é pagar contas sem o neto.`);
  const p = [
    ["Antônio, 47", "Ajudante de pedreiro. Estudou até o 5º ano e lê com dificuldade. Já caiu no golpe do falso atendente.", "Usar a conta por ícones e áudio, sem depender de ninguém"],
    ["Camila, 17", "Estudante e jovem aprendiz. Quer juntar para um notebook. Os bancos bloqueiam ou tratam como adulta.", "Autonomia com limites seguros, vinculada ao responsável"],
    ["Dona Marlene, 68", "Aposentada. Usa o celular só para WhatsApp e depende do neto para o app do banco.", "Pagar as próprias contas sem pedir ajuda"],
  ];
  const cw = (W - 2 * M - 2 * 0.35) / 3;
  p.forEach(([n, ctx, mot], i) => {
    const x = M + i * (cw + 0.35);
    cartao(s, x, 1.6, cw, 4.8, `persona-${i}`);
    sol(s, x + 0.35, 1.95, 0.9, id.vermelho, `persona-sol-${i}`);
    texto(s, n.replace("Dona ", "")[0], { x: x + 0.35, y: 1.95, w: 0.9, h: 0.9, fontSize: 30, bold: true, align: "center", valign: "middle", color: "FFFFFF" });
    texto(s, n, { x: x + 1.45, y: 2.1, w: cw - 1.7, h: 0.6, fontSize: 22, bold: true, color: id.grafite });
    texto(s, ctx, { x: x + 0.35, y: 3.15, w: cw - 0.7, h: 1.6, fontSize: 14, color: id.texto });
    texto(s, "Motivação", { x: x + 0.35, y: 4.85, w: cw - 0.7, h: 0.3, fontSize: 11, bold: true, color: id.texto_2 });
    texto(s, mot, { x: x + 0.35, y: 5.15, w: cw - 0.7, h: 1.0, fontSize: 15, bold: true, color: id.grafite });
  });
}
{
  const s = novo(`PO · ${PO}`, "Simples por padrão, protegido por padrão", "Bloco 1 · Proposta de valor",
    `${PO} (40 s): os cinco princípios valem para todas as telas e viraram RNF com número. À direita, o que ficou de fora de propósito: o "fora do escopo" é tão importante quanto o escopo.`);
  const pr = [["Ícone e áudio em toda tela", "Tudo que está escrito pode ser ouvido"],
    ["Poucos passos", "Até 3 toques de navegação nas ações principais"],
    ["Linguagem do dia a dia", "\"Dinheiro que você tem\", não \"saldo disponível\""],
    ["Proteção contra golpe", "O Rufus nunca liga. O app fala para quem vai o Pix"],
    ["Autonomia com rede de apoio", "Contato de confiança e responsável do menor"]];
  pr.forEach(([t, d], i) => {
    const y = 1.6 + i * 0.95;
    numero(s, M, y, i + 1);
    texto(s, t, { x: M + 0.6, y: y - 0.02, w: 6.6, h: 0.4, fontSize: 17, bold: true, color: id.grafite });
    texto(s, d, { x: M + 0.6, y: y + 0.38, w: 6.6, h: 0.4, fontSize: 13, color: id.texto_2 });
  });
  cartao(s, 8.1, 1.5, W - M - 8.1, 4.9, "fora-do-escopo");
  texto(s, "Fora do escopo", { x: 8.4, y: 1.75, w: 4, h: 0.4, fontSize: 17, bold: true, color: id.grafite });
  texto(s, ["Atendimento presencial", "Crédito e cartão de crédito", "Investimentos", "Conta PJ ou MEI", "Cartão físico e saque", "Câmbio e criptoativos", "Core bancário próprio"]
    .map((t, i, a) => ({ text: t, options: { bullet: true, breakLine: i < a.length - 1 } })),
    { x: 8.4, y: 2.3, w: 4.0, h: 3.9, fontSize: 14, color: id.texto, paraSpaceAfter: 6 });
}
{
  const s = novo(`PO · ${PO}`, "32 RF com MoSCoW e 14 RNF com número", "Bloco 2 · Requisitos",
    `${PO} (45 s): MoSCoW com justificativa em cada RF. Todo RNF tem métrica e forma de medir, e está classificado como de produto, organizacional ou externo (Sommerville, Aula 04). Os números da direita obrigam a infraestrutura e o banco.`);
  s.addChart(pres.charts.BAR, [{ name: "RF", labels: ["Must", "Should", "Could", "Won't"], values: [22, 6, 2, 2] }], {
    x: M, y: 1.5, w: 5.4, h: 4.6, barDir: "bar", showTitle: true, title: "RF por prioridade MoSCoW", titleFontSize: 13, titleColor: id.grafite,
    titleFontFace: "+mn-lt", chartColors: [id.vermelho], showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 12,
    dataLabelColor: id.grafite, dataLabelFontFace: "+mn-lt", catAxisLabelColor: id.texto, catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt",
    valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false, catAxisOrientation: "maxMin",
  });
  const chips = [["300 ms", "p95 das leituras"], ["99,9%", "disponibilidade ao mês"], ["10.000", "usuários ativos e 100 req/s"],
    ["3 toques", "nas ações principais"], ["4,5:1", "contraste WCAG AA"], ["5 min", "perda máxima de dados"]];
  chips.forEach(([n, t], i) => {
    const col = i % 2, lin = Math.floor(i / 2);
    const x = 6.6 + col * 3.15, y = 1.55 + lin * 1.55;
    cartao(s, x, y, 2.95, 1.35, `rnf-${i}`);
    texto(s, n, { x: x + 0.25, y: y + 0.15, w: 2.6, h: 0.6, fontSize: 26, bold: true, color: id.grafite });
    texto(s, t, { x: x + 0.25, y: y + 0.78, w: 2.6, h: 0.45, fontSize: 12, color: id.texto_2 });
  });
  texto(s, "Mais 16 regras de negócio e o processo de engenharia de requisitos em 6 passos (Aula 04).",
    { x: 6.6, y: 6.25, w: 6.1, h: 0.4, fontSize: 12, color: id.texto_2 });
}
{
  const s = novo(`PO · ${PO}`, "Do épico à tarefa: 24 histórias, 114 pontos", "Bloco 2 · Histórias",
    `${PO} (40 s): backlog na hierarquia da Aula 04. Cada história tem Given/When/Then e story points na escala de Fibonacci, com a US13 de 3 pontos como referência. Exemplo à direita.`);
  const ep = [["E1 Conta e acesso", 4, 23], ["E2 Dinheiro do dia a dia", 6, 32], ["E3 Proteção contra golpe", 4, 17], ["E4 Família", 3, 16],
    ["E5 Metas e educação", 3, 10], ["E6 Atendimento e avisos", 3, 13], ["E7 Backoffice", 1, 3]];
  const linhas = [[{ text: "Épico", options: { bold: true } }, { text: "Histórias", options: { bold: true, align: "center" } }, { text: "SP", options: { bold: true, align: "center" } }],
    ...ep.map(([e, h, p]) => [e, { text: String(h), options: { align: "center" } }, { text: String(p), options: { align: "center" } }])];
  s.addTable(linhas, { x: M, y: 1.55, w: 5.6, colW: [3.6, 1.0, 1.0], fontSize: 13, color: id.texto, border: { type: "solid", color: id.borda, pt: 0.75 },
    fill: { color: "FFFFFF" }, rowH: 0.5, fontFace: "Arial", objectName: "tabela-epicos" });
  cartao(s, 6.7, 1.55, W - M - 6.7, 4.85, "exemplo-us");
  texto(s, "US06 · Enviar Pix ouvindo para quem vai · 8 SP", { x: 7.0, y: 1.8, w: 5.5, h: 0.4, fontSize: 15, bold: true, color: id.grafite });
  texto(s, "Como Dona Marlene, quero ouvir o nome de quem vai receber e o valor antes de confirmar, para ter certeza de que não estou errando.",
    { x: 7.0, y: 2.3, w: 5.5, h: 0.9, fontSize: 13, italic: true, color: id.texto });
  texto(s, [
    { text: "Dado ", options: { bold: true } }, { text: "que informei a chave e o valor,", options: { breakLine: true } },
    { text: "Quando ", options: { bold: true } }, { text: "chego na tela de confirmação,", options: { breakLine: true } },
    { text: "Então ", options: { bold: true } }, { text: "o app mostra e fala o nome do recebedor, o banco e o valor." },
  ], { x: 7.0, y: 3.4, w: 5.5, h: 1.5, fontSize: 14, color: id.texto, paraSpaceAfter: 6 });
  texto(s, "Mais 2 critérios: Pix confirmado em até 10 s (RNF02) e saldo insuficiente avisado antes da digital.",
    { x: 7.0, y: 5.25, w: 5.5, h: 0.8, fontSize: 12, color: id.texto_2 });
}
{
  const s = novo(`PO · ${PO}`, "A interface é o produto", "Bloco 2 · Design de interface",
    `${PO} (40 s): Aula 05 aplicada. Taxonomia do app, os três níveis de protótipo (conceito, baixa e alta fidelidade) e o plano de Teste de Resposta Emocional. Contraste medido pela fórmula da WCAG e áreas de toque de 48 dp.`);
  imagem(s, "bloco-2-requisitos/prototipos/img/prancha-alta.png", { x: M, y: 1.35, w: W - 2 * M, h: 5.65 }, { alt: "Prancha com as 8 telas do protótipo de alta fidelidade" });
}

// ================================================================ ARQUITETO
pres.addSection({ title: `Arquiteto · ${ARQ}` });
{
  const s = novo(`Arquiteto · ${ARQ}`, "13 decisões contra a alternativa descartada", "Bloco 3 · ADR",
    `${ARQ} (50 s): nenhuma decisão é "porque conhecemos". Cada motivo sai de um requisito. Os 13 ADRs completos estão no AID.`);
  const adr = [["Monolito modular", "Microsserviços", "100 req/s e 2 devs de back-end não pagam vários serviços e bancos"],
    ["REST + OpenAPI 3.0", "gRPC", "Ganho não é necessário para 300 ms. Navegador e webhooks falam HTTP"],
    ["React Native", "Flutter", "Componentes nativos lidos pelo leitor de tela sem anotação extra"],
    ["NestJS (TypeScript)", "Spring Boot", "Cabe em 1 GB por tarefa e é a mesma linguagem do app"],
    ["PostgreSQL 17", "MongoDB", "Dinheiro exige transação ACID, FK e restrição"],
    ["ECS Fargate", "EKS ou Lambda", "EKS custa US$ 73 por cluster. Lambda tem partida a frio"],
    ["Outbox no PostgreSQL", "SQS ou Kafka", "Dado e evento gravados na mesma transação"],
    ["AWS São Paulo", "Região dos EUA", "Dados no Brasil (LGPD, art. 33) e menor latência"]];
  const cab = ["Decisão", "Descartada", "Por quê"].map((t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: id.grafite } } }));
  s.addTable([cab, ...adr.map((r) => [{ text: r[0], options: { bold: true } }, r[1], r[2]])], {
    x: M, y: 1.45, w: W - 2 * M, colW: [3.0, 2.4, W - 2 * M - 5.4], fontSize: 13, color: id.texto, rowH: 0.55,
    border: { type: "solid", color: id.borda, pt: 0.75 }, fontFace: "Arial", objectName: "tabela-adr" });
}
{
  const s = novo(`Arquiteto · ${ARQ}`, "C4: do contexto ao código", "Bloco 3 · Modelo C4",
    `${ARQ} (45 s): os 4 níveis. No centro, o nível 2 (containers), com tecnologia e protocolo em cada seta. À direita, contexto, componentes e o código do componente crítico, o ServicoEnvioPix.`);
  imagem(s, "bloco-3-arquitetura/diagramas/img/c4-2-containers.png", { x: M, y: 1.35, w: 8.4, h: 5.7 }, { alt: "C4 nível 2, containers" });
  [["c4-1", "1 · Contexto"], ["c4-3", "3 · Componentes"], ["c4-4", "4 · Código"]].forEach(([f, t], i) => {
    const y = 1.35 + i * 1.92;
    cartao(s, 9.25, y, W - M - 9.25, 1.8, `c4-mini-${i}`, "FFFFFF");
    imagens(s, "bloco-3-arquitetura/diagramas/img", f, { x: 9.35, y: y + 0.08, w: 2.1, h: 1.64 }, t);
    texto(s, t, { x: 11.55, y: y + 0.65, w: 1.2, h: 0.5, fontSize: 12, bold: true, color: id.grafite });
  });
}
{
  const s = novo(`Arquiteto · ${ARQ}`, "Casos de uso: 7 atores e 3 sistemas externos", "Bloco 4 · UML",
    `${ARQ} (40 s): todos os atores do Documento de Visão. Mostrar o «include»: Enviar Pix sempre inclui Confirmar recebedor por voz e Avaliar risco. O «extend»: Pedir aprovação ao responsável estende Enviar Pix quando o menor passa do limite. E a generalização: titular e menor são especializações do Cliente.`);
  imagens(s, "bloco-4-uml/diagramas/img", "01", { x: M, y: 1.35, w: W - 2 * M, h: 5.7 }, "Diagrama de casos de uso");
}
{
  const s = novo(`Arquiteto · ${ARQ}`, "Classes tipadas, com visibilidade e relações", "Bloco 4 · UML",
    `${ARQ} (45 s): herança só em Transacao, porque um Pix é uma transação e compartilha o ciclo de vida. Composição onde a parte não vive sem o todo (Chamado e MensagemChamado, Conta e Carteira). Agregação em Conta e ChavePix.`);
  imagens(s, "bloco-4-uml/diagramas/img", "02", { x: M, y: 1.3, w: W - 2 * M, h: 5.8 }, "Diagrama de classes");
}
{
  const s = novo(`Arquiteto · ${ARQ}`, "O erro crítico: o parceiro cai no meio do Pix", "Bloco 4 · Sequência",
    `${ARQ} (45 s): é a sequência mais importante. O cliente não perde dinheiro: a saga compensa a reserva com estorno, e a chave de idempotência impede o Pix em dobro. As sequências de autenticação e do caminho feliz estão no AID.`);
  imagens(s, "bloco-4-uml/diagramas/img", "05", { x: M, y: 1.3, w: W - 2 * M, h: 5.8 }, "Sequência do erro crítico");
}
{
  const s = novo(`Arquiteto · ${ARQ}`, "Componentes e implantação", "Bloco 4 · UML",
    `${ARQ} (40 s): à esquerda, os módulos e as portas para o mundo externo (ADR-002). À direita, dev, homologação e produção, com protocolos e portas: 443, 3000 e 5432.`);
  imagens(s, "bloco-4-uml/diagramas/img", "06", { x: M, y: 1.35, w: 5.9, h: 5.7 }, "Diagrama de componentes");
  imagens(s, "bloco-4-uml/diagramas/img", "07", { x: 6.8, y: 1.35, w: W - M - 6.8, h: 5.7 }, "Diagrama de implantação");
}
{
  const s = novo(`Arquiteto · ${ARQ}`, "Processo de negócio em BPMN 2.0", "Bloco 4 · Processos",
    `${ARQ} (35 s): BPM é a gestão, BPMN é a notação (Aula 02). O envio de Pix em BPMN 2.0, em duas partes: pedido e risco, depois liquidação e estorno. Pools, raias e fluxo de mensagem. A conta de menor também está em BPMN no AID. As duas atividades UML (abertura de conta e análise antifraude) estão no AID.`);
  imagens(s, "bloco-4-uml/diagramas/img", "~bpmn-pix", { x: M, y: 1.35, w: W - 2 * M, h: 5.7 }, "BPMN do envio de Pix");
}

// ================================================================ DBA
pres.addSection({ title: `DBA · ${DBA}` });
{
  const s = novo(`DBA · ${DBA}`, "PostgreSQL porque é dinheiro", "Bloco 5 · Banco de dados",
    `${DBA} (40 s): a escolha vem da arquitetura e dos requisitos: ACID, FK e restrição para o razão contábil. Normalizado até a 3FN, com desnormalização só onde medimos ganho, o saldo de fechamento diário.`);
  imagens(s, "bloco-5-banco/diagramas/img", "conceitual", { x: 5.3, y: 1.35, w: W - M - 5.3, h: 5.7 }, "Modelo conceitual");
  const lin = [["Critério", "PostgreSQL", "MongoDB"], ["Transação entre várias linhas", "ACID nativo", "Restrita"], ["Chave estrangeira e restrição", "No banco", "Na aplicação"],
    ["Razão de partidas dobradas", "Gatilho adiado", "Código da aplicação"], ["Gerenciado com failover", "RDS Multi-AZ", "Outro serviço"]];
  s.addTable(lin.map((r, i) => r.map((c) => (i === 0 ? { text: c, options: { bold: true, color: "FFFFFF", fill: { color: id.grafite } } } : c))), {
    x: M, y: 1.45, w: 4.4, colW: [1.8, 1.3, 1.3], fontSize: 11, color: id.texto, rowH: 0.5, border: { type: "solid", color: id.borda, pt: 0.75 }, fontFace: "Arial" });
  texto(s, `${TABELAS} tabelas no modelo físico`, { x: M, y: 4.6, w: 4.4, h: 0.4, fontSize: 16, bold: true, color: id.grafite });
  texto(s, "Conceitual, lógico com índices justificados, DDL executável e dicionário de dados gerado do próprio banco.", { x: M, y: 5.05, w: 4.4, h: 1.0, fontSize: 13, color: id.texto_2 });
}
{
  const s = novo(`DBA · ${DBA}`, "O DDL roda de verdade, e as regras moram no banco", "Bloco 5 · Modelo físico",
    `${DBA} (45 s): aplicamos o SQL num PostgreSQL 17 real e rodamos casos que precisam ser recusados. Um lançamento desequilibrado, um segundo celular ativo e uma chave de idempotência repetida são barrados pelo banco, não só pelo código.`);
  cartao(s, M, 1.5, 4.2, 4.9, "testes-banco", id.grafite);
  texto(s, `${TESTES_BD[1]}/${+TESTES_BD[1] + +TESTES_BD[2]}`, { x: M + 0.4, y: 1.9, w: 3.5, h: 1.2, fontSize: 60, bold: true, color: "FF8F87" });
  texto(s, "casos de teste com o resultado esperado no PostgreSQL 17", { x: M + 0.4, y: 3.15, w: 3.5, h: 0.8, fontSize: 15, color: "FFFFFF" });
  texto(s, ["Lançamento desequilibrado: recusado", "2 celulares ativos: recusado", "Pix em dobro: recusado", "Pix com nota 85 liberado sozinho: recusado"]
    .map((t, i, a) => ({ text: t, options: { bullet: true, breakLine: i < a.length - 1 } })), { x: M + 0.4, y: 4.1, w: 3.6, h: 2.1, fontSize: 12, color: "FFFFFF", paraSpaceAfter: 4 });
  const sql = ler("bloco-5-banco/sql/001_schema.sql");
  const ini = sql.indexOf("CREATE FUNCTION conferir_partidas_dobradas");
  const fim = sql.indexOf("conferir_partidas_dobradas();", ini) + "conferir_partidas_dobradas();".length;
  if (ini < 0 || fim < ini) { console.error("ABORTADO: gatilho de partidas dobradas não encontrado no SQL"); process.exit(1); }
  const trecho = sql.slice(ini, fim);
  cartao(s, 5.1, 1.5, W - M - 5.1, 4.9, "trecho-sql", "F9FAFB");
  texto(s, "Gatilho que recusa transação desequilibrada (ADR-007)", { x: 5.35, y: 1.7, w: W - M - 5.6, h: 0.35, fontSize: 13, bold: true, color: id.vermelho });
  texto(s, trecho, { x: 5.35, y: 2.15, w: W - M - 5.6, h: 4.1, fontFace: "Courier New", fontSize: 11, color: id.texto });
}
{
  const s = novo(`DBA · ${DBA}`, "Infraestrutura em 2 zonas e custo com fonte", "Bloco 6 · Infra",
    `${DBA} (50 s): 99,9% vem de duas zonas, banco Multi-AZ e dois NAT. Todo preço foi lido da tabela oficial da AWS para São Paulo por um script, com o dólar da PTAX do Banco Central. Os links estão no AID.`);
  imagem(s, "bloco-6-infra/diagramas/img/infra-producao.png", { x: M, y: 1.35, w: 6.6, h: 5.7 }, { alt: "Diagrama de infraestrutura de produção" });
  const lin = [["Ambiente", "R$ por mês"], ["Produção (AWS)", C_PROD[2]], ["Homologação (AWS)", C_HML[2]], ["Serviços fora da AWS", C_EXT[2]], ["Desenvolvimento", "0,00"]];
  s.addTable([...lin.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: i === 0, align: j === 1 ? "right" : "left", ...(i === 0 ? { color: "FFFFFF", fill: { color: id.grafite } } : {}) } }))),
    [{ text: "Total mensal", options: { bold: true } }, { text: C_TOT[2], options: { bold: true, align: "right" } }]], {
    x: 7.5, y: 1.5, w: W - M - 7.5, colW: [3.2, W - M - 7.5 - 3.2], fontSize: 13, color: id.texto, rowH: 0.5, border: { type: "solid", color: id.borda, pt: 0.75 }, fontFace: "Arial" });
  texto(s, `Mais R$ ${C_UNI} de custos únicos: conta do Google Play e teste de invasão.`, { x: 7.5, y: 4.75, w: W - M - 7.5, h: 0.6, fontSize: 13, color: id.texto_2 });
  texto(s, "Fonte: AWS Price List API (sa-east-1), CSV oficial de SMS da AWS, páginas de preço do Expo, GitHub e Registro.br, PTAX do Banco Central de 04/11/2026.",
    { x: 7.5, y: 5.45, w: W - M - 7.5, h: 0.9, fontSize: 10, color: id.texto_2 });
}
{
  const s = novo(`DBA · ${DBA}`, "Nada chega à produção sem passar por 8 portões", "Bloco 6 · CI/CD",
    `${DBA} (40 s): cada etapa tem critério de bloqueio. Lint, testes com cobertura de 80%, build, segurança com npm audit, Trivy e gitleaks, homologação, smoke test, aprovação humana e produção com volta automática.`);
  const et = [["Lint e tipos", "Erro de lint ou contrato inválido"], ["Testes", "Teste falho ou cobertura < 80%"], ["Build", "Imagem não compila"],
    ["Segurança", "Vulnerabilidade alta ou segredo"], ["Publicar", "Etapas 1 a 4 não verdes"], ["Homologação", "/health falha: volta sozinho"],
    ["Smoke test", "p95 > 300 ms ou > 1% de erro"], ["Aprovar e publicar", "Sem revisor, nada sai"]];
  const cw = (W - 2 * M - 3 * 0.25) / 4;
  et.forEach(([t, b], i) => {
    const col = i % 4, lin = Math.floor(i / 4);
    const x = M + col * (cw + 0.25), y = 1.6 + lin * 2.5;
    cartao(s, x, y, cw, 2.2, `etapa-${i}`);
    numero(s, x + 0.25, y + 0.25, i + 1);
    texto(s, t, { x: x + 0.25, y: y + 0.8, w: cw - 0.5, h: 0.4, fontSize: 16, bold: true, color: id.grafite });
    texto(s, `Bloqueia: ${b}`, { x: x + 0.25, y: y + 1.3, w: cw - 0.5, h: 0.75, fontSize: 12, color: id.texto_2 });
  });
}
{
  const s = novo(`DBA · ${DBA}`, "OWASP Top 10 endereçado item por item", "Bloco 6 · Segurança",
    `${DBA} (40 s): autenticação própria com JWT de 15 minutos e celular vinculado, papéis para funcionários (RBAC) e regra de vínculo para o responsável (ABAC). Segredos no Secrets Manager. Cada item da OWASP tem uma medida no Bloco 6.`);
  const ow = [["A01", "Controle de acesso", "RBAC + ABAC do vínculo"], ["A02", "Falhas de criptografia", "TLS 1.2+, CPF cifrado"], ["A03", "Injeção", "SQL parametrizado, DTO validado"],
    ["A04", "Design inseguro", "Limites e retenção antifraude"], ["A05", "Configuração", "Banco em subnet privada, /docs fora da produção"], ["A06", "Componentes", "npm audit e Trivy no pipeline"],
    ["A07", "Autenticação", "Argon2id, bloqueio após 5 erros"], ["A08", "Integridade", "Webhook com HMAC, imagem por hash"], ["A09", "Log e monitoramento", "Log estruturado, alertas"],
    ["A10", "SSRF", "Saída só para hosts do parceiro"]];
  const cw = (W - 2 * M - 4 * 0.2) / 5;
  ow.forEach(([c, t, m], i) => {
    const col = i % 5, lin = Math.floor(i / 5);
    const x = M + col * (cw + 0.2), y = 1.55 + lin * 2.5;
    cartao(s, x, y, cw, 2.3, `owasp-${i}`);
    texto(s, c, { x: x + 0.2, y: y + 0.2, w: cw - 0.4, h: 0.4, fontSize: 18, bold: true, color: id.vermelho });
    texto(s, t, { x: x + 0.2, y: y + 0.65, w: cw - 0.4, h: 0.6, fontSize: 14, bold: true, color: id.grafite });
    texto(s, m, { x: x + 0.2, y: y + 1.3, w: cw - 0.4, h: 0.9, fontSize: 12, color: id.texto_2 });
  });
}

// ================================================================ TODOS
pres.addSection({ title: "Todos" });
{
  const s = novo("Todos", `${SP} pontos em ${SPRINTS} sprints com ${PESSOAS} pessoas`, "Bloco 7 · Planejamento",
    `Quem o grupo escolher (45 s): a estimativa cabe na equipe. Velocidade de ${VEL} SP por sprint, com rampa no começo e o último sprint como reserva para o beta. Salários da Robert Half (mediana de Recife) e encargos CLT calculados item por item.`);
  imagem(s, "bloco-7-planejamento/diagramas/img/cronograma.png", { x: M, y: 1.4, w: W - 2 * M, h: 2.9 }, { alt: "Cronograma em sprints" });
  const st = [[SP, "story points no MVP"], [`${VEL}`, "SP por sprint"], [`R$ ${EQ_MES}`, "equipe por mês, com encargos"], [`R$ ${PROJ_TOT}`, `projeto de ${PERIODO[1]} a ${PERIODO[2]}`]];
  const cw = (W - 2 * M - 3 * 0.3) / 4;
  st.forEach(([n, t], i) => {
    const x = M + i * (cw + 0.3);
    cartao(s, x, 4.55, cw, 1.9, `plan-${i}`);
    texto(s, n, { x: x + 0.25, y: 4.8, w: cw - 0.5, h: 0.7, fontSize: n.length > 10 ? 22 : 30, bold: true, color: id.grafite });
    texto(s, t, { x: x + 0.25, y: 5.55, w: cw - 0.5, h: 0.7, fontSize: 12, color: id.texto_2 });
  });
}
{
  const s = novo("Todos", `${riscos.length} riscos, todos com dono e plano`, "Bloco 7 · Riscos",
    `Quem o grupo escolher (35 s): golpe e baixa adesão são os mais graves, porque atacam o motivo de o Rufus existir. Cada risco tem mitigação, dono e o sinal que dispara a ação.`);
  const ox = 2.3, oy = 1.45, cel = 1.6;
  const cor = (p, i) => (p * i >= 6 ? "FBE3E0" : p * i >= 3 ? "FFF4D6" : "E6F4EE");
  for (let p = 3; p >= 1; p--) for (let i = 1; i <= 3; i++) {
    const x = ox + (i - 1) * (cel * 1.35), y = oy + (3 - p) * cel;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: cel * 1.35 - 0.08, h: cel - 0.08, rectRadius: 0.08, fill: { color: cor(p, i) }, line: { color: id.borda, width: 0.75 }, objectName: `celula-${p}-${i}` });
    const ids = riscos.filter((r) => r.p === p && r.i === i).map((r) => r.id).join("  ");
    texto(s, ids, { x: x + 0.12, y: y + 0.12, w: cel * 1.35 - 0.3, h: cel - 0.3, fontSize: 14, bold: true, color: id.grafite, valign: "middle", align: "center" });
  }
  texto(s, "Probabilidade", { x: M, y: oy + 1.2, w: 1.5, h: 0.4, fontSize: 12, bold: true, color: id.texto_2 });
  ["Alta", "Média", "Baixa"].forEach((t, k) => texto(s, t, { x: M + 0.2, y: oy + k * cel + 0.6, w: 1.3, h: 0.3, fontSize: 12, color: id.texto_2, align: "right" }));
  ["Baixo", "Médio", "Alto"].forEach((t, k) => texto(s, t, { x: ox + k * cel * 1.35, y: oy + 3 * cel + 0.05, w: cel * 1.35, h: 0.3, fontSize: 12, color: id.texto_2, align: "center" }));
  texto(s, "Impacto", { x: ox, y: oy + 3 * cel + 0.35, w: cel * 4, h: 0.3, fontSize: 12, bold: true, color: id.texto_2, align: "center" });
  const top = riscos.filter((r) => r.p * r.i >= 6);
  texto(s, top.map((r, k) => ({ text: `${r.id} ${r.nome}`, options: { breakLine: k < top.length - 1 } })),
    { x: 9.3, y: 1.5, w: W - M - 9.3, h: 4.9, fontSize: 12, color: id.texto, paraSpaceAfter: 6 });
}
{
  const s = novo("Todos", "O dev pode começar amanhã?", "Blocos 8 e 9",
    `Todos (50 s): sim. O README leva do clone ao localhost. Rodamos de verdade: banco com o DDL, API respondendo em /health e o contrato OpenAPI com as 50 rotas em /docs. O Sprint 1 está detalhado, e DoR e DoD dizem quando uma história entra e quando sai.`);
  cartao(s, M, 1.5, 7.2, 4.95, "terminal", id.grafite);
  texto(s, [
    { text: "$ git clone ... && cd codigo", options: { breakLine: true, color: "FFFFFF" } },
    { text: "$ cp .env.example .env", options: { breakLine: true, color: "FFFFFF" } },
    { text: "$ docker compose up --build", options: { breakLine: true, color: "FFFFFF" } },
    { text: " ", options: { breakLine: true } },
    { text: "$ curl localhost:3000/health", options: { breakLine: true, color: "FFFFFF" } },
    { text: "HTTP/1.1 200 OK", options: { breakLine: true, color: "FF8F87" } },
    { text: '{"status":"ok","banco":"ok"}', options: { breakLine: true, color: "FF8F87" } },
    { text: " ", options: { breakLine: true } },
    { text: "localhost:3000/docs  ->  50 rotas (OpenAPI 3.0)", options: { color: "FF8F87" } },
  ], { x: M + 0.4, y: 1.8, w: 6.5, h: 4.4, fontFace: "Courier New", fontSize: 14 });
  const it = [["README", "Do clone ao localhost, testado"], [".env.example", "Todas as variáveis comentadas"], ["OpenAPI 3.0", "50 rotas, validado sem erro"],
    ["Sprint 1", "Itens, donos e critérios de aceite"], ["DoR e DoD", "Quando entra e quando está pronto"], ["Testes", "Pirâmide, cobertura e carga"]];
  it.forEach(([t, d], i) => {
    const y = 1.55 + i * 0.82;
    sol(s, 8.25, y + 0.08, 0.32, id.sucesso, `ok-${i}`);
    texto(s, t, { x: 8.75, y, w: 4, h: 0.35, fontSize: 15, bold: true, color: id.grafite });
    texto(s, d, { x: 8.75, y: y + 0.36, w: 4, h: 0.35, fontSize: 12, color: id.texto_2 });
  });
}
{
  const s = novo("Todos", "A disciplina inteira, aplicada", "Conclusão",
    `Todos (30 s): o projeto é a conclusão da matéria. Cada aula aparece num bloco, e o AID abre com esse mapa completo.`);
  const au = [["01", "Introdução", "Custos de referência e etapas da engenharia de software no plano"],
    ["02", "Processos", "BPMN 2.0 do Pix e lição do Ariane 5 na estratégia de testes"],
    ["03", "Ciclos de vida", "Incremental escolhido contra Cascata, V, Evolutivo e Espiral"],
    ["04", "Requisitos", "ER em 6 passos, RNF classificados, regras de negócio, épicos"],
    ["05", "Interface", "Taxonomia, 3 níveis de protótipo, TER e SWOT"]];
  au.forEach(([n, t, d], i) => {
    const y = 1.55 + i * 1.0;
    cartao(s, M, y, W - 2 * M, 0.85, `aula-${i}`);
    sol(s, M + 0.2, y + 0.14, 0.58, id.vermelho, `aula-sol-${i}`);
    texto(s, n, { x: M + 0.2, y: y + 0.14, w: 0.58, h: 0.58, fontSize: 15, bold: true, align: "center", valign: "middle", color: "FFFFFF" });
    texto(s, `Aula ${n} · ${t}`, { x: M + 1.0, y: y + 0.24, w: 3.2, h: 0.4, fontSize: 16, bold: true, color: id.grafite });
    texto(s, d, { x: M + 4.3, y: y + 0.26, w: W - 2 * M - 4.6, h: 0.4, fontSize: 14, color: id.texto });
  });
}
{
  const s = pres.addSlide({ masterName: "ESCURO", sectionTitle: "Todos" });
  sol(s, 4.67, 0.9, 4.0, "FFFFFF", "sol-final");
  sol(s, 5.42, 1.65, 2.5, id.vermelho, "miolo-final");
  texto(s, "R", { x: 5.42, y: 1.65, w: 2.5, h: 2.5, fontSize: 90, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
  texto(s, "Obrigado. Perguntas?", { x: M, y: 5.25, w: W - 2 * M, h: 0.8, fontSize: 36, bold: true, color: "FFFFFF", align: "center" });
  texto(s, projeto.equipe.map((m) => m.nome).join("  ·  "), { x: M, y: 6.1, w: W - 2 * M, h: 0.4, fontSize: 14, color: id.vermelho_suave, align: "center" });
  s.addNotes("Arguição: qualquer integrante responde qualquer parte. Respostas ensaiadas em apresentacao/arguicao.md.");
}

(async () => {
  await pres.writeFile({ fileName: SAIDA });
  const { applyTheme } = require(APLICAR_TEMA);
  await applyTheme(SAIDA, THEME);
  console.log(`ok  ${path.relative(RAIZ, SAIDA)}`);
})();
