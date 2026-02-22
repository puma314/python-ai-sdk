"""Package version for the Cerebras provider mirror."""

# Version string of this package injected at build time in TypeScript.
__PACKAGE_VERSION__: str | None = None
VERSION: str = __PACKAGE_VERSION__ if __PACKAGE_VERSION__ is not None else '0.0.0-test'
