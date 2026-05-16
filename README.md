# Crop Disease Early Warning Network - ThingsBoard Edition

This project demonstrates a simulated LoRaWAN crop disease early warning network using ChirpStack, ThingsBoard CE, MQTT telemetry, rule-based disease risk scoring, OTA firmware update reporting, and a rogue-device security test.

## Components

- `docker-compose.yml`: ThingsBoard CE with PostgreSQL.
- `chirpstack/docker-compose.yml`: ChirpStack v4 stack with PostgreSQL, Redis, and Mosquitto.
- `src/seeded_multi_simulator.py`: Sends reproducible telemetry for 10 nodes across Zone 1 and Zone 2.
- `src/ota_device_simulator.py`: Simulates ThingsBoard OTA state transitions for Zone 2 devices.
- `src/attack_simulator.py`: Attempts to connect with an invalid token and publish false telemetry.
- `thingsboard/uplink_data_converter.js`: MQTT Integration uplink converter for ChirpStack JSON.
- `thingsboard/risk_engine_script.js`: Rule Chain transformation script for `risk_level`.
- `thingsboard/rollback_rule_chain_notes.md`: Rollback branch documentation.
- `ota_payload/thresholds_v2_config.json`: OTA firmware payload configuration for Zone 2 threshold update.

## Ports

- ThingsBoard UI: `http://localhost:8085`
- ThingsBoard MQTT: `localhost:1884`
- ChirpStack UI: `http://localhost:8080`
- ChirpStack Mosquitto: `localhost:1885`

## Setup

Start ThingsBoard:

```powershell
docker compose up -d
```

Start ChirpStack:

```powershell
cd .\chirpstack
docker compose up -d
```

Install Python dependencies:

```powershell
py -3 -m pip install paho-mqtt requests
```

## ThingsBoard Configuration Checklist

1. Create two device profiles: `Zone1_Sensor` and `Zone2_Sensor`.
2. Create 10 devices:
   - `zone1_node_1` to `zone1_node_5` under `Zone1_Sensor`.
   - `zone2_node_1` to `zone2_node_5` under `Zone2_Sensor`.
3. Assign each device the access token used in `src/seeded_multi_simulator.py`.
4. Create an MQTT Integration subscribed to:

```text
application/+/device/+/event/up
```

5. Paste `thingsboard/uplink_data_converter.js` as the uplink converter.
6. Create a Rule Chain named `Disease Risk Engine`.
7. Add a transformation script node using `thingsboard/risk_engine_script.js`.
8. Add Save Timeseries and Save Attributes nodes for:

```text
temperature, humidity, leaf_wetness, rainfall, risk_level
```

9. Add alarm or notification nodes for `HIGH` and `CRITICAL`.
10. Build a dashboard with:
    - Current risk level per zone.
    - Temperature/humidity time-series chart.
    - Rainfall bar chart.
    - Alert/alarm history.

## Run Telemetry Simulation

The simulator is deterministic because it uses a fixed seed. It starts with normal data, then humidity buildup, then high-risk and rainfall conditions.

```powershell
py -3 .\src\seeded_multi_simulator.py --interval 10 --cycles 18 --seed 453
```

For assignment timing, explain that each simulator cycle represents one 5-minute telemetry interval.

## OTA Demo

Create an OTA firmware package in ThingsBoard:

- Type: Firmware
- Title: `thresholds_v2`
- Version: `1.1.0`
- Device Profile: `Zone2_Sensor`
- Payload: ZIP containing `ota_payload/thresholds_v2_config.json`

Simulate a successful device update:

```powershell
py -3 .\src\ota_device_simulator.py --device zone2_node_1
```

Simulate rollback trigger with two failed Zone 2 devices:

```powershell
py -3 .\src\ota_device_simulator.py --device zone2_node_1 --fail
py -3 .\src\ota_device_simulator.py --device zone2_node_2 --fail
```

Document the rollback branch using `thingsboard/rollback_rule_chain_notes.md`.

## Security Demo

Run the rogue device test:

```powershell
py -3 .\src\attack_simulator.py
```

Expected result:

```text
CONNECT result: Not authorized
Security test passed: rogue device was rejected by ThingsBoard
```

Screenshots to include:

- ThingsBoard device credentials or X.509 setup.
- MQTT client rejection output.
- ThingsBoard logs/audit event if available.
- Device Profile alarm rules for offline, telemetry flooding, and impossible sensor values.

## Submission ZIP Checklist

Include:

- Python scripts from `src/`.
- Docker Compose files.
- ChirpStack config files.
- ThingsBoard converter script.
- Exported Rule Chain JSON.
- Exported Dashboard JSON.
- Exported Device Profile JSON.
- OTA payload config.
- Screenshots folder.
- Final report PDF.

Do not submit production credentials or real JWT tokens.
