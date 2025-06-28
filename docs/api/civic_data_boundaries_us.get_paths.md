# Module `civic_data_boundaries_us.get_paths`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `get_cd118_dir() -> pathlib.Path`

Return the directory for congressional district 118 data.
This is where the 118th Congressional District data is stored.

### `get_congress_dir() -> pathlib.Path`

Return the directory for congressional district data.
This is specifically for congressional districts (CD118).

### `get_data_dir() -> pathlib.Path`

Return the main data directory for this package.
This is where all boundary data is stored.

### `get_national_dir() -> pathlib.Path`

Return the directory for national boundary data.
This includes congressional districts and other national boundaries.

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under `src/civic_data_boundaries_us/utils/`.

### `get_states_dir() -> pathlib.Path`

Return the directory containing state boundary data.
