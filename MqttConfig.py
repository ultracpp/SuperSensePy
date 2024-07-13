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
from Utils import get_conf_path


class MqttConfig:

    def __init__(self, conf_name):
        self.conf_path = get_conf_path(conf_name)

        self.host = "127.0.0.1"
        self.port = 1883
        self.topic = "/SuperSensePy/#"
        self.arr_model = None

    def load(self):
        try:
            with open(self.conf_path, encoding='UTF8') as conf_file:
                for line in conf_file:
                    line = line.strip()

                    if line.startswith("#") or "=" not in line:
                        continue

                    key, value = line.split("=", 1)

                    config_mapping = {
                        "MQTT_HOST": lambda val: setattr(self, 'host', val),
                        "MQTT_PORT": lambda val: setattr(self, 'port', int(val)),
                        "MQTT_TOPIC": lambda val: setattr(self, 'topic', val),
                        "MODELS": lambda val: setattr(self, 'arr_model', val.split(",")),
                    }

                    if key in config_mapping:
                        config_mapping[key](value)

                print("MQTT_HOST:", self.host)
                print("MQTT_PORT:", self.port)
                print("MQTT_TOPIC:", self.topic)
                print("MODELS:", self.arr_model)

        except FileNotFoundError:
            print(f"Configuration file not found: {self.conf_path}")
        except Exception as e:
            print(f"Error loading configuration: {e}")

        print("==========")
