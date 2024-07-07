from Utils import get_conf_path


class KafkaConfig:

    def __init__(self, conf_name):
        self.conf_path = get_conf_path(conf_name)

        self.host = "127.0.0.1"
        self.port = 9092
        self.topic = "SuperSensePy"
        self.poll_timeout = 500
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
                        "KAFKA_HOST": lambda val: setattr(self, 'host', val),
                        "KAFKA_PORT": lambda val: setattr(self, 'port', int(val)),
                        "KAFKA_TOPIC": lambda val: setattr(self, 'topic', val),
                        "KAFKA_POLL_TIMEOUT": lambda val: setattr(self, 'poll_timeout', int(val)),
                        "MODELS": lambda val: setattr(self, 'arr_model', val.split(",")),
                    }

                    if key in config_mapping:
                        config_mapping[key](value)

                print("KAFKA_HOST:", self.host)
                print("KAFKA_PORT:", self.port)
                print("KAFKA_TOPIC:", self.topic)
                print("KAFKA_POLL_TIMEOUT:", self.poll_timeout)
                print("MODELS:", self.arr_model)

        except FileNotFoundError:
            print(f"Configuration file not found: {self.conf_path}")
        except Exception as e:
            print(f"Error loading configuration: {e}")

        print("==========")
