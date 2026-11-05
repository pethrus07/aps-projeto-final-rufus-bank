# 8.6 Sprint 1 detalhado

| | |
| --- | --- |
| Período | 30/11/2026 (segunda) a 11/12/2026 (sexta), 10 dias úteis |
| Meta do sprint | **Antônio entra com a digital num app que fala** |
| Capacidade | 27,2 SP (velocidade de 34 SP x 80% de rampa, ver [Bloco 7](../bloco-7-planejamento/02-estimativas.md)) |
| Planejado | 26 SP em 4 itens |
| Pré-requisito | Sprint 0 concluído: repositório e padrões (T01), esqueleto da API com `/health` (T06), pipeline de CI (T04), porta bancária com adaptador falso (T09) |

## Itens do sprint

| Item | Descrição | SP | Responsável principal | Apoio |
| --- | --- | --- | --- | --- |
| T12 | Esqueleto do app Expo: navegação, tema acessível, botão "Ouvir", cliente gerado do OpenAPI | 8 | Dev Mobile 1 | UX (tema, tamanhos e contraste) |
| T07 | Migrações e razão contábil: carteiras, lançamentos e gatilho de soma zero | 8 | Tech Lead | DevOps (banco do Docker Compose e do pipeline) |
| US02 | Antônio: entrar com a digital | 5 | Dev Mobile 2 (app) e Dev Back-End (API) | QA (E2E), UX (texto e áudio) |
| T11 | Porta de voz: Amazon Polly, cache no S3 e voz do celular sem internet | 5 | Dev Back-End | Dev Mobile 1 (botão "Ouvir") |
| | **Total** | **26** | | |

Como ainda não existe a abertura de conta (US01, sprint 2), a US02 usa um cliente de teste criado pelo script de dados do ambiente de desenvolvimento.

## Critérios de aceite

### T12 · Esqueleto do app

- O app abre no Android 10 e no iOS 16 com as telas de entrada e inicial vazias.
- Todo componente base (botão, campo, texto) tem rótulo de acessibilidade, área de toque de 48 dp e texto base de 18 sp (RNF09).
- O botão "Ouvir" aparece fixo em todas as telas e toca o texto da tela pelo serviço de voz.
- O cliente HTTP do app é gerado a partir do `openapi.yaml` e o build falha se o contrato mudar sem gerar de novo.

### T07 · Razão contábil

- A migração cria `carteira`, `transacao` e `lancamento` conforme o Bloco 5 e roda do zero no Docker Compose.
- Teste de integração: uma transação com lançamentos que não somam zero é **recusada pelo banco**.
- Teste de integração: o saldo de uma carteira é a soma dos seus lançamentos e a rota `GET /v1/contas/me/saldo` responde em menos de 300 ms no p95 com 10.000 lançamentos na carteira (RNF01).

### US02 · Entrar com a digital (copiado do Bloco 2)

Como **Antônio**, quero entrar no app com a minha digital, para não precisar lembrar nem digitar senha.

- **Dado** que criei a senha de 6 números, **quando** aceito usar a biometria, **então** os próximos acessos pedem só a digital.
- **Dado** que errei a senha 5 vezes, **quando** tento a 6ª, **então** o acesso fica bloqueado por 30 minutos e o app explica por voz.
- **Dado** que meu celular não tem biometria, **quando** entro, **então** o app pede a senha de 6 números com teclado grande.

Critérios técnicos que vêm dos RNF e do ADR-010:

- A senha é guardada com Argon2id. O token de acesso vale 15 minutos e o de renovação, 30 dias, trocado a cada uso (RNF05).
- O login exige a assinatura da chave do aparelho guardada no Keystore ou Keychain. A biometria nunca sai do celular.

### T11 · Porta de voz

- `POST /v1/falas` devolve a URL de um áudio para um texto em português.
- Frase fixa repetida é servida do cache no S3 sem chamar o Polly de novo (conferido pelo log).
- Sem internet, o app usa a voz do próprio celular e o usuário não fica sem áudio.
- Em desenvolvimento e no pipeline roda o adaptador falso, sem custo e sem rede.

## Tarefas por pessoa

| Perfil | Tarefas no sprint |
| --- | --- |
| Product Owner | Aceite dos 4 itens na Review. Refinamento de US01, US04, T08 e T02 para o sprint 2. Retomar a conversa com os 2 parceiros BaaS (R04) |
| Tech Lead | T07. Revisão de todo PR de identidade e contas. Scrum Master do sprint |
| Dev Back-End Pleno | Rotas `/auth/login`, `/auth/renovacao`, `/auth/logout` da US02. T11 |
| Dev Mobile 1 | T12 e integração do botão "Ouvir" com o T11 |
| Dev Mobile 2 | Telas de senha, biometria e bloqueio da US02 |
| DevOps (meio período) | PostgreSQL no Docker Compose e no pipeline para o T07. Bucket S3 de áudio em homologação |
| QA | Teste E2E de login com Maestro. Testes de integração do razão junto com o Tech Lead |
| UX | Textos e roteiro de áudio das telas de entrada. Preparar e conduzir o teste com 5 pessoas do perfil |

## Cerimônias e datas

| Cerimônia | Data | Horário |
| --- | --- | --- |
| Sprint Planning | 30/11/2026 | 9h às 11h |
| Daily | Todos os dias úteis | 9h30 |
| Refinamento do sprint 2 | 02/12/2026 | 14h às 15h |
| Teste com 5 usuários | 10/12/2026 | 9h às 13h |
| Sprint Review | 11/12/2026 | 10h às 11h |
| Retrospectiva | 11/12/2026 | 15h às 16h |

## Como saber se o sprint deu certo

Na Review, uma pessoa do perfil do Antônio, com um celular Android de entrada, entra no app só com a digital e ouve a tela inicial sem ninguém ler para ela.
