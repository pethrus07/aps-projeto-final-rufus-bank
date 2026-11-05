# 8.5 Contrato de API (OpenAPI 3.0)

O contrato está em [openapi.yaml](openapi.yaml), no formato **OpenAPI 3.0.3**, e cobre as **50 rotas** da lista canônica (`bloco-3-arquitetura/06-rotas-da-api.md`). Conferido por script em 04/11/2026: nenhuma rota faltando, nenhuma a mais.

## Como ver

- Com o sistema no ar: http://localhost:3000/docs (Swagger UI).
- Sem o sistema: abrir o `openapi.yaml` no [Swagger Editor](https://editor.swagger.io/).

## Como validar

```
cd bloco-8-dev
npx -y @redocly/cli lint openapi.yaml
```

Resultado em 04/11/2026: `Your API description is valid.` sem erros nem avisos, com as regras recomendadas do Redocly (`redocly.yaml` só desliga o aviso de servidor `localhost`, que é o servidor do Docker Compose de propósito). O CI roda o mesmo comando e bloqueia o merge se o contrato quebrar.

## Regras do contrato

| Regra | Como aparece no contrato |
| --- | --- |
| Dinheiro em centavos inteiros | Todo campo `valorCentavos` é `integer` com `format: int64` |
| Idempotência em toda operação que move dinheiro | Parâmetro `Idempotency-Key` (UUID, obrigatório) em `POST /pix/envios`, `POST /boletos/pagamentos`, `POST /metas/{id}/depositos` e `POST /metas/{id}/resgates`. Repetir a chave devolve 200 com a transação original |
| Autenticação | `bearerAuth` (JWT) por padrão. Rotas públicas com `security: []`. Cadastro com `tokenCadastro`. Webhook com `assinaturaParceiro` (HMAC) |
| Papel exigido nas rotas `/admin` | Extensão `x-papel` (ATENDENTE, ANALISTA_ANTIFRAUDE, ADMINISTRADOR) |
| Erro padronizado | Toda resposta de erro usa o schema `Erro`: `codigo` estável, `mensagem` simples para mostrar e falar, `correlacaoId` |
| Texto para o áudio | Respostas que o app fala trazem `textoFalado` (saldo, extrato, recebedor, boleto) |
| Paginação | Por cursor (`cursor` e `limite`, até 50 itens) |

## Respostas de erro reutilizadas

| Status | Nome | Quando |
| --- | --- | --- |
| 400 | Invalido | Campo faltando ou fora do formato |
| 401 | NaoAutenticado | Token ausente, vencido ou inválido |
| 403 | Proibido | Sem o papel ou sem o vínculo (ABAC) |
| 404 | NaoEncontrado | Recurso não existe ou não é do cliente |
| 409 | Conflito | Já existe ou já foi decidido |
| 422 | RegraDeNegocio | Saldo, limite, conta bloqueada |
| 429 | MuitasRequisicoes | Limite de requisições (WAF e login) |
| 503 | ParceiroIndisponivel | Parceiro BaaS ou voz fora do ar, com a frase "Seu dinheiro não saiu" |
