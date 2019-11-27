"""
pipelines configuration for this spider
"""
from txmongo.filter import ASCENDING

from r18.settings import ITEM_PIPELINES, get_env_var

ITEM_PIPELINES.update(
    {
        "r18.pipelines.R18ImagesPipeline": 300,
        "scrapy_pipelines.pipelines.mongo.MongoPipeline": 301,
    }
)

IMAGES_URLS_FIELD = "image_detail_view"
IMAGES_STORE = "./images"

PIPELINE_MONGO_DATABASE = "r18"

PIPELINE_MONGO_USERNAME = "r18"
PIPELINE_MONGO_PASSWORD = get_env_var(
    "R18_MONGO_PASSWORD", default="r18_mongo_password"
)

PIPELINE_MONGO_COLLECTION = "detail"

PIPELINE_MONGO_INDEXES = [
    ("url", ASCENDING),
    ("name", ASCENDING),
    ("actresses.name", ASCENDING),
    ("categories.name", ASCENDING),
    ("detail.Runtime", ASCENDING),
    ("detail.Studio.name", ASCENDING),
    ("detail.Label", ASCENDING),
    ("detail.Channel.name", ASCENDING),
    ("detail.Content ID", ASCENDING),
    (
        "detail.DVD ID",
        ASCENDING,
        {
            "unique": True,
            "partialFilterExpression": {"detail.DVD ID": {"$exists": True}},
        },
    ),
]
