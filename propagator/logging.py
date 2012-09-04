import logging, logging.config
from propagator.config import LOGGING
logging.config.dictConfig(LOGGING)

logger = logging.getLogger("propagator")

debug, info, warn, error = logger.debug, logger.info, logger.warn, logger.error
