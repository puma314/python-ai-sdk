from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TS_PACKAGES = ROOT / 'packages'
PY_PACKAGES = ROOT / 'python' / 'packages'

PACKAGE_NAME_MAP = {
  'google-vertex': 'google_vertex',
  'open-responses': 'open_responses',
  'provider-utils': 'provider_utils',
}

TARGET_PACKAGES = [
  'ai',
  'anthropic',
  'cerebras',
  'google',
  'google-vertex',
  'moonshotai',
  'open-responses',
  'openai',
  'provider-utils',
  'xai',
  'provider',
]


@dataclass
class ParityResult:
  package: str
  source_count: int
  translated_count: int
  missing: list[str]
  extra: list[str]


def _to_python_package_name(package_name: str) -> str:
  return PACKAGE_NAME_MAP.get(package_name, package_name.replace('-', '_'))


def _mapped_target_name(relative_path: Path) -> str:
  result = relative_path.as_posix()
  result = result.replace('-', '_')

  if result.endswith('.test-d.ts'):
    return result.removesuffix('.test-d.ts') + '_test.py'
  if result.endswith('.test.ts'):
    return result.removesuffix('.test.ts') + '_test.py'
  if result.endswith('.ts'):
    return result.removesuffix('.ts') + '.py'
  if result.endswith('.tsx'):
    return result.removesuffix('.tsx') + '.py'

  return result


def _collect_source_files(ts_package_root: Path) -> list[Path]:
  return sorted(
    [
      path.relative_to(ts_package_root)
      for path in ts_package_root.rglob('*')
      if path.is_file()
      and path.suffix in {'.ts', '.tsx'}
      and 'node_modules' not in path.parts
    ]
  )


def _collect_translated_files(py_package_root: Path) -> list[str]:
  if not py_package_root.exists():
    return []

  allowed_suffixes = {'.py', '.pyi'}
  return sorted(
    [
      path.relative_to(py_package_root).as_posix()
      for path in py_package_root.rglob('*')
      if path.is_file()
      and path.suffix in allowed_suffixes
      and '__pycache__' not in path.parts
    ]
  )


def check_package(package_name: str) -> ParityResult:
  ts_root = TS_PACKAGES / package_name
  py_root = PY_PACKAGES / _to_python_package_name(package_name)

  source_files = _collect_source_files(ts_root)
  expected = sorted(_mapped_target_name(path) for path in source_files)
  actual = _collect_translated_files(py_root)

  expected_set = set(expected)
  actual_set = set(actual)

  return ParityResult(
    package=package_name,
    source_count=len(expected),
    translated_count=len(actual),
    missing=sorted(expected_set - actual_set),
    extra=sorted(actual_set - expected_set),
  )


def main() -> int:
  failing = False

  for package_name in TARGET_PACKAGES:
    result = check_package(package_name)
    print(
      f'[{result.package}] source={result.source_count} translated={result.translated_count} '
      f'missing={len(result.missing)} extra={len(result.extra)}'
    )
    if result.missing:
      failing = True
      print('  missing sample:')
      for item in result.missing[:10]:
        print(f'    - {item}')
    if result.extra:
      print('  extra sample:')
      for item in result.extra[:10]:
        print(f'    - {item}')

  return 1 if failing else 0


if __name__ == '__main__':
  raise SystemExit(main())
