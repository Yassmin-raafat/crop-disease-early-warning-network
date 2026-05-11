# Crop Disease Early Warning Network

## Overview
IoT-based crop disease monitoring system using ThingsBoard.

## Features
- 10 simulated sensor nodes
- 2 agricultural zones
- Disease risk prediction
- ThingsBoard Rule Engine
- OTA firmware simulation
- Alarm generation
- Real-time dashboard

## Technologies
- Python
- Docker
- ThingsBoard CE

## Setup

### Start ThingsBoard
docker compose up -d

### Run Simulator
python multi_simulator.py

## Ports
- 8085 → ThingsBoard UI
- 1884 → MQTT

## Telemetry Keys
- temperature
- humidity
- rainfall
- leaf_wetness
- risk_level
- fw_state
