# Module `civic_data_boundaries_us.utils.get_paths`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `get_cd118_in_dir() -> pathlib.Path`

Return the folder under data-in/ where raw CD118 shapefiles are extracted.

### `get_cd118_out_dir() -> pathlib.Path`

Return the directory under data-out/national/ where CD118 geojsons are stored.

### `get_data_in_dir() -> pathlib.Path`

Return the root data-in directory for raw input data (downloads, archives).

### `get_data_out_dir() -> pathlib.Path`

Return the root data-out directory for processed GeoJSON and chunked outputs.

### `get_national_out_dir() -> pathlib.Path`

Return the directory under data-out/ where national-level files are written.
Includes layers like national states, counties, or CD118 merged geojsons.

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under:
    src/civic_data_boundaries_us/utils/

### `get_states_out_dir() -> pathlib.Path`

Return the directory under data-out/ where per-state folders are written.

### `get_tiger_in_dir() -> pathlib.Path`

Return the folder under data-in/ where TIGER shapefiles are stored after download and extraction.
