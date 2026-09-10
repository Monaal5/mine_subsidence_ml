/*
 * Auto-generated scaler parameters for Mine Subsidence Edge Model
 * DO NOT EDIT — regenerate by running train_edge_model.py
 */

#ifndef SCALER_PARAMS_H
#define SCALER_PARAMS_H

#define NUM_FEATURES 8
#define ANOMALY_THRESHOLD -0.61267743f

// Feature names (for reference):
// [0] tilt_mean
// [1] tilt_rate
// [2] strain_delta
// [3] vib_rms
// [4] vib_peak
// [5] vib_dominant_freq
// [6] crack_status
// [7] temp_humidity_index

static const float SCALER_MEAN[NUM_FEATURES] = {
    0.02316141f,
    -0.00000835f,
    -0.00092911f,
    0.02507824f,
    0.05643067f,
    13.01281043f,
    1.00000000f,
    0.53166621f
};

static const float SCALER_SCALE[NUM_FEATURES] = {
    0.01188383f,
    0.01581167f,
    0.87501164f,
    0.00989571f,
    0.02514626f,
    2.87522316f,
    1.00000000f,
    0.19632400f
};

// Apply standard scaling: scaled[i] = (raw[i] - mean[i]) / scale[i]
static inline void scale_features(const float* raw, float* scaled) {
    for (int i = 0; i < NUM_FEATURES; i++) {
        scaled[i] = (raw[i] - SCALER_MEAN[i]) / SCALER_SCALE[i];
    }
}

#endif // SCALER_PARAMS_H
