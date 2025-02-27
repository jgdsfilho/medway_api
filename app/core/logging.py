import logging

from medway_api import settings

log_level = logging.DEBUG if settings.DEBUG else logging.INFO


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=log_level,
    handlers=[
        logging.StreamHandler(),
    ],
)
