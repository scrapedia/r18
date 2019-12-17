"""
The basic settings for this spider
"""
import os
from typing import Any, Dict, List

from r18.exceptions import R18SettingsMissingException


def get_env_var(  # pylint: disable=bad-continuation
    var: str, default: Any = None
) -> Any:
    """
    Get the given variable from the environment
    :param var:
    :type var: str
    :param default:
    :type default: Any
    :return:
    :rtype: Any
    """
    try:
        return os.environ[var]
    except KeyError as exc:
        if default is None:
            raise R18SettingsMissingException from exc
        return default


BOT_NAME: str = "r18"

SPIDER_MODULES: List[str] = ["r18.spiders"]
NEWSPIDER_MODULE: str = "r18.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY: bool = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED: bool = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS: Dict[str, str] = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

SPIDER_MIDDLEWARES: Dict[str, int] = {}

DOWNLOADER_MIDDLEWARES: Dict[str, int] = {}

EXTENSIONS: Dict[str, int] = {}

ITEM_PIPELINES: Dict[str, int] = {}
