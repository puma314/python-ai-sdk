"""Version string for open_responses package mirror."""

# Version string of this package injected at build time.
__PACKAGE_VERSION__: str | None = None
VERSION: str = __PACKAGE_VERSION__ if __PACKAGE_VERSION__ is not None else '0.0.0-test'
