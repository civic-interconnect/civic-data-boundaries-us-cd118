# Module `civic_data_boundaries_us_cd118.cleanup`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

## Functions

### `clean_data_in_dir(data_in_dir: pathlib.Path)`

Delete all .zip files and entire shapefile sets from data-in/,
including loose shapefiles and extracted folders.

Keeps chunked GeoJSONs safe in data-out.

### `main() -> int`

No description available.

