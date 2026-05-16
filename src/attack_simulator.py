import argparse
import json

import paho.mqtt.client as mqtt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=1884)
    parser.add_argument("--token", default="wrong_or_unauthorized_token")
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="rogue_node")
    client.username_pw_set(args.token)

    reason = {"code": None, "text": ""}

    def on_connect(_client, _userdata, _flags, reason_code, _properties):
        reason["code"] = int(reason_code)
        reason["text"] = str(reason_code)
        print(f"CONNECT result: {reason['text']}")
        if int(reason_code) == 0:
            payload = {
                "temperature": 22.0,
                "humidity": 99.0,
                "leaf_wetness": 12.0,
                "rainfall": 20.0,
                "risk_level": "CRITICAL",
            }
            _client.publish("v1/devices/me/telemetry", json.dumps(payload), qos=1)
            print("Unexpected: rogue telemetry was published")

    client.on_connect = on_connect
    client.connect(args.host, args.port, 60)
    client.loop_start()
    import time

    time.sleep(3)
    client.loop_stop()
    client.disconnect()

    if reason["code"] == 0:
        raise SystemExit("Security test failed: rogue device connected")
    print("Security test passed: rogue device was rejected by ThingsBoard")


if __name__ == "__main__":
    main()
