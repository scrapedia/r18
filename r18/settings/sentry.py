import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.WARNING)
sentry_sdk.init(
    dsn="http://<public-key>@<sentry>/<project-id>",
    integrations=[sentry_logging],
)
