from __future__ import annotations
from typing import TYPE_CHECKING, Set
if TYPE_CHECKING:
    from urllib.parse import ParseResult

import requests
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from utils.general import get_absolute_url, is_valid_url, get_short_url, download_image_and_check_size


class UrlScraper:
    def __init__(self, url: str):
        self._url = url
        self._soup = BeautifulSoup(requests.get(url).content, "html.parser")

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, new_url: str):
        if not is_valid_url(new_url):
            raise ValueError(f"Url {new_url} is not valid")
        self._url = new_url

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup

    @soup.setter
    def soup(self, new_soup: BeautifulSoup):
        self._soup = new_soup

    @property
    def url_parsed(self) -> ParseResult:
        return urlparse(self.url)

    @property
    def domain(self) -> str:
        return self.url_parsed.netloc

    @property
    def scheme(self) -> str:
        return self.url_parsed.scheme

    def get_links_with_same_domain(self) -> Set[str]:
        """
        Returns set of all the links on the webpage that have same domain as the webpage.
        """
        links = set()
        for anchor in self._soup.findAll('a'):
            if 'href' not in anchor.attrs:
                continue

            link = anchor.attrs.get('href')
            link = urljoin(self.url, link)
            link = get_absolute_url(link)

            if is_valid_url(link) and self.domain in link:
                links.add(get_short_url(link))
        return links

    def get_img_urls(self) -> Set[str]:
        """
        Returns set of all urls of images on the webpage that have size more than ``min_width`` and ``min_height``
        """
        urls = set()
        checked_urls = set()
        for img_tag in self._soup.findAll('img'):
            img_url = img_tag.attrs.get('src')
            img_url = urljoin(self.url, img_url)
            img_url = img_url.split('?')[0]
            if img_url in checked_urls:
                continue

            checked_urls.add(img_url)

            if not is_valid_url(img_url):
                continue

            urls.add(img_url)
        return urls

    def save_all_images(self, output_folder: str, min_width=20, min_height=20):
        urls = self.get_img_urls()
        for img in urls:
            download_image_and_check_size(img, output_folder, min_width=min_width, min_height=min_height)
