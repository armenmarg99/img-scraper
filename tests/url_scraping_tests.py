import unittest
from unittest import mock

import pathlib
from os.path import join

from bs4 import BeautifulSoup

from url_scraper import UrlScraper
from .outputs.url_scrapper_outputs.gmail import real_links
from .outputs.url_scrapper_outputs.rezka_images import real_img_urls

CUR_DIR = pathlib.Path(__file__).parent.absolute()


class UrlScrapperTestCase(unittest.TestCase):
    def setUp(self):
        self.webpages_dir = join(CUR_DIR, "webpages")

    def test_get_links_with_same_domain(self):
        url_scrapper = UrlScraper(url='https://accounts.google.com/b/0/AddMailService')
        with open(join(self.webpages_dir, 'gmail.html'), 'rb') as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
        with mock.patch.object(url_scrapper, '_soup', soup):
            links = url_scrapper.get_links_with_same_domain()
            self.assertSetEqual(links, real_links)

    def test_get_img_urls(self):
        url_scrapper = UrlScraper(url='https://rezka.ag')
        with open(join(self.webpages_dir, 'rezka.html'), 'rb') as html_file:
            soup = BeautifulSoup(html_file, "html.parser")
        with mock.patch.object(url_scrapper, '_soup', soup):
            img_urls = url_scrapper.get_img_urls()
            self.assertSetEqual(img_urls, real_img_urls)
