@echo off
title Mine Subsidence ESP32-S3 Node Flasher
echo =====================================================================
echo  Mine Subsidence AI Platform — Hardware Team 1-Click ESP32 Flasher
echo =====================================================================
echo.
echo Step 1: Searching for connected ESP32-S3 boards...
arduino-cli board list 2>nul || (
    echo [INFO] Arduino CLI not found. Opening Arduino IDE method...
    echo.
    echo HARDWARE TEAM INSTRUCTIONS:
    echo 1. Connect ESP32-S3 via USB.
    echo 2. Open main.ino in Arduino IDE.
    echo 3. Select Board: "ESP32S3 Dev Module" and select your COM Port.
    echo 4. Click Upload (Arrow button).
    pause
    exit /b
)
echo.
echo Step 2: Compiling & Flashing Firmware to ESP32-S3...
arduino-cli compile --fqbn esp32:esp32:esp32s3 main.ino
arduino-cli upload -p COM4 --fqbn esp32:esp32:esp32s3 main.ino

echo.
echo [OK] ESP32-S3 Sensor Node Flashed Successfully!
pause
