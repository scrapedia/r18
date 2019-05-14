"""
pipelines configuration for this spider
"""
from r18.settings import ITEM_PIPELINES

ITEM_PIPELINES.update({"r18.pipelines.R18ImagesPipeline": 300})

IMAGES_URLS_FIELD = "image_detail_view"
IMAGES_STORE = "./images"
