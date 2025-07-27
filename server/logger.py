import logging

def setup_logger(name="MedMind"):
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)

    return logger


logger=setup_logger()

logger.info("MedMind Server Started")
logger.debug("Logger is set up with DEBUG level")
logger.error("This is an error message for testing purposes")
logger.critical("This is a critical message for testing purposes")


    