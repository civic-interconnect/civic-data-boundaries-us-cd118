"""
cli.py

Command-line interface (CLI) for civic-data-boundaries-us.

Provides commands for:
- Fetching TIGER/Line shapefiles
- Exporting and chunking all GeoJSON files
- Generating spatial indexes and summaries

Run `civic-usa --help` for usage.
"""

import sys

import typer
from civic_lib_core import log_utils

from civic_data_boundaries_us_cd118 import cleanup, export, fetch, index

logger = log_utils.logger

app = typer.Typer(help="Civic USA CD118 CLI — TIGER-based boundary export and indexing")


@app.command("fetch")
def fetch_command():
    """
    Download required TIGER shapefiles (CD118) into data-in/.
    Skips download if files already exist.
    """
    fetch.main()


@app.command("export")
def export_command():
    """
    Export and chunk all data from TIGER into app-ready GeoJSON in data-out/.
    Includes CD118 layers.
    """
    export.main()


@app.command("index")
def index_command():
    """
    Generate index.json and other summary metadata files in data-out/.
    """
    index.main()


@app.command("cleanup")
def cleanup_command():
    """
    Cleanup temporary files and directories created during export.
    Deletes all .zip files and extracted shapefiles from data-in/.
    """
    cleanup.main()


def main() -> int:
    try:
        app()
        return 0
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
