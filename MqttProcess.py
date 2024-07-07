import importlib
import json
import os
import time

import joblib
import tensorflow as tf

from MqttConfig import MqttConfig
from MqttClient import MqttClient
from Utils import get_path


class MqttProcessVariable:
    def __init__(self, model_path, dic_lock, dic_queue, conf_name, log_queue):
        self.model_path = model_path
        self.dic_lock = dic_lock
        self.dic_queue = dic_queue
        self.conf_name = conf_name
        self.log_queue = log_queue

        self.loaded_module = None
        self.loaded_model = None

        self.mqttConfig = MqttConfig(conf_name)
        self.mqttClient = MqttClient(self.mqttConfig.host, self.mqttConfig.port)


mqttProcessVariable = None


def subscriber_connected(client, userdata, flags, rc):
    if rc == 0:
        mqttProcessVariable.log_queue.put({"level": "info", "msg": "subscriber:connected"})
        client.subscribe(mqttProcessVariable.mqttConfig.topic, 1)
    else:
        mqttProcessVariable.log_queue.put({"level": "info", "msg": "subscriber:rc=" + str(rc)})


def publisher_connected(client, userdata, flags, rc):
    if rc == 0:
        mqttProcessVariable.log_queue.put({"level": "info", "msg": "publisher:connected"})
    else:
        mqttProcessVariable.log_queue.put({"level": "info", "msg": "publisher:rc=" + str(rc)})


def on_disconnect(client, userdata, rc):
    mqttProcessVariable.log_queue.put({"level": "info", "msg": "on_disconnect" + str(rc)})

    while True:
        time.sleep(1)
        try:
            if client.connect(mqttProcessVariable.mqttConfig.host, mqttProcessVariable.mqttConfig.port) == 0:
                break
        except Exception as e:
            mqttProcessVariable.log_queue.put({"level": "warn", "msg": str(e)})


def on_subscribe(client, userdata, mid, granted_qos):
    mqttProcessVariable.log_queue.put({"level": "info", "msg": "on_subscribe, " + str(mid) + ", " + str(granted_qos)})


def on_message(client, userdata, message):
    try:
        str1 = message.payload.decode("utf-8")
        if mqttProcessVariable.loaded_module is not None:
            mqttProcessVariable.loaded_module.process_message(mqttProcessVariable.loaded_model, str1)
    except Exception as e:
        mqttProcessVariable.log_queue.put({"level": "warn", "msg": str(e)})


def on_publish(client, userdata, mid):
    mqttProcessVariable.log_queue.put({"level": "info", "msg": "on_publish, " + str(mid)})


def load_models():
    for model_name in mqttProcessVariable.mqttConfig.arr_model:
        model_file_path = os.path.join(mqttProcessVariable.model_path, model_name)
        if model_name.endswith(".pkl"):
            mqttProcessVariable.loaded_model = joblib.load(model_file_path)
        elif model_name.endswith(".h5"):
            mqttProcessVariable.loaded_model = tf.keras.models.load_model(model_file_path)
        mqttProcessVariable.log_queue.put({"level": "info", "msg": f"loaded : {model_file_path}"})
        mqttProcessVariable.log_queue.put(
            {"level": "info", "msg": f"loaded_model : {mqttProcessVariable.loaded_model}"})


def run_mqtt_adapter(model_path, dic_lock, dic_queue, conf_name, log_queue):
    global mqttProcessVariable
    mqttProcessVariable = MqttProcessVariable(model_path, dic_lock, dic_queue, conf_name, log_queue)

    module_path = os.path.join(get_path("modules"), f"{conf_name}_process.py")

    if os.path.isfile(module_path):
        mqttProcessVariable.loaded_module = importlib.import_module(f"modules.{conf_name}_process")

    mqttProcessVariable.mqttConfig.load()

    if "input" in conf_name and mqttProcessVariable.mqttConfig.arr_model:
        load_models()

    mqttClient = mqttProcessVariable.mqttClient

    if "input" in conf_name:
        mqttClient.on_connect(subscriber_connected)
        mqttClient.on_disconnect(on_disconnect)
        mqttClient.on_subscribe(on_subscribe)
        mqttClient.on_message(on_message)
    else:
        mqttClient.on_connect(publisher_connected)
        mqttClient.on_disconnect(on_disconnect)
        mqttClient.on_publish(on_publish)

    mqttClient.connect()
    mqttClient.client.loop_start()

    lock = mqttProcessVariable.dic_lock[conf_name]
    queue = mqttProcessVariable.dic_queue[conf_name]

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

            if cmd == "publish":
                mqttClient.publish(mqttProcessVariable.mqttConfig.topic, msg)
                log_queue.put({"level": "info", "msg": f"{conf_name}, publish"})
            elif cmd == "reload":
                log_queue.put({"level": "info", "msg": f"{conf_name}, {cmd}, {msg}"})
                if msg == "":
                    importlib.reload(mqttProcessVariable.loaded_module)
                elif msg.endswith(".pkl"):
                    model_file_path = os.path.join(model_path, msg)
                    mqttProcessVariable.loaded_model = joblib.load(model_file_path)
                elif msg.endswith(".h5"):
                    model_file_path = os.path.join(model_path, msg)
                    mqttProcessVariable.loaded_model = tf.keras.models.load_model(model_file_path)
                log_queue.put({"level": "info", "msg": f"reloaded : {model_file_path}"})
                log_queue.put({"level": "info", "msg": f"loaded_model : {mqttProcessVariable.loaded_model}"})
        except Exception as e:
            log_queue.put({"level": "warn", "msg": str(e)})
