/*
 * anomaly_detector.h — TinyML Isolation Forest Anomaly Scoring on ESP32-S3
 * Wrapper integrating scaler_params.h and emlearn model header.
 */

#ifndef ANOMALY_DETECTOR_H
#define ANOMALY_DETECTOR_H

#include "scaler_params.h"
#include "isolation_forest_model.h"

struct InferenceResult {
    float anomaly_score;
    bool is_anomalous;
    unsigned long execution_time_us;
};

static inline InferenceResult predict_anomaly(const float raw_features[NUM_FEATURES]) {
    InferenceResult res;
    
    float scaled[NUM_FEATURES];
    scale_features(raw_features, scaled);
    
    unsigned long start_time = micros();
    
    // Call inline inference function (returns float normalized anomaly score)
    float score = subsidence_detector_predict(scaled, NUM_FEATURES);
    
    res.anomaly_score = score;
    res.is_anomalous = (res.anomaly_score < ANOMALY_THRESHOLD);
    
    res.execution_time_us = micros() - start_time;
    
    return res;
}

#endif // ANOMALY_DETECTOR_H
