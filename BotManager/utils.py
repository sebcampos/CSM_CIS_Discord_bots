import logging


def init_logger(name) -> logging.Logger:
    # Creating and Configuring Logger

    Log_Format = f"[%(asctime)s][%(name)s][%(levelname)s\t] - %(message)s"

    logging.basicConfig(
        format=Log_Format,
    )

    logger = logging.getLogger(name)
    logger.setLevel("INFO")
    return logger
