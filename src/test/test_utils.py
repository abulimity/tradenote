from src.utils.log import logger
def test_logger():
    logger.info("test")
    logger.warning("test warning")
    logger.error("test error")
    logger.debug("test debug")
    logger.critical("test critical")