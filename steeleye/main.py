"""
Entry point to test XML download.
"""

import logging

from src.services.downloader import Downloader
from src.services.parser import XMLParser
from src.services.transformer import DataTransformer
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
    parser = XMLParser()
    transformer = DataTransformer()

    try:
        xml_content = downloader.fetch_xml(ESMA_URL)
        logger.info("XML preview: %s", xml_content[:500])

        link = parser.extract_dltins_link(xml_content)
        logger.info("Dltins_link: %s", link)

        zip_bytes = downloader.fetch_binary(link)
        logger.info("ZIP downloaded successfully")

        inner_xml = parser.extract_xml_from_zip(zip_bytes)
        logger.info("Inner XML extracted successfully")
        with open("data/debug.xml", "w", encoding="utf-8") as f:
            f.write(inner_xml)

        records = parser.parse_instruments(inner_xml)
        df = transformer.to_dataframe(records)
        logger.info("DataFrame shape: %s", df.shape)
        logger.info("First 5 rows:\n%s", df.head())
        df.to_csv("data/output.csv", index=False)
        logger.info("CSV file created successfully")

    except Exception:
        logger.exception("Something went wrong")


if __name__ == "__main__":
    main()