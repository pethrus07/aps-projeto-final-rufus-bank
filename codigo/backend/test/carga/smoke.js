// Carga curta do smoke test em homologação (cd.yml, etapa 7).
// 20 usuários virtuais por 30 segundos no /health.
// Reprova se o p95 passar de 300 ms (RNF01) ou se mais de 1% falhar.
/* global __ENV */
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 20,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(95)<300'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const r = http.get(`${__ENV.BASE_URL}/health`);
  check(r, { 'status 200': (x) => x.status === 200 });
}
