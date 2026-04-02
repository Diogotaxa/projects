"""
Parser module for extracting data from ESMA XML
"""

import logging
import zipfile
import io
import xml.etree.ElementTree as ET


class XMLParser:
    """Handles parsing of ESMA XML data"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def extract_dltins_link(self, xml_content: str) -> str:
        """
        Extract the second download link where file_type is 'DLTINS'

        Args:
            xml_content (str): XML content as string

        Returns:
            str: Download URL for the second DLTINS entry

        Raises:
            ValueError: If less than two DLTINS entries are found
        """
        self.logger.info("Parsing XML to find DLTINS links")

        root = ET.fromstring(xml_content)

        dltins_links = []

        for doc in root.iter("doc"):
            file_type = None
            download_link = None

            for field in doc.findall("str"):
                name = field.attrib.get("name")

                if name == "file_type":
                    file_type = field.text

                elif name == "download_link":
                    download_link = field.text

            if file_type == "DLTINS" and download_link:
                dltins_links.append(download_link)

        if len(dltins_links) < 2:
            self.logger.error("Less than 2 DLTINS links found")
            raise ValueError("Not enough DLTINS links found")

        selected_link = dltins_links[1]  # second item (index 1)

        self.logger.info(f"Selected DLTINS link: {selected_link}")

        return selected_link
    
    def extract_xml_from_zip(self, zip_bytes: bytes) -> str:
        """
        Extract the XML file content from a ZIP archive

        Args:
            zip_bytes (bytes): ZIP file content as bytes

        Returns:
            str: Extracted XML content as string

        Raises:
            ValueError: If no XML file is found in the ZIP
        """
        self.logger.info("Extracting XML from ZIP")

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            file_list = z.namelist()

            self.logger.debug(f"Files in ZIP: {file_list}")

            # Find first XML file
            xml_files = [f for f in file_list if f.endswith(".xml")]

            if not xml_files:
                self.logger.error("No XML file found in ZIP")
                raise ValueError("No XML file found in ZIP")

            xml_filename = xml_files[0]
            self.logger.info(f"Extracting file: {xml_filename}")

            with z.open(xml_filename) as xml_file:
                xml_content = xml_file.read().decode("utf-8")

        return xml_content


    def parse_instruments(self, xml_content: str) -> list[dict]:
        """
        Parse the inner XML and extract required fields

        Args:
            xml_content (str): XML content as string

        Returns:
            list[dict]: List of instrument records
        """
        self.logger.info("Parsing instrument data from XML")

        root = ET.fromstring(xml_content)
        records = []

        for instr in root.findall(".//{*}FinInstrm"):

            record = (
            instr.find("{*}NewRcrd") or
            instr.find("{*}ModfdRcrd") or
            instr.find("{*}TermntdRcrd")
            )

            if record is None:
                continue

            attr = record.find("{*}FinInstrmGnlAttrbts")

            if attr is None:
                continue

            record = {
                "FinInstrmGnlAttrbts.Id": self._get_text(attr, "Id"),
                "FinInstrmGnlAttrbts.FullNm": self._get_text(attr, "FullNm"),
                "FinInstrmGnlAttrbts.ClssfctnTp": self._get_text(attr, "ClssfctnTp"),
                "FinInstrmGnlAttrbts.CmmdtyDerivInd": self._get_text(attr, "CmmdtyDerivInd"),
                "FinInstrmGnlAttrbts.NtnlCcy": self._get_text(attr, "NtnlCcy"),
                "Issr": self._get_text(record, "Issr"),
            }

            records.append(record)

        self.logger.info(f"Parsed {len(records)} records")
        return records

    def _get_text(self, parent, tag: str) -> str:
        element = parent.find(f"{{*}}{tag}")
        return element.text if element is not None else ""