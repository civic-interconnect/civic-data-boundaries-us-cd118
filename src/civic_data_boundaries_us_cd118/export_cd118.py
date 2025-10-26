"""Exports CD118 boundaries from TIGER shapefiles to GeoJSON.

Produces one GeoJSON file per state and writes a manifest YAML.

File: export_cd118.py
"""

from pathlib import Path
import sys
from typing import cast

from civic_lib_core import log_utils
from civic_lib_core.date_utils import today_utc_str
from civic_lib_core.yaml_utils import read_yaml, write_yaml
from civic_lib_geo.us_constants import US_STATE_FIPS_TO_ABBR, get_state_dir_name  # type: ignore
import geopandas as gpd  # type: ignore
import pandas as pd  # type: ignore

from civic_data_boundaries_us_cd118.utils.config_utils import load_layer_config
from civic_data_boundaries_us_cd118.utils.get_paths import (
    get_national_out_dir,
    get_states_out_dir,
    get_tiger_in_dir,
)

logger = log_utils.logger


def validate_columns(gdf: gpd.GeoDataFrame, columns: list[str], label: str):
    """Validate that a GeoDataFrame contains all required columns.

    Args:
        gdf (gpd.GeoDataFrame): The GeoDataFrame to validate.
        columns (list[str]): List of column names that must be present in the GeoDataFrame.
        label (str): A descriptive label for the GeoDataFrame, used in error messages.

    Raises:
        ValueError: If any of the required columns are missing from the GeoDataFrame.
            The error message includes the label and lists all missing columns.

    Example:
        >>> import geopandas as gpd
        >>> gdf = gpd.GeoDataFrame({'name': ['A'], 'geometry': [None]})
        >>> validate_columns(gdf, ['name', 'id'], 'Districts data')
        ValueError: Districts data is missing columns: ['id']
    """
    missing = [col for col in columns if col not in gdf.columns]
    if missing:
        raise ValueError(f"{label} is missing columns: {missing}")


def load_cd118_layer(shp_path: Path) -> gpd.GeoDataFrame:
    """Load a single CD118 shapefile."""
    gdf = gpd.read_file(shp_path)
    validate_columns(gdf, ["CD118FP"], label=shp_path.name)
    return gdf


def export_cd118():
    """Export CD118 boundaries.

    - a nationwide GeoJSON
    - one GeoJSON per state
    """
    logger.info("Starting CD118 export...")
    cd118_dir = get_tiger_in_dir()
    logger.debug(f"Data output directory: {cd118_dir}")
    national_dir = get_national_out_dir()
    logger.debug(f"national_dir: {national_dir}")
    national_dir.mkdir(parents=True, exist_ok=True)

    cfg = load_layer_config("cd118")
    cfg_national = load_layer_config("cd118_national")
    if not cfg or not cfg_national:
        logger.error("Failed to load CD118 configuration.")
        return
    logger.debug(f"CD118 config: {cfg}")
    logger.debug(f"CD118 national config: {cfg_national}")

    # Load configuration settings
    simplify_tolerance = cfg.get("simplify_tolerance")
    drop_columns = cfg.get("drop_columns", [])

    logger.info("[CD118 EXPORT] Settings loaded from config:")
    logger.info(f"  simplify_tolerance: {simplify_tolerance}")
    logger.info(f"  drop_columns: {drop_columns}")

    nationwide_gdfs: list[gpd.GeoDataFrame] = []
    manifest_entries: list[dict[str, str | int]] = []

    for shp_file in cd118_dir.glob("**/*.shp"):
        logger.debug(f"shp_file: {shp_file}")
        parts = shp_file.stem.split("_")
        if len(parts) < 3:
            logger.warning(f"Unexpected CD118 filename: {shp_file.name}")
            continue

        state_fips = parts[2]

        # Skip invalid FIPS codes
        state_abbr = US_STATE_FIPS_TO_ABBR.get(state_fips)
        if not state_abbr:
            logger.warning(f"Unknown FIPS code: {state_fips} in {shp_file.name}")
            continue

        state_name = get_state_dir_name(state_abbr)
        logger.debug(f"Processing CD118 shapefile for {state_name}: {shp_file.name}")

        gdf = load_cd118_layer(shp_file)

        # Drop columns dynamically
        if drop_columns:
            drop_existing = [c for c in drop_columns if c in gdf.columns]
            if drop_existing:
                gdf = gdf.drop(columns=drop_existing)
                logger.debug(f"[CD118 EXPORT] Dropped columns: {drop_existing}")
            else:
                logger.debug(f"[CD118 EXPORT] None of the drop_columns exist in {shp_file.name}")

        # Simplify dynamically
        if simplify_tolerance:
            gdf["geometry"] = gdf.geometry.simplify(simplify_tolerance, preserve_topology=True)

        nationwide_gdfs.append(cast("gpd.GeoDataFrame", gdf))

        state_out_dir = get_states_out_dir() / state_name
        state_out_dir.mkdir(parents=True, exist_ok=True)

        state_out_path = state_out_dir / f"cd118_{state_name}.geojson"
        gdf.to_file(state_out_path, driver="GeoJSON")

        logger.info(f"Exported CD118 GeoJSON for {state_name}: {state_out_path}")

        manifest_entries.append(
            {
                "state_name": state_name,
                "state_fips": state_fips,
                "geojson_path": str(state_out_path.relative_to(cd118_dir.parent.parent)),
                "feature_count": len(gdf),
            }
        )

    # Export nationwide GeoJSON
    if nationwide_gdfs:
        combined_df = pd.concat(nationwide_gdfs, ignore_index=True)

        combined_gdf = gpd.GeoDataFrame(
            combined_df,
            geometry="geometry",
            crs=nationwide_gdfs[0].crs if nationwide_gdfs else None,
        )
        nationwide_filename = cfg.get("filename", "cd118_us.geojson")
        nationwide_path = national_dir / nationwide_filename
        combined_gdf.to_file(nationwide_path, driver="GeoJSON")  # type: ignore
        logger.info(f"[CD118 EXPORT] Nationwide file written to: {nationwide_path}")
        logger.info(
            f"[CD118 EXPORT] Nationwide file size: {nationwide_path.stat().st_size / 1e6:.2f} MB"
        )
        logger.info(f"[CD118 EXPORT] Nationwide feature count: {len(combined_gdf)}")

    else:
        logger.warning("No CD118 data found to export for nationwide layer.")

    # Write manifest
    manifest_path = national_dir / "manifest.yaml"
    manifest = read_yaml(manifest_path) if manifest_path.exists() else {}

    total_features = sum((e["feature_count"] for e in manifest_entries), 0)

    manifest.update(
        {
            "layer": "cd118",
            "description": "US 118th Congressional District boundaries from TIGER/Line 2022",
            "source": "US Census TIGER/Line 2022",
            "last_updated": today_utc_str(),
            "total_states": len(manifest_entries),
            "total_features": total_features,
            "states": manifest_entries,
        }
    )

    write_yaml(manifest, manifest_path)
    logger.info(f"Manifest written to {manifest_path}")


def main() -> int:
    """Run CD118 export.

    Returns:
        int: 0 if successful, 1 on error.
    """
    try:
        export_cd118()
        logger.info("CD118 export complete.")
        return 0
    except Exception as e:
        logger.error(f"CD118 export failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
