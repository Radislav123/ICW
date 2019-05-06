import logging.config


logging.config.fileConfig("logger.conf")
logger = logging.getLogger("pickletax")

logger.info("start")
logger.debug("test")
logger.critical("finish")
