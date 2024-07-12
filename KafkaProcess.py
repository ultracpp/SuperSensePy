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
import importlib
import json
import kafka
import os
import time
from threading import Thread, Lock

import joblib
import tensorflow as tf

from KafkaConfig import KafkaConfig
from Utils import get_path, random_string


class KafkaProcessVariable:
    def __init__(self):
        self.model_path = None
        self.dic_lock = {}
        self.dic_queue = {}
        self.conf_name = None
        self.log_queue = None

        self.loaded_module = None
        self.loaded_model = None
        self.kafka_config = None


kafka_process_variable = KafkaProcessVariable()


def consumer_func():
    consumer = kafka.KafkaConsumer(
        kafka_process_variable.kafka_config.topic,
        bootstrap_servers=[kafka_process_variable.kafka_config.host],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=random_string(8),
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=-1
    )

    for message in consumer:
        try:
            if kafka_process_variable.loaded_module:
                kafka_process_variable.loaded_module.process_message(kafka_process_variable.loaded_model, message.value)
        except Exception as e:
            kafka_process_variable.log_queue.put({"level": "warn", "msg": str(e)})


def producer_func():
    producer = kafka.KafkaProducer(
        acks=0,
        compression_type='gzip',
        bootstrap_servers=[kafka_process_variable.kafka_config.host],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer


def load_model(model_name, model_path, log_queue):
    model_file_path = os.path.join(model_path, model_name)
    if model_name.endswith(".pkl"):
        model = joblib.load(model_file_path)
    elif model_name.endswith(".h5"):
        model = tf.keras.models.load_model(model_file_path)
    else:
        raise ValueError("Unsupported model format")

    log_queue.put({"level": "info", "msg": f"loaded: {model_file_path}"})
    log_queue.put({"level": "info", "msg": f"loaded_model: {model}"})
    return model


def run_kafka_adapter(model_path, dic_lock, dic_queue, conf_name, log_queue):
    kafka_process_variable.model_path = model_path
    kafka_process_variable.dic_lock = dic_lock
    kafka_process_variable.dic_queue = dic_queue
    kafka_process_variable.conf_name = conf_name
    kafka_process_variable.log_queue = log_queue

    module_path = os.path.join(get_path("modules"), f"{conf_name}_process.py")
    if os.path.isfile(module_path):
        kafka_process_variable.loaded_module = importlib.import_module(f"modules.{conf_name}_process")

    kafka_process_variable.kafka_config = KafkaConfig(conf_name)
    kafka_process_variable.kafka_config.load()

    if "input" in conf_name and kafka_process_variable.kafka_config.arr_model:
        for model_name in kafka_process_variable.kafka_config.arr_model:
            kafka_process_variable.loaded_model = load_model(model_name, model_path, log_queue)

    if "input" in conf_name:
        Thread(target=consumer_func).start()
    else:
        producer = producer_func()

    lock = kafka_process_variable.dic_lock[conf_name]
    queue = kafka_process_variable.dic_queue[conf_name]

    while True:
        try:
            lock.acquire()
            if queue.empty():
                lock.release()
                time.sleep(1)
                continue

            dic = queue.get()
            lock.release()

            cmd = dic["cmd"]
            msg = dic["msg"]

            if cmd == "stop":
                break
            elif cmd == "produce":
                producer.send(kafka_process_variable.kafka_config.topic, value=msg)
                producer.flush()
                log_queue.put({"level": "info", "msg": f"{conf_name}, produce"})
            elif cmd == "reload":
                log_queue.put({"level": "info", "msg": f"{conf_name}, {cmd}, {msg}"})
                if msg == "":
                    importlib.reload(kafka_process_variable.loaded_module)
                else:
                    kafka_process_variable.loaded_model = load_model(msg, model_path, log_queue)
        except Exception as e:
            kafka_process_variable.log_queue.put({"level": "warn", "msg": str(e)})
        finally:
            if lock.locked():
                lock.release()

