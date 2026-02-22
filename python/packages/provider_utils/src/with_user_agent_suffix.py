"""User-agent header helpers."""

from __future__ import annotations


def withUserAgentSuffix(
  headers: dict[str, str],
  suffix: str,
) -> dict[str, str]:
  """Append SDK suffix to an existing user-agent header."""

  merged = dict(headers)
  current = merged.get('user-agent') or merged.get('User-Agent')
  merged['user-agent'] = f'{current} {suffix}'.strip() if current else suffix
  return merged


__all__ = ['withUserAgentSuffix']
