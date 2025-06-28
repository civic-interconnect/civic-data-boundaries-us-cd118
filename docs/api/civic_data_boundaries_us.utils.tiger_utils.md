# Module `civic_data_boundaries_us.utils.tiger_utils`

## Functions

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under `src/civic_data_boundaries_us/utils/`.

### `get_tiger_base_url() -> str`

Return the base URL for the TIGER/Line shapefiles for 2022.
This is the URL where the TIGER/Line shapefiles can be downloaded.

### `get_tiger_data_dirs() -> dict`

Return a dictionary of local paths for the TIGER/Line shapefiles for states and counties.
These paths point to where the shapefiles are stored in the local repository.

### `get_tiger_layer_urls() -> dict`

Return a dictionary of URLs for the TIGER/Line shapefiles for states and counties.
The URLs point to the ZIP files containing the shapefiles.
