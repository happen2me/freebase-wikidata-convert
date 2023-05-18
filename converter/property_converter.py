"""
Property converter converts between Freebase and Wikidata properties.
"""
import logging
import requests

from bs4 import BeautifulSoup

class PropertyConverter:
    """Convert Freebase property to Wikidata property and vice versa. The data are scraped from
    https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase/Mapping
    """
    def __init__(self, url="https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase/Mapping"):
        """Create a property converter

        Args:
            url (str, optional): The mapping page from Freebase properties to Wikidata properties.
                Defaults to "https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase/Mapping".
        """
        self.url = url
        self.freebase2wikidata = {}
        self.wikidata2freebase = {}
        self.update_mapping()

    def get_wikidata_property(self, freebase_property):
        """Get the wikidata property from freebase property

        Args:
            freebase_property (str): The freebase property, e.g. /organization/organization/child

        Returns:
            str | None: wikidata property identifier, e.g. P355
                If the freebase property is not mapped, return None
        """
        return self.freebase2wikidata.get(freebase_property, None)

    def get_freebase_property(self, wikidata_property):
        """Get the freebase property from wikidata property

        Args:
            wikidata_property (str): The wikidata property, e.g. P355

        Returns:
            str | None: freebase property identifier, e.g. /organization/organization/child
                If the wikidata property is not mapped, return None
        """
        return self.wikidata2freebase.get(wikidata_property, None)

    def update_mapping(self):
        """Update the mapping from freebase property to wikidata property
        by crawling https://www.wikidata.org/wiki/Wikidata:WikiProject_Freebase/Mapping
        """
        response = requests.get(self.url, timeout=60)
        html_doc = response.text
        soup = BeautifulSoup(html_doc)
        freebase2wikidata = {}
        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            try:
                freebase_url = cols[0].a.attrs["href"]
            except AttributeError:
                continue
            except IndexError:
                continue
            if 'www.freebase.com' not in freebase_url:
                continue
            try:
                wikidata_url = cols[1].a.attrs["href"]
            except AttributeError:
                wikidata_url = None
            freebase2wikidata[freebase_url] = wikidata_url

        logging.info("# exsit mapping: %d", len(freebase2wikidata))
        logging.info("# not none mapping: %d", len([x for x in freebase2wikidata.values()
                                                    if x is not None]))
        logging.info("# wikidata properties mapped: %d", len(set(freebase2wikidata.values())))

        freebase2wikidata = {k.split('https://www.freebase.com')[-1]: v.split('/wiki/Property:')[-1]
                             if v is not None else v
                             for k, v in freebase2wikidata.items()}
        wikidata2freebase = {v: k for k, v in freebase2wikidata.items() if v is not None}
        self.freebase2wikidata = freebase2wikidata
        self.wikidata2freebase = wikidata2freebase
