// ThingsBoard transformation script node.
// Saves risk_level as telemetry and can also be followed by a Create Alarm node.

var temperature = Number(msg.temperature);
var humidity = Number(msg.humidity);
var leafWetness = Number(msg.leaf_wetness);
var rainfall = Number(msg.rainfall);

var risk = "LOW";

if (humidity > 85 && temperature >= 18 && temperature <= 25 && leafWetness > 8 && rainfall > 5) {
    risk = "CRITICAL";
} else if (humidity > 85 && temperature >= 18 && temperature <= 25) {
    risk = "HIGH";
} else if (humidity >= 70 && humidity <= 85 && temperature >= 15 && temperature <= 25) {
    risk = "MODERATE";
}

msg.risk_level = risk;
metadata.risk_level = risk;

return {msg: msg, metadata: metadata, msgType: msgType};
