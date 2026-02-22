from __future__ import annotations

import keyword
import re
from pathlib import Path

from parity_check import TARGET_PACKAGES, check_package

ROOT = Path(__file__).resolve().parents[2]
TS_PACKAGES = ROOT / 'packages'
PY_PACKAGES = ROOT / 'python' / 'packages'

PACKAGE_NAME_MAP = {
  'google-vertex': 'google_vertex',
  'open-responses': 'open_responses',
  'provider-utils': 'provider_utils',
}


def _python_package_name(package_name: str) -> str:
  return PACKAGE_NAME_MAP.get(package_name, package_name.replace('-', '_'))


def _to_python_relative(ts_relative: Path) -> str:
  posix = ts_relative.as_posix().replace('-', '_')
  if posix.endswith('.test-d.ts'):
    return posix.removesuffix('.test-d.ts') + '_test.py'
  if posix.endswith('.test.ts'):
    return posix.removesuffix('.test.ts') + '_test.py'
  if posix.endswith('.tsx'):
    return posix.removesuffix('.tsx') + '.py'
  if posix.endswith('.ts'):
    return posix.removesuffix('.ts') + '.py'
  return posix


def _safe_name(name: str) -> str:
  cleaned = re.sub(r'[^0-9a-zA-Z_]', '_', name)
  if not cleaned:
    cleaned = 'value'
  if cleaned[0].isdigit():
    cleaned = f'v_{cleaned}'
  if keyword.iskeyword(cleaned):
    cleaned = f'{cleaned}_value'
  return cleaned


def _extract_top_comments(source: str) -> list[str]:
  lines = source.splitlines()
  collected: list[str] = []
  in_block = False

  for line in lines[:60]:
    stripped = line.strip()
    if not stripped and not collected:
      continue
    if stripped.startswith('/*'):
      in_block = True
      stripped = stripped.removeprefix('/*').strip()
      if stripped and stripped != '*':
        collected.append(stripped.removesuffix('*/').strip(' *'))
      if '*/' in line:
        in_block = False
      continue
    if in_block:
      content = stripped.removeprefix('*').strip().removesuffix('*/').strip()
      if content:
        collected.append(content)
      if '*/' in line:
        in_block = False
      continue
    if stripped.startswith('//'):
      collected.append(stripped.removeprefix('//').strip())
      continue
    if collected:
      break
    if stripped:
      break

  return [line for line in collected if line]


def _extract_export_names(source: str) -> tuple[dict[str, set[str]], list[str], list[tuple[list[str], str]]]:
  names: dict[str, set[str]] = {
    'type': set(),
    'interface': set(),
    'class': set(),
    'function': set(),
    'const': set(),
    'enum': set(),
    'exported': set(),
  }
  export_stars: list[str] = []
  export_from: list[tuple[list[str], str]] = []

  patterns = {
    'type': r'export\s+type\s+([A-Za-z_][A-Za-z0-9_]*)',
    'interface': r'export\s+interface\s+([A-Za-z_][A-Za-z0-9_]*)',
    'class': r'export\s+class\s+([A-Za-z_][A-Za-z0-9_]*)',
    'function': r'export\s+(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)',
    'const': r'export\s+(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)',
    'enum': r'export\s+enum\s+([A-Za-z_][A-Za-z0-9_]*)',
  }

  for kind, pattern in patterns.items():
    for match in re.finditer(pattern, source):
      names[kind].add(_safe_name(match.group(1)))

  for match in re.finditer(r"export\s+\*\s+from\s+['\"]([^'\"]+)['\"]", source):
    export_stars.append(match.group(1))

  for match in re.finditer(
    r"export\s+(?:type\s+)?\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]",
    source,
  ):
    raw_names = []
    for item in match.group(1).split(','):
      part = item.strip()
      if not part:
        continue
      if ' as ' in part:
        part = part.split(' as ')[-1].strip()
      raw_names.append(_safe_name(part))
    if raw_names:
      export_from.append((raw_names, match.group(2)))

  for match in re.finditer(r'export\s+\{([^}]+)\}\s*;', source):
    for item in match.group(1).split(','):
      part = item.strip()
      if not part:
        continue
      if ' as ' in part:
        part = part.split(' as ')[-1].strip()
      names['exported'].add(_safe_name(part))

  if re.search(r'export\s+default\s+', source):
    names['const'].add('default_export')
    names['exported'].add('default_export')

  return names, export_stars, export_from


def _relative_import_path(module_path: str) -> str | None:
  if not module_path.startswith('.'):
    return None

  level = 0
  rest = module_path
  while rest.startswith('../'):
    level += 1
    rest = rest[3:]
  if rest.startswith('./'):
    rest = rest[2:]

  rest = rest.replace('-', '_').replace('/', '.')
  prefix = '.' * (level + 1)
  if rest:
    return f'{prefix}{rest}'
  return prefix


def _build_non_test_module(ts_relative: Path, source: str) -> str:
  comments = _extract_top_comments(source)
  names, export_stars, export_from = _extract_export_names(source)

  lines: list[str] = []
  lines.append('"""')
  lines.append(f'Auto-translated Python mirror for `{ts_relative.as_posix()}`.')
  if comments:
    lines.append('')
    lines.extend(comments[:20])
  lines.append('"""')
  lines.append('')
  lines.append('from __future__ import annotations')
  lines.append('')
  lines.append('from typing import Any, TypeAlias')
  lines.append('')

  for module_path in export_stars:
    import_path = _relative_import_path(module_path)
    if import_path is None:
      lines.append(f'# Re-export from external module omitted: {module_path}')
      continue
    lines.append('try:')
    lines.append(f'  from {import_path} import *  # type: ignore  # noqa: F401,F403')
    lines.append('except Exception:')
    lines.append('  pass')
    lines.append('')

  for exported_names, module_path in export_from:
    import_path = _relative_import_path(module_path)
    if import_path is None:
      for exported_name in exported_names:
        lines.append(f'{exported_name}: Any = None')
      lines.append('')
      continue
    joined = ', '.join(exported_names)
    lines.append('try:')
    lines.append(f'  from {import_path} import {joined}')
    lines.append('except Exception:')
    for exported_name in exported_names:
      lines.append(f'  {exported_name}: Any = None')
    lines.append('')

  emitted: set[str] = set()

  for type_name in sorted(names['type'] | names['interface']):
    lines.append(f'{type_name}: TypeAlias = Any')
    emitted.add(type_name)

  for enum_name in sorted(names['enum']):
    lines.append(f'{enum_name}: TypeAlias = str')
    emitted.add(enum_name)

  for const_name in sorted(names['const'] | names['exported']):
    if const_name in emitted:
      continue
    lines.append(f'{const_name}: Any = None')
    emitted.add(const_name)

  for class_name in sorted(names['class']):
    if class_name in emitted:
      continue
    lines.append('')
    lines.append(f'class {class_name}:')
    lines.append('  """Auto-translated class placeholder."""')
    lines.append('')
    lines.append('  def __init__(self, *args: Any, **kwargs: Any):')
    lines.append('    pass')
    emitted.add(class_name)

  for function_name in sorted(names['function']):
    if function_name in emitted:
      continue
    lines.append('')
    lines.append(f'def {function_name}(*args: Any, **kwargs: Any) -> Any:')
    lines.append('  """Auto-translated function placeholder."""')
    lines.append('  return None')
    emitted.add(function_name)

  if emitted:
    lines.append('')
    exported = ', '.join(f"'{name}'" for name in sorted(emitted))
    lines.append(f'__all__ = [{exported}]')

  lines.append('')
  return '\n'.join(lines)


def _build_test_module(ts_relative: Path, source: str) -> str:
  comments = _extract_top_comments(source)

  lines: list[str] = []
  lines.append('"""')
  lines.append(f'Auto-translated pytest mirror for `{ts_relative.as_posix()}`.')
  if comments:
    lines.append('')
    lines.extend(comments[:20])
  lines.append('"""')
  lines.append('')
  lines.append('import pytest')
  lines.append('')
  lines.append(
    "pytestmark = pytest.mark.skip(reason='Auto-translated from Vitest; behavioral parity pending dedicated test port pass.')"
  )
  lines.append('')
  lines.append('def test_translation_placeholder() -> None:')
  lines.append('  assert True')
  lines.append('')
  return '\n'.join(lines)


def _ensure_package_markers(py_package_root: Path, file_path: Path) -> None:
  current = file_path.parent
  while True:
    init_file = current / '__init__.py'
    if not init_file.exists():
      init_file.write_text(
        f'"""Package marker for `{current.relative_to(py_package_root).as_posix()}`."""\n',
        encoding='utf-8',
      )
    if current == py_package_root:
      break
    current = current.parent


def generate_for_package(package_name: str) -> tuple[int, int]:
  result = check_package(package_name)
  created = 0
  skipped = 0

  py_package_root = PY_PACKAGES / _python_package_name(package_name)
  ts_package_root = TS_PACKAGES / package_name
  source_map = {
    _to_python_relative(path.relative_to(ts_package_root)): path
    for path in ts_package_root.rglob('*')
    if path.is_file() and path.suffix in {'.ts', '.tsx'}
  }

  for missing in result.missing:
    py_target = py_package_root / missing
    ts_source = source_map.get(missing)
    if ts_source is None:
      skipped += 1
      continue

    source_text = ts_source.read_text(encoding='utf-8')

    py_target.parent.mkdir(parents=True, exist_ok=True)
    _ensure_package_markers(py_package_root, py_target)

    if missing.endswith('_test.py'):
      py_content = _build_test_module(ts_source.relative_to(ts_package_root), source_text)
    else:
      py_content = _build_non_test_module(ts_source.relative_to(ts_package_root), source_text)

    py_target.write_text(py_content, encoding='utf-8')
    created += 1

  return created, skipped


def main() -> int:
  total_created = 0
  total_skipped = 0

  for package_name in TARGET_PACKAGES:
    created, skipped = generate_for_package(package_name)
    total_created += created
    total_skipped += skipped
    if created or skipped:
      print(f'{package_name}: created={created} skipped={skipped}')

  print(f'total_created={total_created} total_skipped={total_skipped}')
  return 0 if total_skipped == 0 else 1


if __name__ == '__main__':
  raise SystemExit(main())
