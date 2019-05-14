"""
The spider for r18
"""
from typing import Generator
from urllib.parse import urlparse, urlunparse

from scrapy.http import Request, Response
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider

from r18.items import R18DetailItem


class R18SitemapSpider(SitemapSpider):
    name = "R18 Sitemap"
    sitemap_urls = ["http://www.r18.com/sitemap.xml"]
    sitemap_rules = [
        (
            r"^https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=zh)",
            "redirect_to_en",
        ),
        (
            r"^https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=en)",
            "parse_detail",
        ),
    ]

    def redirect_to_en(self, response: Response) -> Generator[Request, None, None]:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: Generator

        @url https://www.r18.com/videos/vod/amateur/detail/-/id=got031121/?lg=zh
        @returns items 0 0
        @returns requests 1 1
        """

        self.crawler.stats.inc_value("r18/zh_count")

        url = urlunparse(urlparse(response.url)._replace(query="lg=en"))
        yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response: Response) -> Generator[Item, None, None]:
        """

        :param response:
        :type response: Response
        :return:
        :rtype: Generator

        @url https://www.r18.com/videos/vod/amateur/detail/-/id=got031121/?lg=en
        @returns items 1 1
        @returns requests 0 0
        @scrapes url name image_cover image_thumbnail image_detail_view detail
        """

        self.crawler.stats.inc_value("r18/en_count")

        il = ItemLoader(
            item=R18DetailItem(), selector=response.css(".product-details-page")
        )

        il.add_value("url", response.url)
        il.add_css("name", "cite::text")
        il.add_css("image_cover", ".detail-single-picture img::attr(src)")
        il.add_css("image_thumbnail", ".lazy::attr(data-original)")
        il.add_css("image_detail_view", ".lazyOwl::attr(data-src)")
        il.add_css("detail", ".product-details dl")

        if il.get_css(css=".pop-list a[itemprop='url']"):
            il.add_css("actresses", ".pop-list a[itemprop='url']")
        if il.get_css(css=".pop-list a[itemprop='genre']"):
            il.add_css("categories", ".pop-list a[itemprop='genre']")

        yield il.load_item()
