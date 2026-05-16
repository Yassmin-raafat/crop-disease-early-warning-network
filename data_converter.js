// ThingsBoard Data Converter for ChirpStack MQTT Integration
// Decodes ChirpStack JSON payload into ThingsBoard telemetry

/** Decoder function */
function decodePayload(payload) {
    var data = JSON.parse(payload);

    return {
        deviceName: data.devEUI,
        deviceType: "LoRaWAN_Sensor",
        telemetry: {
            temperature: data.object.temperature,
            humidity: data.object.humidity,
            leaf_wetness: data.object.leaf_wetness,
            rainfall: data.object.rainfall
        },
        attributes: {
            zone: data.object.zone
        }
    };
}

// Decode the payload and return the result
decodePayload(payload);