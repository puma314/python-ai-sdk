"""Forward Anthropic container IDs between multi-step calls."""

from __future__ import annotations

from typing import TypedDict


class _Step(TypedDict, total=False):
  providerMetadata: dict[str, dict[str, object]]


def forwardAnthropicContainerIdFromLastStep(
  *,
  steps: list[_Step],
) -> dict[str, object] | None:
  """Return provider options carrying forward the newest container id."""

  for index in range(len(steps) - 1, -1, -1):
    step = steps[index]
    provider_metadata = step.get('providerMetadata') or {}
    anthropic = provider_metadata.get('anthropic')
    if not isinstance(anthropic, dict):
      continue
    container = anthropic.get('container')
    if not isinstance(container, dict):
      continue
    container_id = container.get('id')
    if isinstance(container_id, str) and container_id:
      return {
        'providerOptions': {
          'anthropic': {
            'container': {'id': container_id},
          }
        }
      }
  return None


__all__ = ['forwardAnthropicContainerIdFromLastStep']
