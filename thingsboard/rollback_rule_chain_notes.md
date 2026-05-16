# Rollback Rule Chain Branch

Use this as the documented rollback logic for the OTA section.

1. Start from the root rule chain or a dedicated `OTA Rollback Monitor` rule chain.
2. Add an `Originator fields` node and fetch `deviceProfileName` and `name`.
3. Add a script filter node named `Zone2 firmware failed`.

```javascript
return msg.fw_state === "FAILED"
    && metadata.deviceProfileName === "Zone2_Sensor"
    && msg.fw_version === "1.1.0";
```

4. Add an `Aggregate latest` or `Count` node grouped by `fw_version` over the last 10 minutes.
5. Add a script filter named `Two failures reached`.

```javascript
return Number(msg.failed_count || msg.count || 0) >= 2;
```

6. Add a REST API Call node. Use a tenant administrator JWT in a demo-only environment and call the ThingsBoard REST API to update the `Zone2_Sensor` device profile firmware assignment back to the previous package.
7. Follow it with a `Create alarm` node:

```text
Alarm type: OTA_ROLLBACK_TRIGGERED
Severity: CRITICAL
Details: thresholds_v2 1.1.0 failed on two or more Zone 2 devices, previous firmware reassigned.
```

For the demo, run:

```powershell
py -3 .\src\ota_device_simulator.py --device zone2_node_1 --fail
py -3 .\src\ota_device_simulator.py --device zone2_node_2 --fail
```

The dashboard/alarm widget should then show the rollback alarm.
