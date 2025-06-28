import sys

from civic_lib_core import log_utils
from civic_lib_geo.cli.chunk_geojson import apply_to_geojson_folder, chunk_one

from civic_data_boundaries_us_cd118.export_cd118 import export_cd118
from civic_data_boundaries_us_cd118.utils.config_utils import load_layer_config
from civic_data_boundaries_us_cd118.utils.get_paths import get_data_out_dir

logger = log_utils.logger


def chunk_layers():
    """
    Chunk all exported geojsons in data-out/, based on YAML configs.
    Handles both split-by-state folders and single nationwide layers.
    """
    cfg = load_layer_config("cd118")

    chunk_max_features = cfg.get("chunk_max_features", 500)
    simplify_tolerance = cfg.get("simplify_tolerance", 0.01)

    logger.info("[CHUNKING] Loaded config:")
    logger.info(f"  chunk_max_features: {chunk_max_features}")
    logger.info(f"  simplify_tolerance: {simplify_tolerance}")

    out_dir = get_data_out_dir()
    layer_output_dir = out_dir / cfg.get("output_dir", "cd118")

    if not layer_output_dir.exists():
        logger.info(f"Skipping non-existing output dir: {layer_output_dir}")
        return

    if cfg.get("split_by") == "fips" or cfg.get("split_by") == "state":
        # Process each subfolder (e.g. minnesota, oregon)
        for subfolder in layer_output_dir.iterdir():
            if subfolder.is_dir():
                logger.info(f"Chunking per state: {subfolder}")
                apply_to_geojson_folder(
                    subfolder,
                    action_fn=chunk_one,
                    max_features=chunk_max_features,
                    suffix="_chunked.geojson",
                    tolerance=simplify_tolerance,
                )
    else:
        # Process the layer's main folder directly
        logger.info(f"Chunking layer: {layer_output_dir}")
        apply_to_geojson_folder(
            layer_output_dir,
            action_fn=chunk_one,
            max_features=chunk_max_features,
            suffix="_chunked.geojson",
            tolerance=simplify_tolerance,
        )


def main() -> int:
    """
    Export and chunk TIGER data for layers:
    - CD118
    - Chunking output geojsons

    Returns:
        int: 0 on success, 1 on error
    """
    try:
        logger.info("Starting TIGER export process...")

        out_dir = get_data_out_dir()
        out_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Data output directory: {out_dir}")

        # Export congressional districts
        logger.info("Exporting CD118 boundaries...")
        export_cd118()

        # Chunk geojsons
        logger.info("Starting chunking process...")
        chunk_layers()

        logger.info("Export and chunking complete.")
        return 0

    except Exception as e:
        logger.error(f"Export failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
