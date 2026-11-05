# syntax=docker/dockerfile:1
# Imagem da API do Rufus Bank. Build em 3 estágios (Bloco 6, containerização):
#   1. build   instala tudo e compila o TypeScript
#   2. deps    instala só as dependências de produção
#   3. final   node:22-alpine com o JavaScript compilado, sem compilador nem devDependencies
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
ENV NODE_ENV=producao SERVICO=rufus-api PORTA=3000
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
# roda sem root: o usuário "node" já existe na imagem oficial
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1
CMD ["node", "dist/main.js"]
