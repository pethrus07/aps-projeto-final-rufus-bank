import { Controller, Get, HttpCode, HttpException, HttpStatus, Inject } from '@nestjs/common';
import type { Pool } from 'pg';
import { POOL } from '../compartilhado/tokens';

/**
 * Endpoint de saúde usado pelo balanceador (ALB), pela verificação externa
 * de disponibilidade (RNF03) e pelo smoke test do pipeline.
 * Responde 200 só se o banco também responder; senão 503.
 */
@Controller()
export class SaudeController {
  constructor(@Inject(POOL) private readonly pool: Pool) {}

  @Get(['health', 'v1/health'])
  @HttpCode(200)
  async verificar(): Promise<{ status: string; banco: string; versao: string }> {
    try {
      await this.pool.query('select 1');
    } catch {
      throw new HttpException({ status: 'erro', banco: 'indisponivel' }, HttpStatus.SERVICE_UNAVAILABLE);
    }
    return { status: 'ok', banco: 'ok', versao: process.env.VERSAO ?? 'dev' };
  }
}
