from collections import deque
import json
import numpy as np
from skmultiflow.anomaly_detection import HalfSpaceTrees

my_hst = HalfSpaceTrees(n_estimators=25, window_size=250, depth=15, random_state=1)
queue = deque(maxlen=250)


def process_message(loaded_model, str1):
    try:
        global queue

        json_obj = json.loads(str1)
        to = json_obj["to"]
        arr1 = to.split('/')
        cnt = arr1[3]
        pc = json_obj["pc"]
        cin = pc["m2m:cin"]
        con = float(cin["con"])

        if cnt != "temper":
            return

        queue.append(con)

        if len(queue) == 250:
            X = np.array(queue).reshape(1, -1)
            ret = my_hst.predict(X)
            my_hst.partial_fit(X)

            if ret == 1:
                print("Detected anomaly:")
                print("Queue:", list(queue))
                print("Mqtt:ret", ret)

    except Exception as e:
        print(f"Error processing message: {e}")
