# civic-data-boundaries-us-cd118

[![PyPI](https://img.shields.io/pypi/v/civic-data-boundaries-us-cd118.svg)](https://pypi.org/project/civic-data-boundaries-us-cd118/)
[![Python versions](https://img.shields.io/pypi/pyversions/civic-data-boundaries-us-cd118.svg)](https://pypi.org/project/civic-data-boundaries-us-cd118/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![CI Status](https://github.com/civic-interconnect/civic-data-boundaries-us-cd118/actions/workflows/ci.yml/badge.svg)](https://github.com/civic-interconnect/civic-data-boundaries-us-cd118/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue)](https://civic-interconnect.github.io/civic-data-boundaries-us-cd118/)

> U.S. Civic Boundary Data for [Civic Interconnect](https://github.com/civic-interconnect), including boundaries for the 118th U.S. Congressional Districts.

This package provides and hosts standardized U.S. boundary GeoJSON and shapefile-derived layers from TIGER/Line shapefiles, including:
- Boundaries for the 118th Congressional Districts (CD118)
- Support for OCD IDs and simplified formats
- GeoJSON files and manifest indexes for civic data pipelines

GeoJSON files and indexes are generated for use in civic data pipelines.

For state and county boundaries, see [civic-data-boundaries-us](https://github.com/civic-interconnect/civic-data-boundaries-us/).

---

## Installation

```shell
uv add civic-data-boundaries-us-cd118
#or
pip install civic-data-boundaries-us-cd118
```

Or add to `pyproject.toml` dependencies: `"civic-data-boundaries-us-cd118"`

---

## Data

This repository **hosts pre-generated GeoJSON output** in `data-out/` for direct use in apps, agents, and public mapping tools.

| File | Description |
|-------|------------|
| [`index.json`](https://raw.githubusercontent.com/civic-interconnect/civic-data-boundaries-us-cd118/refs/heads/main/data-out/index.json) | List of all available GeoJSON files with bbox & feature counts |
| [`manifest.json`](https://raw.githubusercontent.com/civic-interconnect/civic-data-boundaries-us-cd118/refs/heads/main/data-out/manifest.json) | Dataset metadata (source, license, timestamps, totals) |
| `states/<state>/<file>.geojson` | Per-state boundary files |
| `national/cd118_us.geojson` | Entire U.S. (all congressional districts) |

### Example: Load from Python

```python
import requests
import geopandas as gpd

URL = "https://raw.githubusercontent.com/civic-interconnect/civic-data-boundaries-us-cd118/refs/heads/main/data-out/states/minnesota/cd118_minnesota.geojson"

gdf = gpd.read_file(URL)
print(gdf.head())
```

### Example: Load in JavaScript (Leaflet / MapLibre)

```js
const url = "https://raw.githubusercontent.com/civic-interconnect/civic-data-boundaries-us-cd118/refs/heads/main/data-out/national/cd118_us.geojson";

fetch(url)
  .then(r => r.json())
  .then(data => {
    L.geoJSON(data).addTo(map);
  });
```

---

## Development

See [DEVELOPER.md](./DEVELOPER.md)

## Pipeline

Fetch
- Downloads TIGER zip files
- Skips files already present

Extract
- Unzips shapefiles into folders
- Skips folders already extracted

Export
- Reads shapefiles
- Writes chunked GeoJSON files suitable for GH hosting

Cleanup
- Removes original .zip files and extracted shapefiles once chunked GeoJSONs are complete


## References

- [Census TIGER/Line 2022](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.2022.html)

Direct URLs for the TIGER/Line shapefiles (2022):

- U.S. States: <https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip>
- U.S. Counties: <https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip>
- 118th Congressional Districts: <https://www2.census.gov/geo/tiger/TIGER2022/CD/tl_2022_us_cd118.zip>
