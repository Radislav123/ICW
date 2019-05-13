import logging.config
import re
from django.core.exceptions import ValidationError


logging.config.fileConfig("logger.conf")
logger = logging.getLogger("pickletax")

logger.info("start")
logger.debug("test")
logger.critical("finish")
