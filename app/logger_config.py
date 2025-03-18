import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from dotenv import load_dotenv
import os

load_dotenv()

sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[sentry_logging],
    send_default_pii=True,
    traces_sample_rate=1.0,
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
)

logger = logging.getLogger(__name__)
