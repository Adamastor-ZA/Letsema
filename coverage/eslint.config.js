import js from '@eslint/js'
import reactHooks from 'eslint-plugin-react-hooks'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist', 'node_modules'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ['src/ui/**/*.{ts,tsx}'],
    plugins: { 'react-hooks': reactHooks },
    rules: reactHooks.configs.recommended.rules,
  },
  {
    // The projection engine must stay pure: no framework, storage, clock, randomness or network.
    files: ['src/engine/**/*.ts'],
    ignores: ['src/engine/**/*.test.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            { group: ['react', 'react-*', 'dexie', 'dexie-*', 'recharts', 'zod'], message: 'The engine is framework-free.' },
            { group: ['**/db/**', '**/ui/**', '**/schema/**', '**/sample/**'], message: 'The engine may only import from src/engine.' },
          ],
        },
      ],
      'no-restricted-globals': [
        'error',
        ...['Date', 'fetch', 'XMLHttpRequest', 'WebSocket', 'window', 'document', 'localStorage', 'indexedDB', 'navigator'].map(
          (name) => ({ name, message: 'The engine must be deterministic and side-effect free.' }),
        ),
      ],
      'no-restricted-properties': ['error', { object: 'Math', property: 'random', message: 'The engine must be deterministic.' }],
    },
  },
)
