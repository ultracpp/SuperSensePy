import time
import logging
import logging.config
from Utils import *


def run_log_adapter(queue):
    logging.config.fileConfig(get_conf_path("log"))
    logger = logging.getLogger()

    while True:
        try:
            if queue.empty():
                time.sleep(0.1)
                continue

            dic = queue.get()

            level = dic["level"]
            msg = dic["msg"]

            if level == logging.DEBUG:
                logger.debug(msg)
            elif level == logging.INFO:
                logger.info(msg)
            elif level == logging.WARNING:
                logger.warning(msg)
            elif level == logging.ERROR:
                logger.error(msg)
            elif level == logging.CRITICAL:
                logger.critical(msg)

        except Exception as err:
            print(f"Error in log adapter: {err}")
