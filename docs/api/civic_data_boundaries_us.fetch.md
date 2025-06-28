# Module `civic_data_boundaries_us.fetch`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `download_file(url: str, dest_path: pathlib.Path)`

No description available.

### `extract_zip(zip_path: pathlib.Path, extract_to: pathlib.Path)`

No description available.

### `get_data_in_dir() -> pathlib.Path`

Return the root data-in directory for raw input data (downloads, archives).

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under:
    src/civic_data_boundaries_us/utils/

### `main() -> int`

No description available.

### `process_layer(layer: dict)`

No description available.
