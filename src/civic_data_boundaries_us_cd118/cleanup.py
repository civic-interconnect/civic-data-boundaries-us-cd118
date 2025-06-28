import shutil
import sys
from pathlib import Path

from civic_lib_core import log_utils

logger = log_utils.logger

# All known shapefile extensions
SHAPEFILE_EXTENSIONS = {".shp", ".shx", ".dbf", ".prj", ".cpg"}


def clean_data_in_dir(data_in_dir: Path):
    """
    Delete all .zip files and entire shapefile sets from data-in/,
    including loose shapefiles and extracted folders.

    Keeps chunked GeoJSONs safe in data-out.
    """
    if not data_in_dir.exists():
        logger.info(f"No cleanup needed. Folder does not exist: {data_in_dir}")
        return

    deleted_files = 0
    deleted_dirs = 0
    deleted_sets = 0

    # Track which shapefile base names we've already deleted
    shapefile_bases_deleted = set()

    for path in data_in_dir.rglob("*"):
        # Delete .zip files
        if path.is_file() and path.suffix == ".zip":
            path.unlink()
            logger.info(f"Deleted zip file: {path}")
            deleted_files += 1

        # Delete entire shapefile sets for any .shp file found
        elif path.is_file() and path.suffix.lower() == ".shp":
            base = path.with_suffix("")
            if base in shapefile_bases_deleted:
                continue

            # Gather all extensions belonging to this shapefile set
            for ext in SHAPEFILE_EXTENSIONS:
                file_path = base.with_suffix(ext)
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"Deleted shapefile component: {file_path}")
                    deleted_files += 1

            shapefile_bases_deleted.add(base)
            deleted_sets += 1

        # Delete folders that contain any shapefiles
        elif path.is_dir():
            if any(p.suffix.lower() in SHAPEFILE_EXTENSIONS for p in path.rglob("*")):
                shutil.rmtree(path)
                logger.info(f"Deleted shapefile folder: {path}")
                deleted_dirs += 1

    logger.info(
        f"Cleanup complete. Deleted {deleted_files} file(s), {deleted_dirs} folder(s), "
        f"and {deleted_sets} shapefile set(s)."
    )


def main() -> int:
    try:
        from civic_data_boundaries_us_cd118.utils.get_paths import get_data_in_dir

        data_in = get_data_in_dir()
        clean_data_in_dir(data_in)
        return 0
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
