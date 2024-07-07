from Utils import get_conf_path, get_path
from SingletonInstane import SingletonInstane


class AppConfig(SingletonInstane):
    def __init__(self):
        self.conf_path = get_conf_path("app")

        self.STANDALONE = True

        self.MQTT_MANAGER_HOST = "127.0.0.1"
        self.MQTT_MANAGER_PORT = 1883
        self.MQTT_MANAGER_TOPIC = "/SuperSensePy/manager"

        self.MODEL_PATH = get_path("model")

        self.MYSQL_HOST = "127.0.0.1"
        self.MYSQL_PORT = 3306
        self.MYSQL_DB = "elvis"
        self.MYSQL_USER = "elvis"
        self.MYSQL_PASSWORD = "elvis"

        self.arr_input_adapter = None
        self.arr_output_adapter = None

    def load(self):
        try:
            with open(self.conf_path, encoding='UTF8') as conf_file:
                for line in conf_file:
                    line = line.strip()

                    if line.startswith("#") or "=" not in line:
                        continue

                    key, value = line.split("=", 1)

                    config_mapping = {
                        "STANDALONE": lambda val: setattr(self, key, val.lower() == "true"),
                        "MQTT_MANAGER_HOST": lambda val: setattr(self, key, val),
                        "MQTT_MANAGER_PORT": lambda val: setattr(self, key, int(val)),
                        "MQTT_MANAGER_TOPIC": lambda val: setattr(self, key, val),
                        "MODEL_PATH": lambda val: setattr(self, key, get_path(val)),
                        "MYSQL_HOST": lambda val: setattr(self, key, val),
                        "MYSQL_PORT": lambda val: setattr(self, key, int(val)),
                        "MYSQL_DB": lambda val: setattr(self, key, val),
                        "MYSQL_USER": lambda val: setattr(self, key, val),
                        "MYSQL_PASSWORD": lambda val: setattr(self, key, val),
                        "INPUT_ADAPTERS": lambda val: setattr(self, 'arr_input_adapter', val.split(",")),
                        "OUTPUT_ADAPTERS": lambda val: setattr(self, 'arr_output_adapter', val.split(",")),
                    }

                    if key in config_mapping:
                        config_mapping[key](value)

                print("STANDALONE:", self.STANDALONE)
                print("MQTT_MANAGER_HOST:", self.MQTT_MANAGER_HOST)
                print("MQTT_MANAGER_PORT:", self.MQTT_MANAGER_PORT)
                print("MQTT_MANAGER_TOPIC:", self.MQTT_MANAGER_TOPIC)
                print("MODEL_PATH:", self.MODEL_PATH)
                print("MYSQL_HOST:", self.MYSQL_HOST)
                print("MYSQL_PORT:", self.MYSQL_PORT)
                print("MYSQL_DB:", self.MYSQL_DB)
                print("MYSQL_USER:", self.MYSQL_USER)
                print("MYSQL_PASSWORD:", self.MYSQL_PASSWORD)
                print("arr_input_adapter:", self.arr_input_adapter)
                print("arr_output_adapter:", self.arr_output_adapter)

        except FileNotFoundError:
            print(f"Configuration file not found: {self.conf_path}")
        except Exception as e:
            print(f"Error loading configuration: {e}")

        print("==========")
