from collections import deque
import json
from MyRRCF import MyRRCF

my_rrcf = MyRRCF(25, 250, 15)
queue = deque(maxlen=250)


def process_message(loaded_model, str1):
    try:
        json_obj = json.loads(str1)
        to = json_obj["to"]
        arr1 = to.split('/')
        cnt = arr1[3]

        if cnt != "temper":
            return

        pc = json_obj["pc"]
        cin = pc["m2m:cin"]
        con = float(cin["con"])

        queue.append(con)

        if len(queue) == 250:
            z = my_rrcf.anomaly_detection(queue)

            if z > 3.0 or z < -3.0:
                print("Detected anomaly:")
                print("Queue:", list(queue))
                print("Z-score:", z)

    except Exception as err:
        print(f"Error processing message: {err}")
