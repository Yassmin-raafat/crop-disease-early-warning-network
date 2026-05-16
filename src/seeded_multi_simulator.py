import argparse
import json
import random
import time
from dataclasses import dataclass

import paho.mqtt.client as mqtt


TB_HOST = "localhost"
TB_PORT = 1884
TELEMETRY_TOPIC = "v1/devices/me/telemetry"


DEVICE_TOKENS = {
    "zone1_node_1": "EkgiGxG2FTPGxVGxkG9f",
    "zone1_node_2": "lFiDKvCLj6mPDPo8B5xC",
    "zone1_node_3": "NdCARABFuFHlahVZYIz4",
    "zone1_node_4": "I084LO9eHFpZOeVq4mVZ",
    "zone1_node_5": "dE6kk88FlkkcNo5JVzxf",
    "zone2_node_1": "deiuBaMsqA2GR7ZRCHkN",
    "zone2_node_2": "bN7H1fmCvGYBClQTgL8Q",
    "zone2_node_3": "8BUFOLnkMTw5UmqLvVPJ",
    "zone2_node_4": "uWSRIYWQT3lh1Ofgc7zg",
    "zone2_node_5": "35KvcSt0sHudpb4yWPXM",
}


@dataclass
class Reading:
    temperature: float
    humidity: float
    leaf_wetness: float
    rainfall: float
    risk_level: str


def zone_for(device_name):
    return "Zone 2" if device_name.startswith("zone2") else "Zone 1"


def risk_level(temperature, humidity, leaf_wetness, rainfall):
    if humidity > 85 and 18 <= temperature <= 25 and leaf_wetness > 8 and rainfall > 5:
        return "CRITICAL"
    if humidity > 85 and 18 <= temperature <= 25:
        return "HIGH"
    if 70 <= humidity <= 85 and 15 <= temperature <= 25:
        return "MODERATE"
    return "LOW"


def generate_reading(device_name, cycle, rng):
    zone2 = device_name.startswith("zone2")
    node_offset = int(device_name.rsplit("_", 1)[1]) * 0.35

    if cycle < 4:
        temperature = 20.0 + node_offset + rng.uniform(-1.5, 1.5)
        humidity = 58.0 + rng.uniform(-4, 6)
        leaf_wetness = 1.0 + rng.uniform(0, 2)
        rainfall = 0.0
    elif cycle < 10:
        temperature = 21.0 + node_offset + rng.uniform(-1.0, 1.0)
        humidity = 68.0 + (cycle - 3) * 3.0 + rng.uniform(-2, 2)
        leaf_wetness = 3.0 + (cycle - 3) * 0.55 + rng.uniform(-0.4, 0.4)
        rainfall = 0.0
    elif cycle < 14:
        temperature = 22.0 + rng.uniform(-1.0, 1.0)
        humidity = 88.0 + rng.uniform(-1, 5)
        leaf_wetness = 6.5 + rng.uniform(-0.5, 1.0)
        rainfall = 0.0
    else:
        temperature = 22.0 + rng.uniform(-1.0, 1.0)
        humidity = 90.0 + rng.uniform(-1, 5)
        leaf_wetness = 8.6 + rng.uniform(-0.2, 1.3)
        rainfall = 6.0 + rng.uniform(0, 5)

    if zone2:
        humidity += 2.5
        leaf_wetness += 0.7

    temperature = round(temperature, 2)
    humidity = round(min(humidity, 99.0), 2)
    leaf_wetness = round(min(leaf_wetness, 12.0), 2)
    rainfall = round(rainfall, 2)

    return Reading(
        temperature=temperature,
        humidity=humidity,
        leaf_wetness=leaf_wetness,
        rainfall=rainfall,
        risk_level=risk_level(temperature, humidity, leaf_wetness, rainfall),
    )


def publish(device_name, token, reading):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(token)
    client.connect(TB_HOST, TB_PORT, 60)

    payload = {
        "deviceName": device_name,
        "zone": zone_for(device_name),
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "leaf_wetness": reading.leaf_wetness,
        "rainfall": reading.rainfall,
        "risk_level": reading.risk_level,
    }

    result = client.publish(TELEMETRY_TOPIC, json.dumps(payload), qos=1)
    client.loop(1)
    client.disconnect()
    return payload, result.rc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--cycles", type=int, default=18)
    parser.add_argument("--seed", type=int, default=453)
    args = parser.parse_args()

    rng = random.Random(args.seed)

    for cycle in range(args.cycles):
        print(f"\nCycle {cycle + 1}/{args.cycles}")
        for device_name, token in DEVICE_TOKENS.items():
            reading = generate_reading(device_name, cycle, rng)
            payload, rc = publish(device_name, token, reading)
            print(f"{device_name}: {payload} publish_rc={rc}")
        if cycle < args.cycles - 1:
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
