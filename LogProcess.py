/*
 * C RB Hash Map - Hash Map Implementation in C Language
 * Copyright (c) 2024 Eungsuk Jeon
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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
