# Module `civic_data_boundaries_us.cli.cli`

## Functions

### `cleanup_command()`

Cleanup temporary files and directories created during export.
Deletes all .zip files and extracted shapefiles from data-in/.

### `export_command()`

Export and chunk all data from TIGER into app-ready GeoJSON in data-out/.
Includes state, county, and CD118 layers.

### `fetch_command()`

Download required TIGER shapefiles (state, county, CD118) into data-in/.
Skips download if files already exist.

### `index_command()`

Generate index.json and other summary metadata files in data-out/.

### `main() -> int`

No description available.
