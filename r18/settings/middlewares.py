from r18.settings import DOWNLOADER_MIDDLEWARES

DOWNLOADER_MIDDLEWARES.update({"r18.middlewares.RedirectToEnMiddleware": 50})
