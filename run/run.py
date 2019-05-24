import sys
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append(str(Path("/").joinpath(*Path(__file__).parts[:-2])))

modules = [
    "r18.settings.autothrottle",
    "r18.settings.concurrent",
    "r18.settings.cookies",
    "r18.settings.httpcache",
    "r18.settings.logging",
    "r18.settings.middlewares",
    "r18.settings.pipelines",
    "r18.settings.sentry",
    "r18.settings.user_agent",
]

if __name__ == "__main__":
    settings = get_project_settings()

    for module in modules:
        settings.setmodule(module=module)

    process = CrawlerProcess(settings=settings)

    process.crawl("R18 Sitemap")

    process.start()
