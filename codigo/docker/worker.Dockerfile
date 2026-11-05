# syntax=docker/dockerfile:1
# Imagem do worker do outbox (ADR-008). Mesmo código da API (ADR-001),
# mesmo build em 3 estágios, outro processo de entrada e sem porta exposta.
# Contexto do build: codigo/backend

FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY tsconfig.json tsconfig.build.json ./
COPY src ./src
RUN npm run build

FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --no-audit --no-fund

FROM node:22-alpine AS final
ENV NODE_ENV=producao SERVICO=rufus-worker
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
USER node
# o worker não recebe requisições: a saúde é medida pela idade do evento
# mais antigo pendente no outbox (alarme do Bloco 6, observabilidade)
CMD ["node", "dist/worker/main.js"]
