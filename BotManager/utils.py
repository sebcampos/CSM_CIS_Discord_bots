import logging
import sys


def init_logger(name):
    # Creating and Configuring Logger

    Log_Format = f"[%(asctime)s][%(name)s][%(levelname)s\t] - %(message)s"


    logging.basicConfig(
        format=Log_Format,
    )

    logger = logging.getLogger(name)
    logger.setLevel("INFO")
    return logger


