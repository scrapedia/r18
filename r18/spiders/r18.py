"""
The spider for r18
"""
from typing import Generator, List, Tuple

from scrapy.http import Response
from scrapy.item import Item
from scrapy.loader import ItemLoader
from scrapy.spiders import SitemapSpider

from r18.items import R18DetailItem


class R18SitemapSpider(SitemapSpider):
    """
    R18 sitemap spider
    """

    name: str = "R18 Sitemap"
    sitemap_urls: List[str] = ["http://www.r18.com/sitemap.xml"]
    sitemap_rules: List[Tuple[str, str]] = [
        (
            r"^https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=(?P<lang>(zh|en)))?$",
            "parse_detail",
        )
    ]

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

        self.crawler.stats.inc_value("r18/en_detail_count")

        detail_il: ItemLoader = ItemLoader(
            item=R18DetailItem(), selector=response.css(".product-details-page")
        )

        detail_il.add_value("url", response.url)
        detail_il.add_css("name", "cite::text")
        detail_il.add_css("image_cover", ".detail-single-picture img::attr(src)")
        detail_il.add_css("image_thumbnail", ".lazy::attr(data-original)")
        detail_il.add_css("image_detail_view", ".lazyOwl::attr(data-src)")
        detail_il.add_css("detail", ".product-details dl")

        if detail_il.get_css(css=".pop-list a[itemprop='url']"):
            detail_il.add_css("actresses", ".pop-list a[itemprop='url']")
        if detail_il.get_css(css=".pop-list a[itemprop='genre']"):
            detail_il.add_css("categories", ".pop-list a[itemprop='genre']")

        yield detail_il.load_item()
