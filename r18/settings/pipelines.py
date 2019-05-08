from r18.settings import ITEM_PIPELINES

ITEM_PIPELINES.update({"r18.pipelines.R18Pipeline": 302})

IMAGES_URLS_FIELD = "image_detail_view"
IMAGES_STORE = "./images"
