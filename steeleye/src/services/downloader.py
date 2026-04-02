"""
Simple downloader service to fetch XML content
"""

import logging
import requests


class Downloader:
    """Handles downloading content from URLs"""

    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def fetch_xml(self, url: str) -> str:
        """
        Download XML content from a URL

        Args:
            url (str): The URL to fetch

        Returns:
            str: XML content as string

        Raises:
            requests.RequestException: If request fails
        """
        self.logger.info(f"Downloading XML from {url}")

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            self.logger.info("Download successful")
            return response.text

        except requests.RequestException as e:
            self.logger.error(f"Failed to download XML: {e}")
            raise
    
    def fetch_binary(self, url: str) -> bytes:
        """
        Download binary content (e.g., ZIP file) from a URL

        Args:
            url (str): The URL to fetch

        Returns:
            bytes: Raw response content

        Raises:
            requests.RequestException: If request fails
        """
        self.logger.info(f"Downloading binary from {url}")

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            self.logger.info("Binary download successful")
            return response.content

        except requests.RequestException as e:
            self.logger.error(f"Failed to download binary: {e}")
            raise