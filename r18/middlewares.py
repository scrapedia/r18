"""
This file contains the middlewares developed only for this project
"""
from collections import namedtuple
from typing import Dict, Union
from urllib.parse import ParseResult, parse_qs, urlencode, urlparse, urlunparse

from scrapy.crawler import Crawler
from scrapy.http import Request
from scrapy.settings import Settings
from scrapy.spiders import Spider

URL = namedtuple("URL", ["url", "parse_result", "qs", "lg"])


class RedirectToEnMiddleware:
    """
    This downloader middleware redirects the zh detail request to en
    """

    def __init__(self, crawler: Crawler):
        """

        :param crawler:
        :type crawler: Crawler
        """
        self.crawler: Crawler = crawler
        self.settings: Settings = crawler.settings

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """

        :param crawler:
        :type crawler: Crawler
        :return:
        :rtype:
        """
        return cls(crawler)

    def process_request(self, request: Request, spider: Spider) -> Union[Request, None]:
        """

        :param request:
        :type request: Request
        :param spider:
        :type spider: Spider
        :return:
        :rtype:
        """
        url: str = self._get_url(request.url)
        if url != request.url:
            return request.replace(url=url)

    def _get_url(self, url: str) -> str:
        parsed_url: ParseResult = urlparse(url)
        parsed_query: Dict = parse_qs(parsed_url.query)

        try:
            lg = parsed_query.get("lg", [])[0]
        except IndexError:
            lg = None

        if lg == "zh":
            self.crawler.stats.inc_value("r18/zh_detail_count")
            parsed_query.update({"lg": ["en"]})
            parsed_url = parsed_url._replace(
                query=urlencode(query=parsed_query, doseq=True)
            )
            url = urlunparse(parsed_url)

        return url
