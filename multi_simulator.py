import paho.mqtt.client as mqtt
import random
import json
import time

client = mqtt.Client()

TB_HOST = "localhost"
TB_PORT = 1884

devices = {
    "node1": "zv1EsR2CKcD5EyShCkuy",
    "node2": "caOfRYlovgGlTctnDYaO",
    "node3": "YZam31H6yZi0BT0z2cE6",
    "node4": "cMcVraXVVR9JtDQIyaTb",
    "node5": "AJta4Jaz1EMOoeVHUqTv",
    "node6": "QTGdzLZmo9q9mxB5Kph1",
    "node7": "ZA7wCoil8NRnJilwjqDb",
    "node8": "ncsmuY46jXmsyc9EcB4L",
    "node9": "cvm4arvGRQhMOO4tnzMx",
    "node10": "4xYE0zLa0TRDV1GWoD7t"
}

zone2_devices = [
    "node6",
    "node7",
    "node8",
    "node9",
    "node10"
]

while True:

    for device_name, token in devices.items():

        client.username_pw_set(token)

        client.connect(TB_HOST, TB_PORT, 60)

        temperature = round(random.uniform(10, 35), 2)
        humidity = round(random.uniform(60, 95), 2)
        leaf_wetness = round(random.uniform(1, 10), 2)
        rainfall = round(random.uniform(0, 10), 2)

        if humidity > 85 and 18 <= temperature <= 25 and leaf_wetness > 8 and rainfall > 5:
            risk = "CRITICAL"

        elif humidity > 85 and 18 <= temperature <= 25:
            risk = "HIGH"

        elif 70 <= humidity <= 85 and 15 <= temperature <= 25:
            risk = "MODERATE"

        else:
            risk = "LOW"

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "leaf_wetness": leaf_wetness,
            "rainfall": rainfall,
            "risk_level": risk
        }

        if device_name in zone2_devices:

            data["fw_title"] = "CropMonitorFirmware"
            data["fw_version"] = "2.0"

            state = random.choice([
                "DOWNLOADING",
                "DOWNLOADED",
                "UPDATED",
                "FAILED"
            ])

            data["fw_state"] = state

            if state == "FAILED":
                data["rollback"] = "Firmware reverted to v1.0"

        client.publish(
            "v1/devices/me/telemetry",
            json.dumps(data)
        )

        print(device_name, data)

        client.disconnect()

    print("========== MQTT DATA SENT ==========")

    time.sleep(5)