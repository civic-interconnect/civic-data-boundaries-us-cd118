"""Handles downloading and extracting TIGER/Line shapefiles for civic-data-boundaries-us-cd118.

File: fetch.py

This script:
- Loads YAML config files describing layers to download
- Downloads TIGER/Line zip files
- Extracts shapefiles into appropriate directories
"""

from pathlib import Path
from typing import NotRequired, TypedDict, cast

from civic_lib_core import log_utils
from civic_lib_geo.us_constants import (  # pyright: ignore[reportMissingTypeStubs]
    US_STATE_ABBR_TO_FIPS,  # pyright: ignore[reportMissingTypeStubs]
)
import requests

from civic_data_boundaries_us_cd118.utils.config_utils import load_layer_config
from civic_data_boundaries_us_cd118.utils.get_paths import get_data_in_dir

logger = log_utils.logger


class LayerConfig(TypedDict, total=False):
    # Common
    output_dir: str  # required by your logic
    nationwide: NotRequired[bool]

    # Nationwide
    url: NotRequired[str]

    # Per-FIPS
    fips_start: NotRequired[int | str]
    fips_end: NotRequired[int | str]
    filename_pattern: NotRequired[str]  # e.g. "tl_2022_{fips}_cd118.zip"
    base_url: NotRequired[str]  # e.g. "https://..."


def download_file(url: str, dest_path: Path) -> Path:
    """Download a file from a URL to a destination path.

    Returns:
        Path to the downloaded file.

    Raises:
        FetchError if the download fails.
    """
    logger.debug(f"Preparing to download file from URL: {url}")
    logger.debug(f"Destination path: {dest_path}")

    if dest_path.exists():
        logger.info(f"Skipping download. File already exists: {dest_path}")
        return dest_path

    logger.info(f"Downloading: {url}")

    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        with dest_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info(f"Downloaded file saved to: {dest_path}")
        return dest_path

    except Exception as e:
        raise FetchError(f"Failed to download {url}. Error: {e}") from e


def extract_zip(zip_path: Path, extract_to: Path) -> None:
    """Extract a ZIP file into a target folder.

    Raises:
        FileNotFoundError if zip file is missing.
        FetchError if extraction fails.
    """
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file does not exist: {zip_path}")

    if extract_to.exists():
        logger.info(f"Skipping extraction. Folder already exists: {extract_to}")


class FetchError(RuntimeError):
    """Raised when a download/extract operation fails."""


def process_layer(layer: LayerConfig) -> None:
    """Process a single layer from YAML config (create folders, download, extract)."""
    logger.debug(f"Processing layer config: {layer}")

    if "output_dir" not in layer:
        raise FetchError(f"Missing required key 'output_dir' in layer config: {layer}")

    data_in_root = get_data_in_dir()
    output_dir = data_in_root / layer["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory ensured: {output_dir}")

    if layer.get("nationwide"):
        # Nationwide single file
        url = layer.get("url")
        if not url:
            raise FetchError(f"Missing 'url' for nationwide layer: {layer}")

        filename = Path(url).name
        zip_path = output_dir / filename
        extract_path = output_dir / filename.replace(".zip", "")

        downloaded = download_file(url, zip_path)
        extract_zip(downloaded, extract_path)
        return

    # Per-FIPS state-level layers
    for key in ("fips_start", "fips_end", "filename_pattern", "base_url"):
        if key not in layer:
            raise FetchError(f"Missing required key '{key}' in per-FIPS layer config: {layer}")

    fips_start = layer.get("fips_start")
    fips_end = layer.get("fips_end")
    if fips_start is None or fips_end is None:
        raise FetchError(f"Missing fips_start or fips_end in layer config: {layer}")

    start = int(fips_start)  # YAML may give str; normalize
    end = int(fips_end) + 1

    valid_fips: set[str] = set(US_STATE_ABBR_TO_FIPS.values())

    filename_pattern: str = layer["filename_pattern"]  # type: ignore[typeddict-item]
    base_url: str = layer["base_url"]  # type: ignore[typeddict-item]

    for fips in range(start, end):
        fips_code = f"{fips:02d}"
        if fips_code not in valid_fips:
            logger.warning(
                f"Skipping invalid FIPS {fips_code} — no such state exists in TIGER data."
            )
            continue

        filename = filename_pattern.format(fips=fips_code)
        url = f"{base_url}/{filename}"

        state_dir = output_dir / fips_code
        state_dir.mkdir(parents=True, exist_ok=True)

        zip_path = state_dir / filename
        extract_path = state_dir / Path(filename).stem

        logger.info(f"Processing FIPS {fips_code} from {url}")
        downloaded = download_file(url, zip_path)
        extract_zip(downloaded, extract_path)


def main() -> int:
    """Fetch all layers defined in YAML configs.

    Returns:
        0 if successful, 1 otherwise.
    """
    logger.info("Starting TIGER download process...")

    # Load all layer configurations
    layers = ["cd118", "cd118_national"]

    for layer_name in layers:
        layer_config = load_layer_config(layer_name)
        if not layer_config:
            logger.warning(f"No configuration found for layer: {layer_name}")
            continue

        # Skip layers without download URLs (locally generated layers)
        if not layer_config.get("url") and not layer_config.get("base_url"):
            logger.info(f"Skipping {layer_name} - no download URL (locally generated layer)")
            continue

        process_layer(cast("LayerConfig", layer_config))
    logger.info("All TIGER layers fetched and extracted successfully.")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())


__all__ = [
    "download_file",
    "extract_zip",
    "process_layer",
    "main",
]
