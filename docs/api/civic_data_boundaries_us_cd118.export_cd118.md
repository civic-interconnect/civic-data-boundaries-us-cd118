# Module `civic_data_boundaries_us_cd118.export_cd118`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `export_cd118()`

Export CD118 boundaries:
  - a nationwide GeoJSON
  - one GeoJSON per state

### `get_national_out_dir() -> pathlib.Path`

Return the directory under data-out/ where national-level files are written.
Includes layers like national states, counties, or CD118 merged geojsons.

### `get_state_dir_name(state_abbr: str) -> str`

Return the standardized directory name for a state (full lowercase name with underscores).

### `get_states_out_dir() -> pathlib.Path`

Return the directory under data-out/ where per-state folders are written.

### `get_tiger_in_dir() -> pathlib.Path`

Return the folder under data-in/ where TIGER shapefiles are stored after download and extraction.

### `load_cd118_layer(shp_path: pathlib.Path) -> geopandas.geodataframe.GeoDataFrame`

Load a single CD118 shapefile.

### `load_layer_config(layer_name: str) -> dict`

Load configuration for a given layer, merged with global defaults.

### `main() -> int`

Run CD118 export.

Returns:
    int: 0 if successful, 1 on error.

### `read_yaml(path: str | pathlib.Path) -> dict[str, typing.Any]`

Read and parse a YAML file into a dictionary.

Args:
    path (str | Path): YAML file path.

Returns:
    dict: Parsed YAML data.

### `today_utc_str() -> str`

Return today's date in UTC in 'YYYY-MM-DD' format.

Returns:
    str: Current UTC date as a string.

### `validate_columns(gdf: geopandas.geodataframe.GeoDataFrame, columns: list[str], label: str)`

No description available.

### `write_yaml(data: dict[str, typing.Any], path: str | pathlib.Path) -> pathlib.Path`

Write a dictionary to a YAML file.

Args:
    data (dict): Data to write.
    path (str | Path): File path to write to.

Returns:
    Path: The path the file was written to.

