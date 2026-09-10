/*
 * shared_payload.h — Shared Sensor Payload Contract for ESP32 Nodes (SIH26)
 * Byte-for-byte aligned payload structure shared between Slave Node & Master Gateway.
 */

#ifndef SHARED_PAYLOAD_H
#define SHARED_PAYLOAD_H

#include <stdint.h>

typedef struct __attribute__((packed)) {
    uint32_t node_id;               // Node ID (1 to 5)
    uint32_t timestamp;             // Unix timestamp from DS3231 RTC
    float pitch;                    // Pitch angle in degrees
    float roll;                     // Roll angle in degrees
    float mpu_vib_rms;              // Vibration RMS from MPU6050 (m/s²)
    float adxl_vib_rms;             // Vibration RMS from ADXL345 (m/s²)
    uint8_t stage1_anomaly_score;   // 1 = Anomaly / Alert, 0 = Normal
    double lat;                     // Latitude coordinate
    double lng;                     // Longitude coordinate
} SensorPayload;

#endif // SHARED_PAYLOAD_H
