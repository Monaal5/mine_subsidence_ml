/*
 * master_gateway.ino — Reference Master Gateway ESP32 Firmware (SIH26)
 * Receives SensorPayload over ESP-NOW from Slave Nodes,
 * prints its MAC address on boot, and forwards telemetry JSON via HTTPS POST
 * to the deployed FastAPI Dashboard endpoint (/api/ingest).
 */

#include <esp_now.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "shared_payload.h"

// Phone Hotspot WiFi Credentials
const char* WIFI_SSID     = "YOUR_PHONE_HOTSPOT_SSID";
const char* WIFI_PASSWORD = "YOUR_HOTSPOT_PASSWORD";

// Deployed FastAPI Dashboard Endpoint URL
const char* DASHBOARD_URL = "https://mine-subsidence-ml-2rr5.onrender.com/api/ingest";

SensorPayload lastPacket;
volatile bool newDataAvailable = false;

// ESP-NOW Receive Callback
void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *incomingData, int len) {
    if (len != sizeof(SensorPayload)) {
        Serial.printf("[WARN] Packet size mismatch: got %d bytes, expected %d bytes\n", len, (int)sizeof(SensorPayload));
        return;
    }
    memcpy(&lastPacket, incomingData, sizeof(lastPacket));
    newDataAvailable = true;
}

void forwardToDashboard(const SensorPayload &p) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[ERROR] WiFi disconnected — reconnecting...");
        WiFi.reconnect();
        return;
    }

    HTTPClient http;
    http.begin(DASHBOARD_URL);
    http.addHeader("Content-Type", "application/json");

    char jsonPayload[320];
    snprintf(jsonPayload, sizeof(jsonPayload),
        "{\"node_id\":%u,\"timestamp\":%u,\"pitch\":%.2f,\"roll\":%.2f,"
        "\"mpu_vib_rms\":%.2f,\"adxl_vib_rms\":%.2f,\"stage1_anomaly_score\":%u,"
        "\"lat\":%.6f,\"lng\":%.6f}",
        p.node_id, p.timestamp, p.pitch, p.roll,
        p.mpu_vib_rms, p.adxl_vib_rms, p.stage1_anomaly_score,
        p.lat, p.lng);

    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
        Serial.printf("[GATEWAY SUCCESS] POST to Dashboard -> Code %d\n", httpResponseCode);
    } else {
        Serial.printf("[GATEWAY ERROR] POST Failed -> %s\n", http.errorToString(httpResponseCode).c_str());
    }
    http.end();
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("==================================================");
    Serial.println("SIH26 Mine Subsidence — Master Gateway (WiFi + ESP-NOW)");
    Serial.println("==================================================");

    // 1. Connect to Phone Hotspot WiFi
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    Serial.print("Connecting to phone hotspot WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(400);
        Serial.print(".");
    }
    
    Serial.println("\n--------------------------------------------------");
    Serial.printf("[OK] WiFi Connected! Local IP: %s\n", WiFi.localIP().toString().c_str());
    Serial.printf("[CRITICAL] Master MAC Address: %s\n", WiFi.macAddress().c_str());
    Serial.printf("           (Copy this MAC into slave_node.ino masterAddress[])\n");
    Serial.printf("[INFO] WiFi Channel: %d\n", WiFi.channel());
    Serial.println("--------------------------------------------------");

    // 2. Initialize ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("[ERROR] ESP-NOW initialization failed");
        return;
    }
    
    // Register Receive Callback
    esp_now_register_recv_cb(onDataRecv);
    Serial.println("[OK] ESP-NOW Receive Callback registered. Listening for slave packets...\n");
}

void loop() {
    if (newDataAvailable) {
        newDataAvailable = false;
        
        Serial.println("==================================================");
        Serial.printf("[RX PACKET] Node ID: N%u | Timestamp: %u\n", lastPacket.node_id, lastPacket.timestamp);
        Serial.printf("  Pitch: %6.2f deg | Roll: %6.2f deg\n", lastPacket.pitch, lastPacket.roll);
        Serial.printf("  Vib (MPU/ADXL): %.2f / %.2f m/s²\n", lastPacket.mpu_vib_rms, lastPacket.adxl_vib_rms);
        Serial.printf("  Anomaly Score: [%u] -> %s\n", 
                      lastPacket.stage1_anomaly_score, 
                      lastPacket.stage1_anomaly_score ? "ALERT" : "NORMAL");
        Serial.println("--------------------------------------------------");
        
        // Forward Packet to Cloud Dashboard Endpoint
        forwardToDashboard(lastPacket);
        Serial.println("==================================================\n");
    }
    
    delay(10);
}
