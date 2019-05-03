from scrapy.item import Field, Item


class R18DetialItem(Item):
    url = Field()

    name = Field()
    image = Field()
    detail = Field()
