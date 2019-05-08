import hashlib

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class R18Pipeline(ImagesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(R18Pipeline, self).__init__(
            store_uri, download_func=download_func, settings=settings
        )

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        sub_folder = image_guid[:2]
        return "full/{}/{}.jpg".format(sub_folder, image_guid)

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.images_result_field in item.fields:
            item[self.images_result_field] = {x["url"]: x for ok, x in results if ok}
        return item
