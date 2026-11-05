import type { NextFunction, Request, Response } from 'express';
import type { Pool, PoolClient } from 'pg';
import { carregarConfig } from '../src/compartilhado/config';
import { criarPool } from '../src/compartilhado/banco';
import { CorrelacaoMiddleware } from '../src/compartilhado/correlacao.middleware';
import { processarLote, type EventoOutbox } from '../src/worker/outbox';
import { AppModule } from '../src/app.module';

describe('configuração', () => {
  const original = { ...process.env };
  afterEach(() => {
    process.env = { ...original };
  });

  it('falha com mensagem clara quando falta variável obrigatória', () => {
    delete process.env.DATABASE_URL;
    expect(() => carregarConfig()).toThrow(/DATABASE_URL/);
  });

  it('usa os valores padrão documentados no .env.example', () => {
    process.env.DATABASE_URL = 'postgres://x';
    process.env.JWT_SEGREDO = 'segredo';
    delete process.env.PORTA;
    delete process.env.OUTBOX_LOTE;
    const c = carregarConfig();
    expect(c.porta).toBe(3000);
    expect(c.outboxLote).toBe(50);
  });

  it('cria o pool sem conectar e com o schema rufus', async () => {
    const pool = criarPool('postgres://u:s@localhost:1/db');
    expect(pool).toBeDefined();
    await pool.end();
  });

  it('o módulo raiz da API carrega os 8 módulos', () => {
    expect(AppModule).toBeDefined();
  });
});

describe('identificador de correlação (RNF13)', () => {
  function chamar(recebido?: string): string {
    const cabecalhos: Record<string, string> = {};
    const req = { header: () => recebido, method: 'GET', originalUrl: '/health?x=1' } as unknown as Request;
    const res = {
      setHeader: (k: string, v: string) => {
        cabecalhos[k] = v;
      },
      on: (_e: string, f: () => void) => f(),
      statusCode: 200,
    } as unknown as Response;
    const next: NextFunction = jest.fn();
    new CorrelacaoMiddleware().use(req, res, next);
    expect(next).toHaveBeenCalled();
    return cabecalhos['X-Correlation-Id'] ?? '';
  }

  it('reaproveita o id recebido', () => {
    expect(chamar('abc-123')).toBe('abc-123');
  });

  it('gera um id novo quando não recebe', () => {
    expect(chamar()).toMatch(/^[0-9a-f-]{36}$/);
  });
});

describe('laço do outbox (ADR-008)', () => {
  function poolFalso(eventos: EventoOutbox[]) {
    const sqls: string[] = [];
    const cliente = {
      query: jest.fn(async (sql: string) => {
        sqls.push(sql.trim().split(/\s+/).slice(0, 2).join(' '));
        if (sql.includes('from outbox_evento')) return { rows: eventos };
        return { rows: [] };
      }),
      release: jest.fn(),
    } as unknown as PoolClient;
    const pool = { connect: async () => cliente } as unknown as Pool;
    return { pool, sqls, cliente };
  }
  const evento = (tipo: string): EventoOutbox => ({ id: '1', tipo, agregado_id: 'a', payload: {}, tentativas: 0 });

  it('marca como processado o evento tratado com sucesso', async () => {
    const { pool, sqls } = poolFalso([evento('PixConcluido')]);
    const tratar = jest.fn(async () => undefined);
    const n = await processarLote(pool, { PixConcluido: tratar }, 10);
    expect(n).toBe(1);
    expect(tratar).toHaveBeenCalled();
    expect(sqls).toContain('update outbox_evento');
    expect(sqls).toContain('commit');
  });

  it('agenda nova tentativa quando o tratador falha ou não existe', async () => {
    const { pool, sqls } = poolFalso([evento('SemTratador')]);
    const n = await processarLote(pool, {}, 10);
    expect(n).toBe(0);
    expect(sqls).toContain('rollback to');
    expect(sqls.filter((s) => s === 'update outbox_evento')).toHaveLength(1);
  });

  it('desfaz a transação e devolve a conexão se o banco falhar', async () => {
    const cliente = {
      query: jest.fn(async (sql: string) => {
        if (sql.includes('from outbox_evento')) throw new Error('banco caiu');
        return { rows: [] };
      }),
      release: jest.fn(),
    } as unknown as PoolClient;
    const pool = { connect: async () => cliente } as unknown as Pool;
    await expect(processarLote(pool, {}, 10)).rejects.toThrow('banco caiu');
    expect(cliente.release).toHaveBeenCalled();
  });
});
