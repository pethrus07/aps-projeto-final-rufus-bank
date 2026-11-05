// Regras de lint do backend.
// A regra no-restricted-imports protege a fronteira dos módulos (ADR-001):
// um módulo só importa o index.ts público de outro módulo, nunca as camadas
// internas dele (dominio, aplicacao, infraestrutura, http).
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

const camadas = ['dominio', 'aplicacao', 'infraestrutura', 'http'];

export default tseslint.config(
  { ignores: ['dist/**', 'coverage/**', 'node_modules/**', 'eslint.config.mjs'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      'no-console': 'error',
      // fora de src/modulos: só pelo index.ts do módulo
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: camadas.map((c) => `**/modulos/*/${c}/**`),
              message: 'Importe só o index.ts público do módulo (ADR-001).',
            },
          ],
        },
      ],
    },
  },
  {
    // dentro de src/modulos/<modulo>/<camada>/: a própria camada vizinha (../x) é livre,
    // a camada de OUTRO módulo (../../outro/x) é proibida
    files: ['src/modulos/*/*/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: camadas.map((c) => `../../*/${c}/**`),
              message: 'Outro módulo só pelo index.ts público (ADR-001).',
            },
          ],
        },
      ],
    },
  },
);
