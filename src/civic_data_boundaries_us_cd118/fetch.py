"""
fetch.py

Handles downloading and extracting TIGER/Line shapefiles
for civic-data-boundaries-us-cd118.

This script:
- Loads YAML config files describing layers to download
- Downloads TIGER/Line zip files
- Extracts shapefiles into appropriate directories
"""

import zipfile
from pathlib import Path

import requests
import yaml
from civic_lib_core import log_utils
from civic_lib_geo.us_constants import US_STATE_ABBR_TO_FIPS

from civic_data_boundaries_us_cd118.utils.get_paths import get_data_in_dir, get_repo_root

__all__ = [
    "download_file",
    "extract_zip",
    "process_layer",
    "main",
]


logger = log_utils.logger


class FetchError(Exception):
    """Custom exception for TIGER fetch errors."""


def download_file(url: str, dest_path: Path) -> Path:
    """
    Download a file from a URL to a destination path.

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

        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info(f"Downloaded file saved to: {dest_path}")
        return dest_path

    except Exception as e:
        raise FetchError(f"Failed to download {url}. Error: {e}") from e


def extract_zip(zip_path: Path, extract_to: Path) -> None:
    """
    Extracts a ZIP file into a target folder.

    Raises:
        FileNotFoundError if zip file is missing.
        FetchError if extraction fails.
    """
    if not zip_path.exists():
        raise FileNotFoundError(f"Zip file does not exist: {zip_path}")

    if extract_to.exists():
        logger.info(f"Skipping extraction. Folder already exists: {extract_to}")
        return

    logger.info(f"Extracting {zip_path} to {extract_to}")

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info(f"Extraction complete: {extract_to}")
    except Exception as e:
        raise FetchError(f"Failed to extract {zip_path}. Error: {e}") from e


def process_layer(layer: dict) -> None:
    """
    Process a single layer from YAML config:
    - create folders
    - download zip files
    - extract them
    """
    logger.debug(f"Processing layer config: {layer}")

    if "output_dir" not in layer:
        raise FetchError(f"Missing required key 'output_dir' in layer config: {layer}")

    data_in_root = get_data_in_dir()
    output_dir = data_in_root / layer["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory ensured: {output_dir}")

    if layer.get("nationwide"):
        # Nationwide single file
        if "url" not in layer:
            raise FetchError(f"Missing 'url' for nationwide layer: {layer}")

        url = layer["url"]
        filename = Path(url).name
        zip_path = output_dir / filename
        extract_path = output_dir / filename.replace(".zip", "")

        downloaded = download_file(url, zip_path)
        extract_zip(downloaded, extract_path)

    else:
        # Per-FIPS state-level layers
        required_fips_keys = ["fips_start", "fips_end", "filename_pattern", "base_url"]
        for key in required_fips_keys:
            if key not in layer:
                raise FetchError(f"Missing required key '{key}' in per-FIPS layer config: {layer}")

        start = int(layer["fips_start"])
        end = int(layer["fips_end"]) + 1

        valid_fips = set(US_STATE_ABBR_TO_FIPS.values())

        for fips in range(start, end):
            fips_code = f"{fips:02d}"
            if fips_code not in valid_fips:
                logger.warning(
                    f"Skipping invalid FIPS {fips_code} — no such state exists in TIGER data."
                )
                continue

            filename = layer["filename_pattern"].format(fips=fips_code)
            url = f"{layer['base_url']}/{filename}"

            state_dir = output_dir / fips_code
            state_dir.mkdir(parents=True, exist_ok=True)

            zip_path = state_dir / filename
            extract_path = state_dir / filename.replace(".zip", "")

            logger.info(f"Processing FIPS {fips_code} from {url}")

            downloaded = download_file(url, zip_path)
            extract_zip(downloaded, extract_path)


def main() -> int:
    """
    Main entrypoint for fetching all layers defined in YAML configs.

    Returns:
        0 if successful, 1 otherwise.
    """
    try:
        logger.info("Starting TIGER download process...")
        yaml_dir = get_repo_root() / "data-config"

        if not yaml_dir.exists():
            raise FetchError(f"Config directory does not exist: {yaml_dir}")

        yaml_files = list(yaml_dir.glob("*.yaml"))
        if not yaml_files:
            raise FetchError(f"No YAML configs found in: {yaml_dir}")

        logger.info(f"Found {len(yaml_files)} YAML config file(s) in: {yaml_dir}")

        for yaml_file in yaml_files:
            logger.info(f"Processing config file: {yaml_file.name}")

            with yaml_file.open("r", encoding="utf-8") as f:
                try:
                    config = yaml.safe_load(f)
                except Exception as e:
                    raise FetchError(f"Error parsing YAML file {yaml_file}: {e}") from e

                if not config or "layers" not in config:
                    raise FetchError(f"YAML config file is empty or missing 'layers': {yaml_file}")

                for layer in config["layers"]:
                    process_layer(layer)

        logger.info("All TIGER layers fetched and extracted successfully.")
        return 0

    except FetchError as e:
        logger.error(f"Fetch process failed: {e}")
        return 1

    except Exception as e:
        logger.error(f"Unexpected error during fetch process: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
