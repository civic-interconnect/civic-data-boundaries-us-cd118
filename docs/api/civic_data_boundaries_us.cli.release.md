# Module `civic_data_boundaries_us.cli.release`

## Functions

### `bump_version(old: str, new: str)`

Bump version number in pyproject.toml.

Args:
    old: Old version string (e.g., 0.1.0)
    new: New version string (e.g., 0.2.0)

### `tag_release(version: str)`

Create and push a Git release tag.

Args:
    version: Version string to tag (e.g., 0.2.0)
