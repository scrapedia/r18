# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS: int = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY: int = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN: int = 1
# CONCURRENT_REQUESTS_PER_IP: int = 16
