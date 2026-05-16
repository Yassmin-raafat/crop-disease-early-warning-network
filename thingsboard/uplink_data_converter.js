// ThingsBoard MQTT Integration uplink converter for ChirpStack v4 JSON.
// Topic pattern: application/+/device/+/event/up

var data = JSON.parse(payload);
var object = data.object || data.decodedData || {};

var deviceName = data.deviceInfo && data.deviceInfo.deviceName
    ? data.deviceInfo.deviceName
    : (data.devEUI || data.devEui || metadata.deviceName);

var zone = object.zone || (deviceName.indexOf("zone2") === 0 ? "Zone 2" : "Zone 1");

var result = {
    deviceName: deviceName,
    deviceType: zone === "Zone 2" ? "Zone2_Sensor" : "Zone1_Sensor",
    attributes: {
        zone: zone,
        devEui: data.devEUI || data.devEui || ""
    },
    telemetry: {
        temperature: Number(object.temperature),
        humidity: Number(object.humidity),
        leaf_wetness: Number(object.leaf_wetness),
        rainfall: Number(object.rainfall)
    }
};

return result;
