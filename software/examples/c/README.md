# ICP-10111 Barometric Pressure Sensor - C Examples

This directory contains C code examples for interfacing with the ICP-10111 Barometric Pressure Sensor module.

## Examples

### Basic I2C Communication
- `basic_reading.c` - Simple pressure and temperature reading
- `continuous_monitoring.c` - Continuous sensor data acquisition
- `low_power_mode.c` - Power management and sleep mode operation

### Advanced Examples
- `calibration.c` - Sensor calibration routines
- `data_logging.c` - Data logging with timestamp
- `multi_sensor.c` - Managing multiple sensors on the same I2C bus

## Build Instructions

```bash
gcc -o sensor_example basic_reading.c -li2c
```

## Dependencies

- Linux I2C development library (`libi2c-dev`)
- Standard C library

## Hardware Requirements

- ICP-10111 Barometric Pressure Sensor module
- I2C capable development board (Raspberry Pi, Arduino, etc.)
- Pull-up resistors (if not integrated on module)

## I2C Configuration

```c
#define ICP10111_I2C_ADDR    0x63
#define BME688_I2C_ADDR      0x77
#define I2C_BUS              "/dev/i2c-1"
```
