import type { Pool, PoolClient } from 'pg';
import { log } from '../compartilhado/log';

/** Um evento lido da tabela outbox_evento (ADR-008). */
export interface EventoOutbox {
  id: string;
  tipo: string;
  agregado_id: string;
  payload: unknown;
  tentativas: number;
}

/** Quem trata cada tipo de evento. Precisa ser idempotente: o outbox entrega "pelo menos uma vez". */
export type Tratador = (evento: EventoOutbox, cliente: PoolClient) => Promise<void>;

/** Espera entre tentativas: 2^tentativas segundos, no máximo 15 minutos. */
export function esperaSegundos(tentativas: number): number {
  return Math.min(2 ** tentativas, 900);
}

/**
 * Processa um lote do outbox. Vários workers podem rodar juntos:
 * FOR UPDATE SKIP LOCKED faz cada um pegar eventos diferentes.
 * Devolve quantos eventos foram processados com sucesso.
 */
export async function processarLote(pool: Pool, tratadores: Record<string, Tratador>, lote: number): Promise<number> {
  const cliente = await pool.connect();
  let ok = 0;
  try {
    await cliente.query('begin');
    const { rows } = await cliente.query<EventoOutbox>(
      `select id, tipo, agregado_id, payload, tentativas
         from outbox_evento
        where processado_em is null and proxima_tentativa_em <= now()
        order by id
        limit $1
        for update skip locked`,
      [lote],
    );
    for (const evento of rows) {
      const tratar = tratadores[evento.tipo];
      try {
        await cliente.query('savepoint evento');
        if (!tratar) throw new Error(`sem tratador para ${evento.tipo}`);
        await tratar(evento, cliente);
        await cliente.query('update outbox_evento set processado_em = now() where id = $1', [evento.id]);
        await cliente.query('release savepoint evento');
        ok += 1;
      } catch (erro) {
        await cliente.query('rollback to savepoint evento');
        const tentativas = evento.tentativas + 1;
        await cliente.query(
          `update outbox_evento
              set tentativas = $2, proxima_tentativa_em = now() + make_interval(secs => $3)
            where id = $1`,
          [evento.id, tentativas, esperaSegundos(tentativas)],
        );
        log.warn({ eventoId: evento.id, tipo: evento.tipo, tentativas, erro: erro instanceof Error ? erro.message : String(erro) }, 'evento falhou');
      }
    }
    await cliente.query('commit');
  } catch (erro) {
    await cliente.query('rollback');
    throw erro;
  } finally {
    cliente.release();
  }
  return ok;
}
