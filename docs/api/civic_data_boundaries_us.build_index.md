# Module `civic_data_boundaries_us.build_index`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `get_bbox(gdf: geopandas.geodataframe.GeoDataFrame) -> list[float] | None`

Return bbox as [minx, miny, maxx, maxy] or None.

### `get_index_path() -> pathlib.Path`

Return the default path to the boundaries index CSV file.

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under `src/civic_data_boundaries_us/utils/`.

### `get_states_dir() -> pathlib.Path`

Return the directory containing state boundary data.

### `main() -> pandas.core.frame.DataFrame`

Scan state folders and build a boundaries index CSV.

### `process_state_dir(state_dir: pathlib.Path) -> dict`

Process a single state directory and return a summary row.

### `read_yaml(path: str | pathlib.Path) -> dict[str, typing.Any]`

Read and parse a YAML file into a dictionary.

Args:
    path (str | Path): YAML file path.

Returns:
    dict: Parsed YAML data.
