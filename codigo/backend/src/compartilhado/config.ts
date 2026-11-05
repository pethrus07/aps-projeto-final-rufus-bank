/**
 * Lê e valida as variáveis de ambiente uma vez só, na partida.
 * Variável obrigatória ausente derruba o processo com mensagem clara,
 * em vez de falhar mais tarde no meio de uma requisição.
 * A lista completa e comentada está em codigo/.env.example.
 */
export interface Config {
  ambiente: 'desenvolvimento' | 'homologacao' | 'producao' | 'teste';
  porta: number;
  bancoUrl: string;
  openapiCaminho: string;
  nivelLog: string;
  jwtSegredo: string;
  outboxIntervaloMs: number;
  outboxLote: number;
}

function obrigatoria(nome: string): string {
  const valor = process.env[nome];
  if (!valor) {
    throw new Error(`Variável de ambiente obrigatória ausente: ${nome} (veja .env.example)`);
  }
  return valor;
}

export function carregarConfig(): Config {
  const ambiente = (process.env.NODE_ENV ?? 'desenvolvimento') as Config['ambiente'];
  return {
    ambiente,
    porta: Number(process.env.PORTA ?? 3000),
    bancoUrl: obrigatoria('DATABASE_URL'),
    openapiCaminho: process.env.OPENAPI_CAMINHO ?? '../../bloco-8-dev/openapi.yaml',
    nivelLog: process.env.LOG_NIVEL ?? 'info',
    jwtSegredo: obrigatoria('JWT_SEGREDO'),
    outboxIntervaloMs: Number(process.env.OUTBOX_INTERVALO_MS ?? 1000),
    outboxLote: Number(process.env.OUTBOX_LOTE ?? 50),
  };
}
