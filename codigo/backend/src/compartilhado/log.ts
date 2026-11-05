import pino from 'pino';

/**
 * Log estruturado em JSON (RNF13). Uma linha por evento, sempre com
 * o identificador de correlação quando houver requisição.
 * Dados pessoais (CPF, nome, celular, token) nunca entram no log:
 * a lista `redact` apaga esses campos mesmo se alguém os passar por engano.
 */
export const log = pino({
  level: process.env.LOG_NIVEL ?? 'info',
  base: { servico: process.env.SERVICO ?? 'rufus-api', ambiente: process.env.NODE_ENV ?? 'desenvolvimento' },
  timestamp: pino.stdTimeFunctions.isoTime,
  redact: {
    paths: ['cpf', '*.cpf', 'senha', '*.senha', 'token', '*.token', 'authorization', '*.authorization', 'celular', '*.celular'],
    censor: '[removido]',
  },
});
