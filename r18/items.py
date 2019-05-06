from typing import Dict, Generator, List, Tuple

from scrapy.item import Field, Item
from scrapy.loader.processors import TakeFirst
from scrapy.selector import Selector


class ParseActresses(object):
    def __call__(self, value: List[str]) -> Generator[Tuple[str, str], None, None]:
        for _ in value:
            href, text = Selector(text=_).css("a::attr(href), span::text").extract()
            yield href, text.strip()


class ParseCategories(object):
    def __call__(self, value: List[str]) -> Generator[Tuple[str, str], None, None]:
        for _ in value:
            href, text = Selector(text=_).css("a::attr(href), a::text").extract()
            yield href, text.strip()


class ParseDetail(object):
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

    def __call__(self, v: List[str]) -> Generator[Dict[str, str], None, None]:
        for _ in v:
            div = Selector(text=_)
            product = dict()
            for k, v in zip(div.css("dt::text").extract(), div.css("dd")):
                _k = k[:-1]
                _func = self.product_parser.get(
                    _k, lambda x: x.css("dd::text").get().strip()
                )
                _v = _func(v)
                if _v and _v != "----":
                    product.update({_k: _v})
            yield product


class R18DetailItem(Item):
    url = Field(output_processor=TakeFirst())
    name = Field(output_processor=TakeFirst())
    image_cover = Field(output_processor=TakeFirst())
    image_thumbnail = Field()
    image_detail_view = Field()
    detail = Field(input_processor=ParseDetail(), output_processor=TakeFirst())
    actresses = Field(input_processor=ParseActresses())
    categories = Field(input_processor=ParseCategories())
