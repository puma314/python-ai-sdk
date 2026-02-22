"""Build configuration mirror for anthropic package."""

default_export = [
  {
    'entry': ['src/index.ts'],
    'format': ['cjs', 'esm'],
    'dts': True,
    'sourcemap': True,
  },
  {
    'entry': ['src/internal/index.ts'],
    'outDir': 'dist/internal',
    'format': ['cjs', 'esm'],
    'dts': True,
    'sourcemap': True,
  },
]

__all__ = ['default_export']
