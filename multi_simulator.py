import paho.mqtt.client as mqtt
import random
import json
import time

TB_HOST = "localhost"
TB_PORT = 1884

devices = {
    "zone1_node_1": "EkgiGxG2FTPGxVGxkG9f",
    "zone1_node_2": "lFiDKvCLj6mPDPo8B5xC",
    "zone1_node_3": "NdCARABFuFHlahVZYIz4",
    "zone1_node_4": "I084LO9eHFpZOeVq4mVZ",
    "zone1_node_5": "dE6kk88FlkkcNo5JVzxf",

    "zone2_node_1": "deiuBaMsqA2GR7ZRCHkN",
    "zone2_node_2": "bN7H1fmCvGYBClQTgL8Q",
    "zone2_node_3": "8BUFOLnkMTw5UmqLvVPJ",
    "zone2_node_4": "uWSRIYWQT3lh1Ofgc7zg",
    "zone2_node_5": "35KvcSt0sHudpb4yWPXM"
}

zone2_devices = [
    "zone2_node_1",
    "zone2_node_2",
    "zone2_node_3",
    "zone2_node_4",
    "zone2_node_5"
]

while True:

    for device_name, token in devices.items():

        client = mqtt.Client()

        # Set device token
        client.username_pw_set(token)

        # Connect to ThingsBoard MQTT
        client.connect(TB_HOST, TB_PORT, 60)

        # Generate random telemetry
        temperature = round(random.uniform(10, 35), 2)
        humidity = round(random.uniform(60, 95), 2)
        leaf_wetness = round(random.uniform(1, 10), 2)
        rainfall = round(random.uniform(0, 10), 2)

        # Disease Risk Logic
        if (
            humidity > 85 and
            18 <= temperature <= 25 and
            leaf_wetness > 8 and
            rainfall > 5
        ):
            risk = "CRITICAL"

        elif humidity > 85 and 18 <= temperature <= 25:
            risk = "HIGH"

        elif 70 <= humidity <= 85 and 15 <= temperature <= 25:
            risk = "MODERATE"

        else:
            risk = "LOW"

        telemetry = {
            "temperature": temperature,
            "humidity": humidity,
            "leaf_wetness": leaf_wetness,
            "rainfall": rainfall,
            "risk_level": risk
        }

        # OTA Simulation for Zone 2
        if device_name in zone2_devices:

            telemetry["fw_title"] = "CropMonitorFirmware"
            telemetry["fw_version"] = "2.0"

            state = random.choice([
                "DOWNLOADING",
                "DOWNLOADED",
                "VERIFIED",
                "UPDATING",
                "UPDATED",
                "FAILED"
            ])

            telemetry["fw_state"] = state

            if state == "FAILED":
                telemetry["rollback"] = "Firmware reverted to v1.0"

        # Publish telemetry
        result = client.publish(
            "v1/devices/me/telemetry",
            json.dumps(telemetry)
        )

        # Give MQTT time to send message
        client.loop(2)

        print(f"{device_name} -> {telemetry}")
        print("Publish result:", result.rc)
        print("-" * 50)

        client.disconnect()

    print("\nTelemetry sent for all devices.")
    print("Waiting 10 seconds...\n")

    time.sleep(10)