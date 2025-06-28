# civic-data-boundaries-us-cd118

[![Version](https://img.shields.io/badge/version-v0.0.1-blue)](https://github.com/civic-interconnect/civic-data-boundaries-us-cd118/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/civic-data-boundaries-us-cd118/actions/workflows/tests.yml/badge.svg)](https://github.com/civic-interconnect/civic-data-boundaries-us-cd118/actions)

> U.S. Civic Boundary Data for [Civic Interconnect](https://github.com/civic-interconnect), including boundaries for the 118th U.S. Congressional Districts.

This package provides and hosts standardized U.S. boundary GeoJSON and shapefile-derived layers from TIGER/Line shapefiles, including:
- Boundaries for the 118th Congressional Districts (CD118)
- Support for OCD IDs and simplified formats
- GeoJSON files and manifest indexes for civic data pipelines

GeoJSON files and indexes are generated for use in civic data pipelines.

For state and county boundaries, see [civic-data-boundaries-us](https://github.com/civic-interconnect/civic-data-boundaries-us/).

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
