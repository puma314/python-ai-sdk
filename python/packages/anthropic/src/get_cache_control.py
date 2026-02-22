"""Cache-control extraction and validation for Anthropic requests."""

from __future__ import annotations

from typing import TypedDict
from typing import cast

from packages.provider.src.shared.v3.shared_v3_warning import SharedV3Warning


class AnthropicCacheControl(TypedDict):
  """Anthropic cache-control object."""

  type: str


class _AnthropicProviderMetadata(TypedDict, total=False):
  cacheControl: AnthropicCacheControl
  cache_control: AnthropicCacheControl


MAX_CACHE_BREAKPOINTS = 4


def _getCacheControl(
  providerMetadata: dict[str, object] | None,
) -> AnthropicCacheControl | None:
  """Extract cache_control from anthropic provider metadata."""

  anthropic = None
  if providerMetadata is not None:
    candidate = providerMetadata.get('anthropic')
    if isinstance(candidate, dict):
      anthropic = candidate
  if anthropic is None:
    return None
  cache_control = anthropic.get('cacheControl') or anthropic.get('cache_control')
  return cast(AnthropicCacheControl, cache_control) if isinstance(cache_control, dict) else None


class CacheControlValidator:
  """Validate cache-control usage and enforce Anthropic breakpoints limit."""

  def __init__(self) -> None:
    self.breakpointCount = 0
    self.warnings: list[SharedV3Warning] = []

  def getCacheControl(
    self,
    providerMetadata: dict[str, object] | None,
    context: dict[str, object],
  ) -> AnthropicCacheControl | None:
    cache_control = _getCacheControl(providerMetadata)
    if cache_control is None:
      return None

    can_cache = bool(context.get('canCache'))
    context_type = str(context.get('type', 'unknown context'))

    if not can_cache:
      self.warnings.append(
        {
          'type': 'unsupported',
          'feature': 'cache_control on non-cacheable context',
          'details': f'cache_control cannot be set on {context_type}. It will be ignored.',
        }
      )
      return None

    self.breakpointCount += 1
    if self.breakpointCount > MAX_CACHE_BREAKPOINTS:
      self.warnings.append(
        {
          'type': 'unsupported',
          'feature': 'cacheControl breakpoint limit',
          'details': (
            f'Maximum {MAX_CACHE_BREAKPOINTS} cache breakpoints exceeded '
            f'(found {self.breakpointCount}). This breakpoint will be ignored.'
          ),
        }
      )
      return None

    return cache_control

  def getWarnings(self) -> list[SharedV3Warning]:
    """Return validation warnings accumulated so far."""

    return self.warnings


__all__ = ['AnthropicCacheControl', 'CacheControlValidator']
