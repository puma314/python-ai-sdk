"""String URL helpers."""


def withoutTrailingSlash(url: str | None) -> str | None:
  """Remove one trailing slash from a URL string."""

  if url is None:
    return None
  return url[:-1] if url.endswith('/') else url


__all__ = ['withoutTrailingSlash']
