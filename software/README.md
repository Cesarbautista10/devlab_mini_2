# Software Documentation

This directory contains comprehensive software components for the ICP-10111 Barometric Pressure Sensor development ecosystem, including professional documentation generation tools, cross-platform code examples, and development utilities.

## Overview

This software package provides comprehensive development tools and examples for integrating the ICP-10111 Barometric Pressure Sensor into embedded systems and IoT applications. The package includes cross-platform libraries, example implementations, and professional documentation generation tools.

### Key Features

- **Cross-Platform Support**: Linux, embedded RTOS, and microcontroller compatibility
- **Multiple Languages**: C (embedded systems) and Python (high-level applications)  
- **Real-time Processing**: Sub-millisecond measurement cycles with interrupt handling
- **Professional Documentation**: Automated LaTeX documentation generation
- **Production Ready**: Industrial-grade error handling and validation

## Supported Platforms

### Embedded Linux Systems
- **Raspberry Pi** (all models with I2C support)
- **BeagleBone Black/Green** 
- **NVIDIA Jetson** series
- **Orange Pi** and compatible SBCs
- **Industrial Linux** systems with I2C interface

### Microcontrollers
- **ESP32/ESP8266** (Arduino IDE and ESP-IDF)
- **STM32** series (HAL and LL drivers)
- **Arduino** compatible boards
- **PIC32** and other RTOS-based systems

## Software Architecture

### Core Components

**1. Device Communication Layer**
- **I2C Protocol Handler**: Low-level register access and bus management
- **Device Detection**: Automatic sensor discovery and capability detection
- **Error Recovery**: Robust error handling with automatic retry mechanisms
- **Power Management**: Software-controlled low-power modes

**2. Data Processing Engine**
- **Real-time Calculations**: Pressure and temperature conversion algorithms
- **Calibration Management**: Factory calibration data handling
- **Data Filtering**: Configurable digital filtering for noise reduction
- **Unit Conversion**: Automatic conversion between measurement units

**3. Application Interface**
- **High-level APIs**: Simplified sensor control functions
- **Event-driven Processing**: Interrupt-based measurement notifications
- **Data Logging**: Built-in logging capabilities with timestamp management
- **Configuration Management**: Runtime parameter adjustment

## Programming Examples

### C Language Implementation

**Target Applications**: Embedded systems, real-time applications, microcontrollers

**Features:**
- **ANSI C Compliance**: Compatible with embedded compilers
- **Minimal Dependencies**: Only standard I2C libraries required
- **Real-time Performance**: Optimized for sub-millisecond response times
- **Memory Efficient**: <2KB RAM footprint for complete implementation

**Core Functions:**
```c
int icp10111_init(int i2c_fd);                    
int icp10111_configure(uint8_t mode, uint8_t rate);

// Data acquisition functions  
int icp10111_read_pressure(float *pressure_hpa);      
int icp10111_read_temperature(float *temperature_c); 
int icp10111_read_both(sensor_data_t *data);

// Power management and control
int icp10111_set_power_mode(power_mode_t mode);
int icp10111_trigger_measurement(void);
```

**Hardware Requirements:**
- I2C bus enabled on host system
- `libi2c-dev` development library
- GCC compiler with C99 support
- 4.7kΩ pull-up resistors on SDA/SCL lines

**Usage Example:**
```c

#include "icp10111.h"

int main() {
    float pressure, temperature;
    int i2c_fd = open("/dev/i2c-1", O_RDWR);
    
    if (icp10111_init(i2c_fd) == 0) {
        icp10111_read_pressure(&pressure);
        icp10111_read_temperature(&temperature);
        printf("Pressure: %.2f hPa, Temperature: %.2f°C
", 
               pressure, temperature);
    }
    
    close(i2c_fd);
    return 0;
}
```

### Python Implementation

**Target Applications**: IoT systems, data logging, research applications, prototyping

**Features:**
- **Object-Oriented Design**: Clean, maintainable code structure
- **Type Hints**: Full type annotation for better code documentation  
- **Async Support**: Non-blocking I/O for concurrent applications
- **Data Analysis**: Integration with NumPy/Pandas for data processing
- **Logging Framework**: Comprehensive logging with configurable levels

**Core Classes:**
```python
class ICP10111Sensor:
    def __init__(self, bus_number: int = 1, address: int = 0x63)
    def read_pressure(self) -> float
    def read_temperature(self) -> float  
    def read_sensor_data(self) -> SensorData
    def configure_measurement(self, mode: MeasurementMode)
    def set_power_mode(self, mode: PowerMode)
```

**Dependencies:**
```bash
pip install smbus2      # I2C communication library
pip install numpy       # Numerical processing (optional)
pip install logging     # Enhanced logging (built-in)
```

**Usage Example:**
```python
from icp10111 import ICP10111Sensor
import time

# Initialize sensor
sensor = ICP10111Sensor(bus_number=1)

# Configure for continuous measurement
sensor.configure_measurement(mode='continuous', rate=10)  # 10 Hz

# Read data
while True:
    data = sensor.read_sensor_data()
    print(f"Pressure: {data.pressure:.2f} hPa")
    print(f"Temperature: {data.temperature:.2f}°C")
    time.sleep(1)
```

## Advanced Configuration

### I2C Settings
- **Default Bus**: `/dev/i2c-1` (Raspberry Pi)
- **ICP-10111 Address**: `0x63`
- **BME688 Address**: `0x77` (if present)
- **Clock Speed**: 100kHz (standard) / 400kHz (fast mode)

### Measurement Parameters
- **Pressure Range**: 300-1250 hPa
- **Pressure Resolution**: 0.01 hPa
- **Temperature Range**: -40°C to +85°C
- **Sample Rate**: 1 Hz (adjustable)

## 🛠️ Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   sudo usermod -a -G i2c $USER
   # Logout and login again
   ```

2. **I2C Device Not Found**
   ```bash
   # Check if I2C is enabled
   lsmod | grep i2c
   
   # Scan for devices
   i2cdetect -y 1
   ```

3. **Reading Errors**
   ```bash
   # Verify connections and pull-up resistors
   # Check power supply voltage (3.3V nominal)
   # Ensure proper grounding
   ```

### Performance Optimization

**For Real-time Applications:**
- Use dedicated I2C bus for sensor communication
- Enable I2C fast mode (400kHz) for faster data transfer
- Implement interrupt-driven data acquisition
- Use DMA for bulk data transfers

**For Low-Power Applications:**
- Configure sensor sleep mode between measurements
- Use triggered measurement mode instead of continuous
- Implement wake-on-interrupt functionality
- Optimize measurement intervals based on application needs

## Quick Start Guide

### 1. Hardware Connection

**Physical Wiring** (Raspberry Pi example):
```
ICP-10111 Module    →    Raspberry Pi 4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VCC (Pin 1)         →    3.3V (Pin 1)
GND (Pin 2)         →    GND (Pin 6) 
SDA (Pin 3)         →    GPIO 2/SDA (Pin 3)
SCL (Pin 4)         →    GPIO 3/SCL (Pin 5)
```

**Alternative: QWIIC Connection**
- Use SparkFun QWIIC cable (JST GH 1.25mm)
- Plug directly into QWIIC-compatible development board
- Daisy-chainable with other QWIIC modules

### 2. System Configuration (Raspberry Pi OS)

```bash
# Enable I2C interface
sudo raspi-config
# → Interface Options → I2C → Enable → Reboot

# Verify I2C kernel module
lsmod | grep i2c_dev

# Install development tools
sudo apt-get update
sudo apt-get install i2c-tools python3-pip build-essential libi2c-dev

# Configure I2C permissions (avoid sudo requirements)
sudo usermod -a -G i2c $USER
sudo reboot
```

### 3. Hardware Verification

```bash
# Scan I2C bus for connected devices
i2cdetect -y 1

# Expected devices:
# 0x63 = ICP-10111 Barometric Pressure Sensor
# 0x77 = BME688 Environmental Sensor (if populated)
```

### 4. Run Example Code

**C Implementation:**
```bash
cd software/examples/c/main/
gcc -O2 -Wall -std=c99 -o icp_sensor main.c -li2c
./icp_sensor
```

**Python Implementation:**
```bash
cd software/examples/py/main/
pip3 install --user smbus2
python3 main.py
```

## Expected Performance

### Typical Measurement Ranges

**At Sea Level (Standard Conditions):**
- **Pressure**: 1013.25 ± 30 hPa (29.92 ± 0.9 inHg)
- **Temperature**: Ambient ± sensor self-heating (~0.1°C)
- **Calculated Altitude**: 0 ± accuracy_margin

**Measurement Quality Indicators:**
```
✅ GOOD:     1000-1040 hPa, stable readings within ±0.1 hPa
⚠️  CAUTION: <1000 or >1040 hPa, check sensor placement/calibration  
❌ ERROR:    Readings outside 300-1250 hPa range, sensor malfunction
```

### Performance Specifications

| Parameter | C Implementation | Python Implementation |
|-----------|------------------|----------------------|
| **Measurement Rate** | Up to 100 Hz | Up to 50 Hz |
| **Startup Time** | <50ms | <200ms |
| **Memory Usage** | <2KB RAM | <50MB RAM |
| **Power Consumption** | <1.5mA | <1.8mA |

## Integration Guidelines

### Real-time Applications
- Use dedicated I2C bus for sensor communication
- Enable I2C fast mode (400kHz) for faster data transfer
- Implement interrupt-driven data acquisition
- Use DMA for bulk data transfers

### Low-Power Applications
- Configure sensor sleep mode between measurements
- Use triggered measurement mode instead of continuous
- Implement wake-on-interrupt functionality
- Optimize measurement intervals based on application needs
|-----------|---------|-------|-------------|
| **I2C Bus** | `/dev/i2c-1` | `/dev/i2c-0` to `/dev/i2c-2` | Raspberry Pi I2C interface |
| **Device Address** | `0x63` | Fixed | 7-bit I2C address |
| **Clock Speed** | `100 kHz` | `100/400/1000 kHz` | I2C communication speed |
| **Sampling Rate** | `1 Hz` | `0.1-100 Hz` | Measurement frequency |
| **Pressure Resolution** | `0.01 hPa` | Fixed | ADC resolution |
| **Operating Mode** | `Normal` | `Low Power/Normal/High Res` | Power vs accuracy trade-off |

### BME688 Environmental Sensor (Optional)

| Parameter | Default | Range | Function |
|-----------|---------|-------|----------|
| **I2C Address** | `0x77` | Fixed | Environmental co-processor |
| **Humidity Sampling** | `1x` | `0x-16x` | Oversampling rate |
| **Gas Sensor** | `Disabled` | `Enabled/Disabled` | VOC detection |
| **Filter Coefficient** | `0` | `0-127` | IIR filtering |

### Configuration Files

**C Configuration (`sensor_config.h`):**
```c
#define ICP10111_I2C_BUS        1
#define ICP10111_I2C_ADDR       0x63
#define ICP10111_SAMPLE_RATE    10      // Hz
#define ICP10111_FILTER_ENABLE  1
#define BME688_ENABLE           0       // Set to 1 if BME688 present
```

**Python Configuration (`config.yaml`):**
```yaml
sensor:
  i2c_bus: 1
  address: 0x63
  sampling_rate: 10.0  # Hz
  
data_logging:
  enable: true
  format: "csv"        # csv, json, binary
  filename: "pressure_data_{timestamp}.csv"
  
filtering:
  enable: true
  type: "moving_average"
  window_size: 10

environmental:
  bme688_enable: false
  humidity_oversampling: 1
  gas_sensor_enable: false
```

## 🛠️ Troubleshooting Guide

### Common Issues and Solutions

**1. 🚫 Permission Denied (EACCES)**
```bash
# Problem: I2C device access requires elevated privileges
# Solution A: Add user to i2c group (recommended)
sudo usermod -a -G i2c $USER
newgrp i2c  # Or logout/login

# Solution B: Use sudo (temporary fix)
sudo ./your_program

# Verification: Check group membership
groups $USER | grep i2c
```

**2. 🔍 I2C Device Not Found (ENODEV)**
```bash
# Problem: Sensor not detected on I2C bus
# Diagnosis: Scan for devices
i2cdetect -y 1

# Troubleshooting steps:
# 1. Check physical connections
# 2. Verify I2C is enabled
sudo raspi-config  # Interface Options → I2C → Enable

# 3. Check kernel modules
lsmod | grep i2c
# Expected: i2c_dev, i2c_bcm2835

# 4. Try different I2C bus
i2cdetect -y 0  # Some boards use bus 0
```

**3. ⚡ Compilation Errors (C/C++)**
```bash
# Problem: Missing development headers/libraries
# Solution: Install complete development environment
sudo apt-get update
sudo apt-get install build-essential libi2c-dev linux-headers-$(uname -r)

# For cross-compilation (ARM embedded):
sudo apt-get install gcc-arm-linux-gnueabihf

# Verify installation:
pkg-config --exists libi2c-dev && echo "libi2c-dev: OK"
```

**4. 🐍 Python Import Errors**
```bash
# Problem: Missing Python modules
# Solution A: Install via pip (recommended)
pip3 install smbus2 numpy pyyaml

# Solution B: Use system packages
sudo apt-get install python3-smbus python3-numpy python3-yaml

# For virtual environments:
python3 -m venv sensor_env
source sensor_env/bin/activate
pip install -r requirements.txt
```

**5. 📊 Unrealistic Readings**

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Pressure > 1250 hPa | Sensor malfunction | Check power supply, replace sensor |
| Pressure < 300 hPa | I2C communication error | Verify connections, check pullups |
| High noise (>1 hPa) | EMI interference | Add filtering, shield cables |
| Temperature drift | Self-heating | Reduce sampling rate, improve airflow |
| Zero readings | Initialization failure | Check sensor ID, reset sequence |

### Debug Mode and Logging

**Enable verbose logging in Python:**
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Output example:
# 2025-07-21 10:30:15,123 - icp10111 - DEBUG - I2C bus opened: /dev/i2c-1
# 2025-07-21 10:30:15,125 - icp10111 - DEBUG - Sensor ID read: 0x08
# 2025-07-21 10:30:15,130 - icp10111 - INFO - Calibration coefficients loaded
```

**C debugging with detailed error messages:**
```c
#define DEBUG_ENABLED 1

#if DEBUG_ENABLED
    #define DEBUG_PRINT(fmt, ...) \
        fprintf(stderr, "[DEBUG] %s:%d: " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)
#else
    #define DEBUG_PRINT(fmt, ...)
#endif
```

### Performance Optimization

**High-frequency sampling (>10 Hz):**
- Use burst read mode for multiple samples
- Implement interrupt-driven data collection
- Consider DMA for sustained high throughput
- Monitor I2C bus utilization

**Low-power applications:**
- Configure sensor sleep mode between readings
- Use timer-based wake-up
- Implement adaptive sampling rates
- Monitor current consumption

## Additional Resources

### Technical Documentation
- ICP-10111 sensor datasheet and register map
- I2C communication protocol specifications  
- Platform-specific integration guides
- Application notes for specialized use cases

### Development Tools
- Logic analyzer captures for I2C debugging
- Oscilloscope waveforms for signal integrity
- Power consumption measurement guidelines
- Environmental testing procedures
