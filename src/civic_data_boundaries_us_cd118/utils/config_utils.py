from pathlib import Path

import yaml
from civic_lib_core import log_utils

logger = log_utils.logger


def load_layer_config(layer_name: str) -> dict:
    """
    Load configuration for a given layer, merged with global defaults.
    """
    yaml_dir = Path(__file__).parent.parent.parent.parent / "data-config"
    logger.debug(f"Looking for YAML configs in {yaml_dir}")

    yaml_files = list(yaml_dir.glob("*.yaml"))
    if not yaml_files:
        logger.warning(f"No YAML config files found in {yaml_dir}")
        return {}
    logger.debug(f"Found YAML config files: {[f.name for f in yaml_files]}")

    for yaml_file in yaml_files:
        with open(yaml_file, encoding="utf-8") as f:
            logger.debug(f"Loading config from {yaml_file.name}")
            # Load the YAML file
            config = yaml.safe_load(f) or {}

            # Check all layers in this file
            for layer in config.get("layers", []):
                if layer.get("name") == layer_name:
                    # Merge global defaults with layer-specific
                    merged = {
                        "simplify_tolerance": layer.get(
                            "simplify_tolerance", config.get("simplify_tolerance")
                        ),
                        "chunk_max_features": layer.get(
                            "chunk_max_features", config.get("chunk_max_features")
                        ),
                        "drop_columns": layer.get("drop_columns", config.get("drop_columns")),
                        # Include all other layer-specific fields too:
                        **layer,
                    }
                    return merged

    # If not found, return empty dict
    return {}
