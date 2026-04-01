"""
Entry point to test XML download.
"""

import logging

from src.services.downloader import Downloader
from src.settings.settings import ESMA_URL


def setup_logging() -> None:
    """Configure basic logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main() -> None:
    """Run a simple test download."""
    setup_logging()
    logger = logging.getLogger(__name__)

    downloader = Downloader()

    try:
        xml_content = downloader.fetch_xml(ESMA_URL)

        logger.info(f"XML downloaded successfully:\n{xml_content[:500]}")

    except Exception:
        logger.exception("Something went wrong")


if __name__ == "__main__":
    main()