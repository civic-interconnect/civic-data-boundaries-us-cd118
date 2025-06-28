# Module `civic_data_boundaries_us_cd118.fetch`

## Classes

### `FetchError(self, /, *args, **kwargs)`

Custom exception for TIGER fetch errors.

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `download_file(url: str, dest_path: pathlib.Path) -> pathlib.Path`

Download a file from a URL to a destination path.

Returns:
    Path to the downloaded file.

Raises:
    FetchError if the download fails.

### `extract_zip(zip_path: pathlib.Path, extract_to: pathlib.Path) -> None`

Extracts a ZIP file into a target folder.

Raises:
    FileNotFoundError if zip file is missing.
    FetchError if extraction fails.

### `get_data_in_dir() -> pathlib.Path`

Return the root data-in directory for raw input data (downloads, archives).

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under:
    src/civic_data_boundaries_us/utils/

### `main() -> int`

Main entrypoint for fetching all layers defined in YAML configs.

Returns:
    0 if successful, 1 otherwise.

### `process_layer(layer: dict) -> None`

Process a single layer from YAML config:
- create folders
- download zip files
- extract them

