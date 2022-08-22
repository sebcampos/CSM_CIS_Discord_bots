import logging


def init_logger(name) -> logging.Logger:
    """
    Receives the name to add to the logger
    :param name: str
    :return: void
    """

    Log_Format = f"[%(asctime)s][%(name)s][%(levelname)s\t] - %(message)s"

    logging.basicConfig(
        format=Log_Format,
    )

    logger = logging.getLogger(name)
    logger.setLevel("INFO")
    return logger
