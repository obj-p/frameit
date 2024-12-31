from abc import ABC, abstractmethod
from collections.abc import Generator
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from frameit.scraper.listing import Listing


class Scraper(ABC):
    @staticmethod
    def html(url: str, markup="html.parser") -> BeautifulSoup:
        req = Request(url)
        resp = urlopen(req).read()
        return BeautifulSoup(resp, markup)

    @abstractmethod
    def listings(self) -> Generator[Listing, None, None]:
        pass
