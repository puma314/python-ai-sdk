
## provider scaffold run — 2026-02-22

[provider] [NOTE] Scaffolded 35 directories, 133 total .py files (35 __init__.py + 98 stub modules) for python/packages/provider.

[provider] [NOTE] Source tree had 140 .ts files in packages/provider/src/. All meaningful files mapped and stubbed.

[provider] [NOTE] Files skipped (build/config/docs):
  - packages/provider/CHANGELOG.md (SKIP: docs)
  - packages/provider/README.md (SKIP: docs)
  - packages/provider/package.json (SKIP: build config)
  - packages/provider/tsconfig.json (SKIP: build config)
  - packages/provider/tsconfig.build.json (SKIP: build config)
  - packages/provider/tsup.config.ts (SKIP: build config)
  - packages/provider/turbo.json (SKIP: build config)

[provider] [NOTE] Root-level src/index.ts mapped to python/packages/provider/__init__.py as the package public API barrel.

[provider] [NOTE] All sub-directory index.ts barrel files mapped to __init__.py in their respective directories.

[provider] [NOTE] kebab-case → snake_case conversion applied to all filenames and directory names (e.g., language-model → language_model, ai-sdk-error → ai_sdk_error).

[provider] [NOTE] Versioned subdirectories (v2/, v3/) preserved as-is per mapping rules.

[provider] [NOTE] No test files (.test.ts) or type-declaration files (.test-d.ts) were present in packages/provider/src/ — nothing to skip or map there.

[provider] [NOTE] No __fixtures__ JSON files found in this package.

[provider] [NOTE] The `provider` subdirectory inside python/packages/provider/ shadows the package name. This may require import path care during implementation (e.g., from provider.provider.v3.provider_v3 import ...).

[provider] [QUESTION] The v2 language model has `language-model-v2-provider-defined-tool.ts` while v3 has `language-model-v3-provider-tool.ts` — naming is asymmetric. Confirm this is intentional in the TS source and should be preserved as-is in the Python stubs.

[provider] [NEEDS HUMAN] `embedding-model/v2` only has `embedding-model-v2.ts` and `embedding-model-v2-embedding.ts` (no call-options, no result). The v3 counterpart adds call-options, result, and embedding types. Translator should check if v2 types are subsumed by v3 or remain independently maintained.
