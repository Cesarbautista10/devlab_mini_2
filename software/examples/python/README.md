# ICP-10111 Barometric Pressure Sensor - Python Examples

This directory contains Python code examples for interfacing with the ICP-10111 Barometric Pressure Sensor module.

## Examples

### Basic Usage
- `basic_reading.py` - Simple pressure and temperature reading
- `continuous_monitoring.py` - Continuous sensor data acquisition with plotting
- `data_logger.py` - CSV data logging with timestamps

### Advanced Examples
- `web_server.py` - Real-time web interface for sensor data
- `mqtt_publisher.py` - MQTT data publishing for IoT applications
- `altitude_calculator.py` - Altitude calculation from pressure readings

## Installation

```bash
pip install -r requirements.txt
```

## Dependencies

Create a `requirements.txt` file with:
```
smbus2
numpy
matplotlib
paho-mqtt
flask
```

## Quick Start

```python
import smbus2
import time

# I2C configuration
I2C_BUS = 1
ICP10111_ADDR = 0x63

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

# Read sensor data
def read_pressure():
    # Implementation here
    pass

# Example usage
while True:
    pressure = read_pressure()
    print(f"Pressure: {pressure} hPa")
    time.sleep(1)
```

## Hardware Requirements

- ICP-10111 Barometric Pressure Sensor module
- Raspberry Pi or similar I2C capable device
- Python 3.6+

## I2C Configuration

```python
ICP10111_I2C_ADDR = 0x63
BME688_I2C_ADDR = 0x77
I2C_BUS = 1  # Usually /dev/i2c-1 on Raspberry Pi
```
