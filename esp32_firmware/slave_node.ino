/*
 * slave_node.ino — Reference Slave ESP32 Node Firmware (SIH26)
 * Reads MPU6050 (0x69), ADXL345 (0x53), DS3231 RTC, applies pre-filter rules,
 * and transmits packed SensorPayload to Master Gateway via ESP-NOW.
 */

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_ADXL345_U.h>
#include "RTClib.h"
#include <esp_now.h>
#include <esp_wifi.h>
#include <WiFi.h>
#include "shared_payload.h"

// WiFi Credentials (same as phone hotspot)
const char* WIFI_SSID     = "YOUR_PHONE_HOTSPOT_SSID";
const char* WIFI_PASSWORD = "YOUR_HOTSPOT_PASSWORD";

// Master Gateway MAC Address (Replace with your Master's actual MAC address from Serial log)
uint8_t masterAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// Sensor Instances
Adafruit_MPU6050 mpu;
Adafruit_ADXL345_Unified adxl = Adafruit_ADXL345_Unified(12345);
RTC_DS3231 rtc;

SensorPayload myData;
esp_now_peer_info_t peerInfo;

void setup() {
    Serial.begin(115200);
    Wire.begin(21, 22);
    
    Serial.println("==================================================");
    Serial.println("SIH26 Mine Subsidence — Slave Node (ESP-NOW)");
    Serial.println("==================================================");

    // 1. Init MPU6050 at custom address 0x69 (AD0 tied to 3.3V)
    if (!mpu.begin(0x69)) {
        Serial.println("[ERROR] MPU6050 failed at 0x69");
    } else {
        Serial.println("[OK] MPU6050 initialized at 0x69");
    }

    // 2. Init ADXL345 at 0x53
    if (!adxl.begin(0x53)) {
        Serial.println("[ERROR] ADXL345 failed at 0x53");
    } else {
        Serial.println("[OK] ADXL345 initialized at 0x53");
    }

    // 3. Init RTC
    if (!rtc.begin()) {
        Serial.println("[ERROR] DS3231 RTC failed");
    } else {
        Serial.println("[OK] DS3231 RTC initialized");
    }

    // 4. Connect to WiFi to auto-align channel with Master Gateway
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to phone hotspot for channel sync");
    int retry = 0;
    while (WiFi.status() != WL_CONNECTED && retry < 20) {
        delay(300);
        Serial.print(".");
        retry++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.printf("\n[OK] WiFi Connected. Channel: %d | MAC: %s\n", WiFi.channel(), WiFi.macAddress().c_str());
    } else {
        Serial.println("\n[WARN] WiFi Connect timeout — proceeding with default channel");
    }

    // 5. Init ESP-NOW
    if (esp_now_init() != ESP_OK) {
        Serial.println("[ERROR] ESP-NOW Init Failed");
        return;
    }
    
    memcpy(peerInfo.peer_addr, masterAddress, 6);
    peerInfo.channel = 0; // Use current WiFi channel
    peerInfo.encrypt = false;

    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
        Serial.println("[WARN] Peer registration check (ensure master MAC is set)");
    }

    // Default Node Configuration
    myData.node_id = 1;
    myData.lat = 30.7588;  // Hardcoded fixed GPS fallback coordinates
    myData.lng = 76.7685;
}

void loop() {
    // --- A. READ MPU6050 ---
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    
    // Pitch and Roll Calculation (deg)
    float pitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * 180.0 / M_PI;
    float roll  = atan2(a.acceleration.y, a.acceleration.z) * 180.0 / M_PI;
    
    // MPU Vibration RMS Vector Magnitude
    float mpu_total = sqrt(a.acceleration.x * a.acceleration.x + 
                           a.acceleration.y * a.acceleration.y + 
                           a.acceleration.z * a.acceleration.z);
    float mpu_vib_rms = abs(mpu_total - 9.81);
    if (mpu_vib_rms < 0.25) mpu_vib_rms = 0.00; // Noise suppression threshold

    // --- B. READ ADXL345 ---
    sensors_event_t adxl_evt;
    adxl.getEvent(&adxl_evt);
    
    // ADXL Vibration RMS Calculation
    float adxl_total = sqrt(adxl_evt.acceleration.x * adxl_evt.acceleration.x + 
                            adxl_evt.acceleration.y * adxl_evt.acceleration.y + 
                            adxl_evt.acceleration.z * adxl_evt.acceleration.z);
    float adxl_vib_rms = abs(adxl_total - 9.81);
    if (adxl_vib_rms < 0.25) adxl_vib_rms = 0.00; // Noise suppression threshold

    // --- C. READ TIME ---
    DateTime now = rtc.now();

    // --- D. STAGE 1 ANOMALY PRE-FILTER RULE ---
    // Flagged if tilt magnitude > 3.5 deg OR vibration RMS > 1.8 m/s²
    bool anomaly = (abs(pitch) > 3.5 || abs(roll) > 3.5 || mpu_vib_rms > 1.8 || adxl_vib_rms > 1.8);

    // --- E. PACK DATA & TRANSMIT OVER ESP-NOW ---
    myData.timestamp = now.unixtime();
    myData.pitch = pitch;
    myData.roll = roll;
    myData.mpu_vib_rms = mpu_vib_rms;
    myData.adxl_vib_rms = adxl_vib_rms;
    myData.stage1_anomaly_score = anomaly ? 1 : 0;

    esp_err_t result = esp_now_send(masterAddress, (uint8_t *) &myData, sizeof(myData));

    // --- F. SERIAL DIAGNOSTIC LOGGING ---
    Serial.println("--------------- SENSOR READOUT ---------------");
    Serial.printf("TIMESTAMP     : %04d-%02d-%02d %02d:%02d:%02d\n", 
                  now.year(), now.month(), now.day(), now.hour(), now.minute(), now.second());
    Serial.printf("TILT ANGLES   : Pitch: %6.2f deg  |  Roll: %6.2f deg\n", pitch, roll);
    Serial.printf("VIBRATION RMS : MPU: %5.2f m/s²   |  ADXL: %5.2f m/s²\n", mpu_vib_rms, adxl_vib_rms);
    Serial.printf("STAGE 1 SCORE : [%d] -> %s\n", myData.stage1_anomaly_score, anomaly ? "*** ANOMALY ***" : "NORMAL");
    Serial.printf("ESP-NOW SEND  : %s\n", result == ESP_OK ? "SUCCESS" : "FAIL");
    Serial.println("----------------------------------------------\n");

    delay(1000);
}
