import json


def process_message(loaded_model, str1):
    if loaded_model is None:
        print("Loaded model is None. Skipping prediction.")
        return

    try:
        # print(str1)
        json_obj = json.loads(str1)
        temper = float(json_obj["Temperature"])
        humid = float(json_obj["Humidity"])
        press = float(json_obj["Pressure"])
        X_test = [[temper, humid, press]]
        y_pred = loaded_model.predict(X_test)
        print("Kafka:X_test", temper, humid, press)
        print("Kafka:y_pred", y_pred)
    except Exception as e:
        print(f"Error processing message: {e}")
