/*
 * SuperSensePy - IoT-Anomaly-Detection in Python Language
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
import paho.mqtt.client as mqtt


class MqttClient:

    def __init__(self, host="127.0.0.1", port=1883):
        self.host = host
        self.port = port
        self.client = mqtt.Client()

    def connect(self, keepalive=60):
        return self.client.connect(self.host, self.port, keepalive)

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self, topic="#", qos=0):
        self.client.subscribe(topic, qos)

    def publish(self, topic, payload, qos=0, retain=False):
        self.client.publish(topic, payload, qos, retain)

    def on_connect(self, func):
        self.client.on_connect = func

    def on_disconnect(self, func):
        self.client.on_disconnect = func

    def on_subscribe(self, func):
        self.client.on_subscribe = func

    def on_message(self, func):
        self.client.on_message = func

    def on_publish(self, func):
        self.client.on_publish = func
