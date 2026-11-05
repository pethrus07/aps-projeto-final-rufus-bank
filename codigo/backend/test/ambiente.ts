// Variáveis mínimas para os testes de unidade rodarem sem .env.
// O CI define as suas próprias (ci.yml, job testes) e elas têm prioridade.
process.env.NODE_ENV ??= 'teste';
process.env.DATABASE_URL ??= 'postgres://rufus:rufus_teste@localhost:5432/rufus_teste';
process.env.JWT_SEGREDO ??= 'segredo-de-teste-com-mais-de-32-caracteres';
