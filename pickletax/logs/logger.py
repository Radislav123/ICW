import logging.config
import os.path
import logging

log_path = os.path.abspath("logs\\pickletaxlogger.conf")
logging.config.fileConfig(log_path)
authorization_logger = logging.getLogger("pickletax.authorization")
unit_tests_logger = logging.getLogger("pickletax.unit_tests")
manage_logger = logging.getLogger("pickletax.manager")
