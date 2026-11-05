import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { carregarConfig } from './compartilhado/config';
import { criarPool } from './compartilhado/banco';
import { CONFIG, POOL } from './compartilhado/tokens';
import { CorrelacaoMiddleware } from './compartilhado/correlacao.middleware';
import { SaudeController } from './saude/saude.controller';
import { ModuloIdentidade } from './modulos/identidade';
import { ModuloContas } from './modulos/contas';
import { ModuloPagamentos } from './modulos/pagamentos';
import { ModuloFamilia } from './modulos/familia';
import { ModuloAntifraude } from './modulos/antifraude';
import { ModuloAtendimento } from './modulos/atendimento';
import { ModuloNotificacao } from './modulos/notificacao';
import { ModuloBackoffice } from './modulos/backoffice';

const config = carregarConfig();

/** Raiz da API: os 8 módulos do monolito modular (ADR-001) e o que é compartilhado. */
@Module({
  imports: [
    ModuloIdentidade,
    ModuloContas,
    ModuloPagamentos,
    ModuloFamilia,
    ModuloAntifraude,
    ModuloAtendimento,
    ModuloNotificacao,
    ModuloBackoffice,
  ],
  controllers: [SaudeController],
  providers: [
    { provide: CONFIG, useValue: config },
    { provide: POOL, useValue: criarPool(config.bancoUrl) },
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(CorrelacaoMiddleware).forRoutes('*');
  }
}
