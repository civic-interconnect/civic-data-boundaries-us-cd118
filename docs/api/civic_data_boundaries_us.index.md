# Module `civic_data_boundaries_us.index`

## Classes

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

### `compute_bbox(geojson_path: pathlib.Path) -> list[float] | None`

Compute bounding box [minx, miny, maxx, maxy] for a GeoJSON file.

Returns:
    list[float] | None: Bounding box or None if read fails.

### `get_data_out_dir() -> pathlib.Path`

Return the root data-out directory for processed GeoJSON and chunked outputs.

### `main() -> int`

CLI entry point for index.
