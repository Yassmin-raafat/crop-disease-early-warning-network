import argparse
import hashlib
import json
import time

import paho.mqtt.client as mqtt


TB_HOST = "localhost"
TB_PORT = 1884

TOKENS = {
    "zone2_node_1": "deiuBaMsqA2GR7ZRCHkN",
    "zone2_node_2": "bN7H1fmCvGYBClQTgL8Q",
    "zone2_node_3": "8BUFOLnkMTw5UmqLvVPJ",
    "zone2_node_4": "uWSRIYWQT3lh1Ofgc7zg",
    "zone2_node_5": "35KvcSt0sHudpb4yWPXM",
}


def checksum(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def publish_state(client, state, extra=None):
    payload = {"fw_state": state}
    if extra:
        payload.update(extra)
    client.publish("v1/devices/me/telemetry", json.dumps(payload), qos=1)
    client.loop(1)
    print(payload)


def run_device(device_name, token, fail=False):
    firmware_payload = json.dumps(
        {
            "title": "thresholds_v2",
            "version": "1.1.0",
            "zone": "Zone 2",
            "thresholds": {
                "moderate_humidity_min": 68,
                "high_humidity_min": 82,
                "high_temperature_min": 17,
                "high_temperature_max": 26,
                "critical_leaf_wetness_min": 7,
                "critical_rainfall_24h_min": 4,
            },
        },
        sort_keys=True,
    )

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=device_name)
    client.username_pw_set(token)
    client.connect(TB_HOST, TB_PORT, 60)

    meta = {
        "fw_title": "thresholds_v2",
        "fw_version": "1.1.0",
        "fw_size": len(firmware_payload),
        "fw_checksum": checksum(firmware_payload),
    }

    for state in ["DOWNLOADING", "DOWNLOADED", "VERIFIED", "UPDATING"]:
        publish_state(client, state, meta)
        time.sleep(1)

    if fail:
        publish_state(client, "FAILED", {"fw_version": "1.1.0", "failure_reason": "simulated checksum error"})
    else:
        publish_state(client, "UPDATED", {"fw_version": "1.1.0"})

    client.disconnect()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="zone2_node_1", choices=sorted(TOKENS))
    parser.add_argument("--fail", action="store_true")
    args = parser.parse_args()
    run_device(args.device, TOKENS[args.device], args.fail)


if __name__ == "__main__":
    main()
