"""Generates index.json and summary metadata in data-out/.

File: index.py

Used by civic-usa-cd118 CLI:
    civic-usa-cd118 index

Currently builds:
- index.json with bounding boxes
- manifest.json with dataset summary
"""

import json
from pathlib import Path
from typing import Any

from civic_lib_core import date_utils, log_utils
import geopandas as gpd

from civic_data_boundaries_us_cd118.utils.get_paths import get_data_out_dir

logger = log_utils.logger


class IndexBuildError(Exception):
    """Raised if building the index fails."""


def compute_bbox(geojson_path: Path) -> list[float] | None:
    """Compute bounding box [minx, miny, maxx, maxy] for a GeoJSON file.

    Returns:
        List of four floats, or None if read fails.
    """
    try:
        gdf: gpd.GeoDataFrame = gpd.read_file(geojson_path)
        bounds = gdf.total_bounds
        return [round(x, 6) for x in bounds]
    except Exception as e:
        logger.warning(f"Could not read {geojson_path.name}: {e}")
        return None


def compute_feature_count(geojson_path: Path) -> int | None:
    """Count number of features in a GeoJSON file.

    Returns:
        Integer feature count, or None if read fails.
    """
    try:
        gdf: gpd.GeoDataFrame = gpd.read_file(geojson_path)
        return len(gdf)
    except Exception as e:
        logger.warning(f"Could not read {geojson_path.name} to count features: {e}")
        return None


def write_manifest(
    out_dir: Path,
    layer_config: dict[str, Any],
    index_data: list[dict[str, Any]],
    manifest_filename: str = "manifest.json",
    days_back: int | None = None,
) -> None:
    """Write a manifest file containing metadata about a geospatial dataset.

    Args:
        out_dir (Path): The output directory where the manifest file will be written.
        layer_config (dict): Configuration dictionary containing dataset metadata such as
            name, description, year, source, license, geometry_type, and nationwide flag.
        index_data (list[dict]): List of dictionaries containing information about indexed
            files, where each entry should have a "path" key and optionally a "features" key.
        manifest_filename (str, optional): Name of the manifest file to create.
            Defaults to "manifest.json".
        days_back (int | None, optional): Number of days back to include in date range.
            If None, no date range is included. Defaults to None.

    Returns:
        None

    Raises:
        IOError: If the manifest file cannot be written to the specified path.

    Note:
        The function creates a JSON manifest file containing dataset metadata, file counts,
        feature counts, file paths, generation timestamp, and optional date range information.
    """
    total_files = len(index_data)
    total_features = sum(
        entry["features"] for entry in index_data if entry.get("features") is not None
    )

    # Compute optional date range
    date_range_list = None
    if days_back is not None:
        date_range_list = date_utils.date_range(days_back)

    manifest: dict[str, Any] = {
        "dataset": layer_config.get("name"),
        "description": layer_config.get("description"),
        "year": layer_config.get("year"),
        "source": layer_config.get("source"),
        "license": layer_config.get("license"),
        "geometry_type": layer_config.get("geometry_type"),
        "nationwide": layer_config.get("nationwide"),
        "total_files": total_files,
        "total_features": total_features,
        "files_indexed": [entry["path"] for entry in index_data],
        "generated_at": date_utils.now_utc_str(),
        "date_range": date_range_list,
    }

    manifest_path = out_dir / manifest_filename
    with Path.open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    logger.info(f"Manifest written to {manifest_path}")


def build_index_main() -> int:
    """Build an index.json summarizing exported GeoJSONs.

    Returns:
        0 if successful, 1 on failure.
    """
    try:
        out_dir = get_data_out_dir()
        index: list[dict[str, Any]] = []

        logger.info(f"Scanning {out_dir} for GeoJSONs...")

        for geojson in out_dir.rglob("*.geojson"):
            logger.debug(f"Processing {geojson}")
            bbox = compute_bbox(geojson)
            feature_count = compute_feature_count(geojson)

            index_entry: dict[str, Any] = {
                "path": str(geojson.relative_to(out_dir)),
                "bbox": bbox,
                "features": feature_count,
            }
            index.append(index_entry)

        # Save index.json
        index_file = out_dir / "index.json"
        with Path.open(index_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

        logger.info(f"index.json written to {index_file}")
        logger.info(f"{len(index)} GeoJSONs indexed.")

        # Dummy layer config (for standalone runs)
        dummy_layer_config: dict[str, Any] = {
            "name": "cd118",
            "description": "US 118th Congressional District boundaries from TIGER/Line 2022",
            "year": 2022,
            "source": "US Census Bureau TIGER/Line",
            "license": "Public domain",
            "geometry_type": "Polygon",
            "nationwide": False,
        }

        # Save manifest
        write_manifest(
            out_dir=out_dir,
            layer_config=dummy_layer_config,
            index_data=index,
            days_back=7,
        )

        return 0

    except Exception as e:
        logger.error(f"Index build failed: {e}")
        return 1


def main() -> int:
    """CLI entry point for index."""
    try:
        return build_index_main()
    except Exception as e:
        logger.error(f"Index command failed unexpectedly: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
