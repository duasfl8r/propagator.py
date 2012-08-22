import logging, logging.config
from art.config import LOGGING
logging.config.dictConfig(LOGGING)

logger = logging.getLogger("art")

debug, info, warn, error = logger.debug, logger.info, logger.warn, logger.error
