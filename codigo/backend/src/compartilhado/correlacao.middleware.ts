import { randomUUID } from 'node:crypto';
import { Injectable, NestMiddleware } from '@nestjs/common';
import type { NextFunction, Request, Response } from 'express';
import { log } from './log';

/**
 * Garante um identificador de correlação em 100% das requisições (RNF13).
 * Usa o X-Correlation-Id recebido ou gera um novo, devolve no cabeçalho
 * da resposta e registra uma linha de log com rota, status e duração.
 */
@Injectable()
export class CorrelacaoMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction): void {
    const recebido = req.header('x-correlation-id');
    const correlacaoId = recebido && recebido.length <= 64 ? recebido : randomUUID();
    res.setHeader('X-Correlation-Id', correlacaoId);
    const inicio = process.hrtime.bigint();
    res.on('finish', () => {
      const duracaoMs = Number(process.hrtime.bigint() - inicio) / 1e6;
      log.info({ correlacaoId, metodo: req.method, rota: req.originalUrl.split('?')[0], status: res.statusCode, duracaoMs }, 'requisicao');
    });
    next();
  }
}
