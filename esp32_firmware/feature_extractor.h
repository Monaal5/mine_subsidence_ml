/*
 * feature_extractor.h — Feature Vector Generation from Raw Sensors
 * Computes the 8 feature elements required by the TinyML Isolation Forest model.
 */

#ifndef FEATURE_EXTRACTOR_H
#define FEATURE_EXTRACTOR_H

#include <math.h>

struct RawSensorReadings {
    float tilt_x_deg;
    float tilt_y_deg;
    float strain_delta_ue;
    float vib_rms_g;
    float vib_peak_g;
    float vib_dominant_freq_hz;
    int crack_status;       // 1 = intact, 0 = broken
    float temperature_c;
    float humidity_pct;
    float pressure_hpa;
};

struct FeatureVector {
    float features[8];
    // Index mapping:
    // [0] tilt_mean
    // [1] tilt_rate
    // [2] strain_delta
    // [3] vib_rms
    // [4] vib_peak
    // [5] vib_dominant_freq
    // [6] crack_status
    // [7] temp_humidity_index
};

static float last_tilt_magnitude = 0.0f;

static inline FeatureVector extract_features(const RawSensorReadings& raw) {
    FeatureVector fv;
    
    // 1. Tilt Mean Magnitude (sqrt(x^2 + y^2))
    float tilt_mag = sqrtf(raw.tilt_x_deg * raw.tilt_x_deg + raw.tilt_y_deg * raw.tilt_y_deg);
    fv.features[0] = tilt_mag;
    
    // 2. Tilt Rate (delta since last window)
    fv.features[1] = tilt_mag - last_tilt_magnitude;
    last_tilt_magnitude = tilt_mag;
    
    // 3. Strain Delta
    fv.features[2] = raw.strain_delta_ue;
    
    // 4. Vibration RMS
    fv.features[3] = raw.vib_rms_g;
    
    // 5. Vibration Peak
    fv.features[4] = raw.vib_peak_g;
    
    // 6. Vibration Dominant Frequency
    fv.features[5] = raw.vib_dominant_freq_hz;
    
    // 7. Crack Status
    fv.features[6] = (float)raw.crack_status;
    
    // 8. Temp-Humidity Combined Index
    float temp_norm = (raw.temperature_c - 20.0f) / 25.0f;
    float hum_norm = (raw.humidity_pct - 35.0f) / 65.0f;
    fv.features[7] = 0.5f * temp_norm + 0.5f * hum_norm;
    
    return fv;
}

#endif // FEATURE_EXTRACTOR_H
