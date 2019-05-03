from urllib.parse import urlparse, urlunparse

from scrapy.http import Request, Response
from scrapy.spiders import SitemapSpider

from r18.items import R18DetialItem


class R18SitemapSpider(SitemapSpider):
    name = "R18 Sitemap"
    sitemap_urls = ["http://www.r18.com/sitemap.xml"]
    sitemap_rules = [
        (
            r"https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=zh)",
            "redirect_to_en",
        ),
        (
            r"https:\/\/www\.r18\.com\/videos\/vod\/(.+)\/detail\/-\/id=.+\/(\?lg=en)",
            "parse_detail",
        ),
    ]

    product_parser = {
        "Channel": lambda x: list(
            (text.strip(), href)
            for text, href in zip(
                x.css("a::text").extract(), x.css("a::attr(href)").extract()
            )
        ),
        "Runtime": lambda x: " ".join(x.css("dd::text").get().strip().split()),
        "Series": lambda x: list(
            (text.strip(), href)
            for text, href in zip(
                x.css("a::text").extract(), x.css("a::attr(href)").extract()
            )
        ),
        "Studio": lambda x: list(
            (text.strip(), href)
            for text, href in zip(
                x.css("a::text").extract(), x.css("a::attr(href)").extract()
            )
        ),
    }

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
        @returns items 1 1
        @returns requests 0 0
        @scrapes url name image detail
        """
        div = response.css(".product-details-page")

        product = dict()
        for key, value in zip(div.css("dt::text").extract(), div.css("dd")):
            _key = key[:-1]
            _func = self.product_parser.get(
                _key, lambda x: x.css("dd::text").get().strip()
            )
            product.update({_key: _func(value)})

        item = R18DetialItem()

        item.update(
            {
                "url": response.url,
                "name": div.css("cite::text").get(),
                "image": {
                    "cover": div.css(
                        "img:not([alt='close']):not([class]):not([itemprop])::attr(src)"
                    ).get(),
                    "lazy": div.css("img[class='lazyOwl']::attr(data-src)").extract(),
                },
                "detail": product,
            }
        )

        yield item
