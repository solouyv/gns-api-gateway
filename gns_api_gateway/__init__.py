import logging

from gns_api_gateway.settings import Settings

logging.basicConfig(
    level=Settings().logger_level.upper(),
    format="[%(asctime)s] [%(name)s: %(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S",
)
