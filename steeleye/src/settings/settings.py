"""
Store every config.
"""

ESMA_URL = (
    "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select"
    "?q=*&fq=publication_date:[2021-01-17T00:00:00Z TO 2021-01-19T23:59:59Z]"
    "&wt=xml&indent=true&start=0&rows=100"
)