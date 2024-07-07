import multiprocessing as mp
import time
from AppConfig import *
from LogProcess import *
from MqttProcess import *
from KafkaProcess import *


def main():
    app = AppConfig.instance()
    app.load()

    ctx = mp.get_context('spawn')
    manager = mp.Manager()

    log_queue = manager.Queue()
    p_log = ctx.Process(target=run_log_adapter, args=(log_queue,))
    p_log.start()

    proc_map = {}

    def start_process(conf_name):
        dic_lock = manager.Lock()
        dic_queue = manager.Queue()

        if conf_name.startswith("mqtt"):
            process = ctx.Process(target=run_mqtt_adapter,
                                  args=(app.MODEL_PATH, dic_lock, dic_queue, conf_name, log_queue,))
        elif conf_name.startswith("kafka"):
            process = ctx.Process(target=run_kafka_adapter,
                                  args=(app.MODEL_PATH, dic_lock, dic_queue, conf_name, log_queue,))

        process.start()
        return process, dic_queue

    try:
        for conf_name in app.arr_input_adapter:
            proc_map[conf_name] = start_process(conf_name)

        for conf_name in app.arr_output_adapter:
            proc_map[conf_name] = start_process(conf_name)

        while True:
            str1 = input()
            arr1 = str1.split()

            if len(arr1) == 1:
                print(arr1[0])
            elif len(arr1) >= 2:
                cmd = arr1[0]
                conf = arr1[1]

                if cmd == "reload" and conf in proc_map:
                    proc, queue = proc_map[conf]
                    proc.terminate()
                    proc.join()

                    proc_map[conf] = start_process(conf)

    except Exception as err:
        print(err)
    finally:
        # Clean up processes
        p_log.terminate()
        p_log.join()
        for proc, _ in proc_map.values():
            proc.terminate()
            proc.join()


if __name__ == '__main__':
    main()
