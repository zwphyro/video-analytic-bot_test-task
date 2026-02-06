import logging


def configure_logging(log_level):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s\t%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
