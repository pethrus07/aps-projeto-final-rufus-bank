import 'reflect-metadata';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { NestFactory } from '@nestjs/core';
import { load } from 'js-yaml';
import swaggerUi from 'swagger-ui-express';
import { AppModule } from './app.module';
import { carregarConfig } from './compartilhado/config';
import { log } from './compartilhado/log';

/** Partida da API. Escuta na porta 3000 (06-rotas-da-api.md). */
async function iniciar(): Promise<void> {
  const config = carregarConfig();
  const app = await NestFactory.create(AppModule, { logger: ['error', 'warn'] });
  app.enableShutdownHooks();
  // não anunciar o framework no cabeçalho (OWASP A05, bloco-6-infra/04-seguranca.md)
  app.getHttpAdapter().getInstance().disable('x-powered-by');

  // Contrato OpenAPI 3.0 (bloco-8-dev/openapi.yaml) navegável em /docs.
  // Em produção /docs não é publicado: o contrato fica no repositório.
  if (config.ambiente !== 'producao') {
    const contrato = load(readFileSync(resolve(config.openapiCaminho), 'utf-8')) as swaggerUi.JsonObject;
    app.use('/docs', swaggerUi.serve, swaggerUi.setup(contrato, { customSiteTitle: 'Rufus Bank API' }));
  }

  await app.listen(config.porta, '0.0.0.0');
  log.info({ porta: config.porta, ambiente: config.ambiente }, 'api no ar');
}

iniciar().catch((erro: unknown) => {
  log.fatal({ erro: erro instanceof Error ? erro.message : String(erro) }, 'api nao subiu');
  process.exit(1);
});
