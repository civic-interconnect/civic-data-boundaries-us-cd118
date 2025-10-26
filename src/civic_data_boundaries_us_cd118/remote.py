"""Remote data access for civic-data-boundaries-us-cd118.

File: src/civic_data_boundaries_us_cd118/remote.py
"""

from __future__ import annotations

import json
from typing import Any
from urllib.request import urlopen

BASE = "https://raw.githubusercontent.com/civic-interconnect/civic-data-boundaries-us-cd118/refs/heads/main/data-out"


def load_index() -> list[dict[str, Any]]:
    """Load the index of available congressional district boundaries from a remote JSON file.

    This function fetches the index.json file from the base URL which contains
    metadata about available congressional district boundary files.

    Returns:
        list[dict[str, Any]]: A list of dictionaries containing metadata for each
            available congressional district boundary file. Each dictionary typically
            includes information such as file paths, identifiers, and other relevant
            metadata.

    Raises:
        ValueError: If the constructed URL does not start with 'http:' or 'https:'.
        URLError: If there's an issue accessing the remote URL.
        JSONDecodeError: If the response cannot be parsed as valid JSON.
    """
    url = f"{BASE}/index.json"
    # URL scheme validation to ensure only http/https are allowed
    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'")
    with urlopen(url) as r:  # nosec B310  # noqa: S310
        return json.load(r)


def file_url(rel_path: str) -> str:
    """Generate a complete URL by combining the base URL with a relative path.

    Args:
        rel_path (str): The relative path to append to the base URL. Leading slashes
                       will be automatically stripped to prevent double slashes.

    Returns:
        str: The complete URL formed by concatenating BASE and the cleaned relative path.

    Example:
        >>> file_url("data/boundaries.json")
        "https://example.com/data/boundaries.json"
        >>> file_url("/data/boundaries.json")
        "https://example.com/data/boundaries.json"
    """
    return f"{BASE}/{rel_path.lstrip('/')}"
