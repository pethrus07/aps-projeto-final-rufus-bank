import { Pool } from 'pg';

/**
 * Pool de conexões com o PostgreSQL. Uma instância por processo.
 * Máximo de 10 conexões por tarefa: com 6 tarefas da API no pico (RNF04)
 * e 1 worker, ficam no máximo 70 conexões, abaixo do limite do db.t4g.medium.
 */
export function criarPool(url: string): Pool {
  // search_path fixo no schema "rufus" (Bloco 5): não depende do nome do usuário do banco
  return new Pool({ connectionString: url, max: 10, idleTimeoutMillis: 30_000, options: '-c search_path=rufus' });
}
