import logging
import os

from datetime import date

today = date.today()
curent_day = today.strftime("%d.%m.%Y")


def get_logger(name) -> logging.Logger:
    if not os.path.exists('./logs'):
        os.mkdir('./logs')
    else:
        pass
    FILENAME = f"logs/logging_{curent_day}.log"

    # logging.basicConfig(format=FORMAT,encoding="utf-8", datefmt=TIME_FORMAT, level=level,
    # filename=FILENAME)
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)
    f_format = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s]\n\t%(message)s')
    # root_logger.
    handler = logging.FileHandler(FILENAME, 'a', 'utf-8')
    handler.setFormatter(f_format)

    logger.addHandler(handler)

    return logger
