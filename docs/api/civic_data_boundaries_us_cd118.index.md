# Module `civic_data_boundaries_us_cd118.index`

## Classes

### `IndexBuildError(self, /, *args, **kwargs)`

Raised if building the index fails.

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `build_index_main() -> int`

Build an index.json summarizing exported GeoJSONs.

Returns:
    0 if successful, 1 on failure.

### `compute_bbox(geojson_path: pathlib.Path) -> list[float] | None`

Compute bounding box [minx, miny, maxx, maxy] for a GeoJSON file.

Returns:
    List of four floats, or None if read fails.

### `compute_feature_count(geojson_path: pathlib.Path) -> int | None`

Count number of features in a GeoJSON file.

Returns:
    Integer feature count, or None if read fails.

### `get_data_out_dir() -> pathlib.Path`

Return the root data-out directory for processed GeoJSON and chunked outputs.

### `main() -> int`

CLI entry point for index.

### `write_manifest(out_dir: pathlib.Path, layer_config: dict, index_data: list[dict], manifest_filename: str = 'manifest.json', days_back: int | None = None) -> None`

Writes a manifest JSON file summarizing a data export.

Args:
    out_dir (Path): Root data output folder.
    layer_config (dict): Config dictionary for the layer.
    index_data (list[dict]): The index entries with paths and metadata.
    manifest_filename (str): Filename for the manifest (default "manifest.json").
    days_back (int | None): Optional number of days back for a date range.

