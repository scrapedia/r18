from urllib.parse import urlparse, urlunparse

from scrapy.http import Request, Response
from scrapy.spiders import SitemapSpider


class R18SitemapSpider(SitemapSpider):
    name = "R18 Sitemap"
    sitemap_urls = ["http://www.r18.com/sitemap.xml"]
    sitemap_rules = [
        (
            r"https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=zh)",
            "redirect_to_en"),
        (
            r"https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=en)",
            "parse_detail"),
    ]

    def redirect_to_en(self, response: Response):
        """

        :param response:
        :return:

        @url https://www.r18.com/videos/vod/amateur/detail/-/id=got031121/?lg=zh
        @returns items 0 0
        @returns requests 1 1
        """
        url = urlunparse(urlparse(response.url)._replace(query="lg=en"))
        yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response: Response):
        """

        :param response:
        :return:
        @url https://www.r18.com/videos/vod/amateur/detail/-/id=got031121/?lg=en
        @return item 1 1
        @scrape
        """
        if response.request.url.startswith("https://www.r18.com/videos/vod/"):
            print("Redirect from {}".format(response.request.url))
        else:
            print("Direct from {}".format(response.request.url))
