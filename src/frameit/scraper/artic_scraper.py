from .listing import Listing
from .scraper import Scraper


class ARTICScraper(Scraper):
    _ARTIST_LINK_ATTR = "data-gtm-0-artist"
    _TITLE_LINK_ATTR = "data-gtm-1-event"
    _DOWNLOAD_URL_BUTTON_ATTR = "data-gallery-img-download-url"
    _LISTING_CLASS = "m-listing"
    _LISTING_LINK_CLASS = "m-listing__link"
    _LISTINGS_URL = (
        "https://www.artic.edu/collection?is_public_domain=1&has_multimedia=1"
    )
    _PAGINATOR_CLASS = "m-paginator__pages"

    def _get_listing(self, listing):
        listing_link = listing.find("a", class_=self._LISTING_LINK_CLASS)
        artist = listing_link.get(self._ARTIST_LINK_ATTR)
        title = listing_link.get(self._TITLE_LINK_ATTR)
        href = listing_link.get("href")
        download_url = None

        if href:
            link_html = self.html(href)
            download_button = link_html.find(
                "button", {self._DOWNLOAD_URL_BUTTON_ATTR: True}
            )
            download_url = (
                download_button.get(self._DOWNLOAD_URL_BUTTON_ATTR)
                if download_button
                else None
            )

        return Listing(artist, title, download_url)

    def listings(self):
        listings_html = self.html(self._LISTINGS_URL)
        listings = listings_html.find_all("li", class_=self._LISTING_CLASS)
        paginator = listings_html.find("ul", class_=self._PAGINATOR_CLASS)
        pages = paginator.find_all("li")
        last_page = int(pages[-1].text) if pages else 1

        for listing in listings:
            yield self._get_listing(listing)

        for page in range(2, last_page + 1):
            listings_html = self.html(f"{self._LISTINGS_URL}&page={page}")
            listings = listings_html.find_all("li", class_=self._LISTING_CLASS)

            for listing in listings:
                yield self._get_listing(listing)
