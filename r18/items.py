"""
The parsers used in ItemLoader and Item's processors
"""
import re
from datetime import datetime
from typing import Dict, Generator, Iterable, List

from scrapy.item import Field, Item
from scrapy.loader.processors import TakeFirst
from scrapy.selector import Selector

PATTERN_RUNTIME = re.compile(
    r"(?P<runtime>\d+)min\.(\s\(HD:\s(?P<hd_runtime>\d+)min\.\))?", flags=re.VERBOSE
)


class ParseActresses:  # pylint: disable=too-few-public-methods
    """
    actresses parser for field actresses
    """

    def __call__(self, actresses: List[str]) -> Generator[Dict[str, str], None, None]:
        for _ in actresses:
            href, text = Selector(text=_).css("a::attr(href), span::text").extract()
            yield {"name": text.strip(), "url": href}


class ParseCategories:  # pylint: disable=too-few-public-methods
    """
    categories parser for field categories
    """

    def __call__(self, categories: List[str]) -> Generator[Dict[str, str], None, None]:
        for _ in categories:
            href, text = Selector(text=_).css("a::attr(href), a::text").extract()
            yield {"name": text.strip(), "url": href}


class ParseDetail:  # pylint: disable=too-few-public-methods
    """
    detail parser for field detail
    """

    def __init__(self):
        self.product_parser = {
            "Channel": self._parse_channel,
            "Release Date": self._release_date,
            "Runtime": self._parse_runtime,
            "Series": self._parse_series,
            "Studio": self._parse_studio,
        }

    @staticmethod
    def _parse_channel(channel: Selector) -> List[Dict[str, str]]:
        _channel = list()
        for text, href in zip(
            channel.css("a::text").extract(),  # pylint: disable=bad-continuation
            channel.css("a::attr(href)").extract(),  # pylint: disable=bad-continuation
        ):
            _channel.append({"name": text.strip(), "url": href})
        return _channel

    @staticmethod
    def _release_date(release_date: Selector) -> datetime:
        _release_date = release_date.css("dd::text").get().strip()
        replace_pair = (("june", "jun"), ("july", "jul"), ("sept", "sep"))
        _ = _release_date.lower()
        for pair in replace_pair:
            _ = _.replace(*pair)
        try:
            return datetime.strptime(_, "%b. %d, %Y")
        except ValueError:
            return datetime.strptime(_, "%b %d, %Y")

    @staticmethod
    def _parse_runtime(runtime: Selector):
        _runtime = " ".join(runtime.css("dd::text").get().strip().split())
        return int(PATTERN_RUNTIME.match(_runtime).group("runtime"))

    @staticmethod
    def _parse_series(series: Selector):
        _series = dict()
        for text, href in zip(
            series.css("a::text").extract(),  # pylint: disable=bad-continuation
            series.css("a::attr(href)").extract(),  # pylint: disable=bad-continuation
        ):
            _series.update({"name": text.strip(), "url": href})
        return _series

    @staticmethod
    def _parse_studio(studio: Selector) -> List[Dict[str, str]]:
        _studio = list()
        for text, href in zip(
            studio.css("a::text").extract(),  # pylint: disable=bad-continuation
            studio.css("a::attr(href)").extract(),  # pylint: disable=bad-continuation
        ):
            _studio.append({"name": text.strip(), "url": href})
        return _studio

    def __call__(self, values: List[str]) -> Generator[Dict[str, str], None, None]:
        for _ in values:
            div = Selector(text=_)
            product = dict()
            for k, value in zip(div.css("dt::text").extract(), div.css("dd")):
                _k = k[:-1]
                _func = self.product_parser.get(
                    _k, lambda x: x.css("dd::text").get().strip()
                )
                try:
                    _v = _func(value)
                except AttributeError:
                    pass
                else:
                    if _v and _v != "----":
                        product.update({_k.lower(): _v})
            yield product


class JoinDict:  # pylint: disable=too-few-public-methods
    """
    join multiple dictionaries into one
    """

    def __call__(self, values: Iterable[Dict]) -> Dict:
        _ = dict()
        for value in values:
            _.update(value)
        return _


class R18DetailItem(Item):
    """
    The item which store all data extracted from web pages
    """

    url = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())

    images = Field()
    image_cover = Field(output_processor=TakeFirst())
    image_thumbnail = Field()
    image_detail_view = Field()

    detail = Field(input_processor=ParseDetail(), output_processor=JoinDict())
    actresses = Field(input_processor=ParseActresses())
    categories = Field(input_processor=ParseCategories())
