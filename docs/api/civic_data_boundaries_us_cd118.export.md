# Module `civic_data_boundaries_us_cd118.export`

## Functions

### `apply_to_geojson_folder(folder: pathlib.Path, action_fn: collections.abc.Callable, *, suffix: str = '_processed.geojson', tolerance: float | None = None, max_features: int | None = None)`

Apply an action to every .geojson file in a folder.

Args:
    folder (Path): Path to folder containing .geojson files.
    action_fn (Callable): Function to apply to each file.
    suffix (str): Suffix to add to output filenames.
    tolerance (float | None): Optional tolerance value for simplification.
    max_features (int | None): Optional limit for chunking.

### `chunk_layers()`

Chunk all exported geojsons in data-out/, based on YAML configs.
Handles both split-by-state folders and single nationwide layers.

### `chunk_one(path: pathlib.Path, max_features: int, output_dir: pathlib.Path)`

Chunk a single GeoJSON file and write the output files.

Args:
    path (Path): Path to input GeoJSON file.
    max_features (int): Max features per chunk.
    output_dir (Path): Output folder to store chunks.

### `export_cd118()`

Export CD118 boundaries:
  - a nationwide GeoJSON
  - one GeoJSON per state

### `get_data_out_dir() -> pathlib.Path`

Return the root data-out directory for processed GeoJSON and chunked outputs.

### `load_layer_config(layer_name: str) -> dict`

Load configuration for a given layer, merged with global defaults.

### `main() -> int`

Export and chunk TIGER data for layers:
- CD118
- Chunking output geojsons

Returns:
    int: 0 on success, 1 on error

