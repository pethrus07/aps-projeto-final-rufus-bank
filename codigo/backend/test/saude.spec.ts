import { Test } from '@nestjs/testing';
import type { INestApplication } from '@nestjs/common';
import request from 'supertest';
import { SaudeController } from '../src/saude/saude.controller';
import { POOL } from '../src/compartilhado/tokens';
import { esperaSegundos } from '../src/worker/outbox';

describe('GET /health', () => {
  async function montar(query: () => Promise<unknown>): Promise<INestApplication> {
    const modulo = await Test.createTestingModule({
      controllers: [SaudeController],
      providers: [{ provide: POOL, useValue: { query } }],
    }).compile();
    const app = modulo.createNestApplication();
    await app.init();
    return app;
  }

  it('responde 200 quando o banco responde', async () => {
    const app = await montar(async () => ({ rows: [] }));
    const r = await request(app.getHttpServer()).get('/health');
    expect(r.status).toBe(200);
    expect(r.body).toMatchObject({ status: 'ok', banco: 'ok' });
    await app.close();
  });

  it('responde 503 quando o banco cai', async () => {
    const app = await montar(async () => {
      throw new Error('sem conexao');
    });
    const r = await request(app.getHttpServer()).get('/health');
    expect(r.status).toBe(503);
    await app.close();
  });
});

describe('espera do outbox', () => {
  it('cresce em potência de 2 e para em 15 minutos', () => {
    expect(esperaSegundos(1)).toBe(2);
    expect(esperaSegundos(5)).toBe(32);
    expect(esperaSegundos(20)).toBe(900);
  });
});
