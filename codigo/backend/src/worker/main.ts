import { carregarConfig } from '../compartilhado/config';
import { criarPool } from '../compartilhado/banco';
import { log } from '../compartilhado/log';
import { processarLote, type Tratador } from './outbox';

/**
 * Worker: lê o outbox em laço (ADR-008).
 * Esqueleto: os tratadores reais (enviar Pix ao parceiro, push, avisar
 * contato de confiança) entram nos sprints. O tratador de exemplo só registra.
 */
const tratadores: Record<string, Tratador> = {
  ExemploPing: async (evento) => {
    log.info({ eventoId: evento.id }, 'ping recebido');
  },
};

async function iniciar(): Promise<void> {
  const config = carregarConfig();
  const pool = criarPool(config.bancoUrl);
  let ativo = true;
  const parar = (): void => {
    ativo = false;
  };
  process.on('SIGTERM', parar);
  process.on('SIGINT', parar);
  log.info({ intervaloMs: config.outboxIntervaloMs, lote: config.outboxLote }, 'worker no ar');

  while (ativo) {
    try {
      const n = await processarLote(pool, tratadores, config.outboxLote);
      if (n > 0) log.info({ processados: n }, 'lote do outbox');
    } catch (erro) {
      log.error({ erro: erro instanceof Error ? erro.message : String(erro) }, 'falha ao ler o outbox');
    }
    await new Promise((r) => setTimeout(r, config.outboxIntervaloMs));
  }
  await pool.end();
  log.info('worker parado');
}

void iniciar();
