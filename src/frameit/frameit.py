import os
import time
from urllib.request import urlretrieve

import click

from frameit.scraper import ARTICScraper


@click.command()
def frameit():
    scraper = ARTICScraper()

    for listing in scraper.listings():
        url = listing.url
        if not url:
            continue

        artist = listing.artist or "_unknown_"
        title = listing.title or "_unknown_"
        filename = f"{artist}-{title}.jpg".lower().replace(" ", "_")

        if not os.path.exists(filename):
            urlretrieve(listing.url, filename)
            time.sleep(1)


if __name__ == "__main__":
    frameit()
