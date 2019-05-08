from typing import Dict, Generator, List, Tuple, Iterable

from scrapy.item import Field, Item
from scrapy.loader.processors import TakeFirst
from scrapy.selector import Selector


class ParseActresses(object):
    def __call__(self, actresses: List[str]) -> Generator[Tuple[str, str], None, None]:
        for _ in actresses:
            href, text = Selector(text=_).css("a::attr(href), span::text").extract()
            yield text.strip(), href


class ParseCategories(object):
    def __call__(self, categories: List[str]) -> Generator[Tuple[str, str], None, None]:
        for _ in categories:
            href, text = Selector(text=_).css("a::attr(href), a::text").extract()
            yield text.strip(), href


class ParseDetail(object):
    def __init__(self):
        self.product_parser = {
            "Channel": self._parse_channel,
            "Runtime": self._parse_runtime,
            "Series": self._parse_series,
            "Studio": self._parse_studio,
        }

    def _parse_channel(self, channel: Selector) -> Dict[str, str]:
        _channel = dict()
        for text, href in zip(
            channel.css("a::text").extract(), channel.css("a::attr(href)").extract()
        ):
            _channel.update({text.strip(): href})
        return _channel

    def _parse_runtime(self, runtime: Selector):
        _runtime = " ".join(runtime.css("dd::text").get().strip().split())
        return _runtime

    def _parse_series(self, series: Selector):
        _series = dict()
        for text, href in zip(
            series.css("a::text").extract(), series.css("a::attr(href)").extract()
        ):
            _series.update({text.strip(): href})
        return _series

    def _parse_studio(self, studio: Selector):
        _studio = dict()
        for text, href in zip(
            studio.css("a::text").extract(), studio.css("a::attr(href)").extract()
        ):
            _studio.update({text.strip(): href})
        return _studio

    def __call__(self, v: List[str]) -> Generator[Dict[str, str], None, None]:
        for _ in v:
            div = Selector(text=_)
            product = dict()
            for k, v in zip(div.css("dt::text").extract(), div.css("dd")):
                _k = k[:-1]
                _func = self.product_parser.get(
                    _k, lambda x: x.css("dd::text").get().strip()
                )
                try:
                    _v = _func(v)
                except AttributeError as err:
                    pass
                else:
                    if _v and _v != "----":
                        product.update({_k: _v})
            yield product


class JoinDict(object):
    def __call__(self, values: Iterable[Dict]) -> Dict:
        _ = dict()
        for d in values:
            _.update(d)
        return _


class R18DetailItem(Item):
    url = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())

    images = Field()
    image_cover = Field(output_processor=TakeFirst())
    image_thumbnail = Field()
    image_detail_view = Field()

    detail = Field(input_processor=ParseDetail(), output_processor=JoinDict())
    actresses = Field(input_processor=ParseActresses(), output_processor=dict)
    categories = Field(input_processor=ParseCategories(), output_processor=dict)
