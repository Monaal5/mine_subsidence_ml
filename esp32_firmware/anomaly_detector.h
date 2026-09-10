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
    
    // Call emlearn generated inline inference function
    int pred_class = subsidence_detector_predict(scaled, NUM_FEATURES);
    
    // In emlearn Isolation Forest, scores < 0 or class -1 indicate outliers
    res.anomaly_score = (float)pred_class;
    res.is_anomalous = (pred_class < 0) || (res.anomaly_score < ANOMALY_THRESHOLD);
    
    res.execution_time_us = micros() - start_time;
    
    return res;
}

#endif // ANOMALY_DETECTOR_H
