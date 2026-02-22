# Python AI SDK

## Development Commands

All commands should be run from the `python/` directory.

### Linting

```bash
uv run ruff check .          # Check for lint errors
uv run ruff check --fix .    # Auto-fix lint errors
```

### Formatting

```bash
uv run ruff format .          # Format all files
uv run ruff format --check .  # Check formatting without modifying files
```

### Type-checking

```bash
uv run pyright .  # Run static type analysis
```
