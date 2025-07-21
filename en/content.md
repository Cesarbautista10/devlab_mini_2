# SCOPE AND PURPOSE

## Document Scope

This technical datasheet provides comprehensive specifications, electrical characteristics, mechanical dimensions, and application guidelines for the ICP-10111 Barometric Pressure Sensor module. This document is intended for design engineers, system integrators, and technical personnel involved in the development and integration of environmental sensing solutions.

## Product Overview

The ICP-10111 Barometric Pressure Sensor module is a compact embedded sensor with integrated environmental monitoring capabilities, designed for IoT applications and precise atmospheric measurements. The module combines high-accuracy pressure sensing with auxiliary environmental monitoring capabilities in a compact, easy-to-integrate form factor.

## Key Features

- **ICP-10111 Pressure Sensor** - High precision barometric pressure measurement
- **BME688 Environmental Sensor** - Temperature, humidity, and gas sensing capabilities  
- **Low Power Consumption** - Optimized for battery-powered applications
- **I2C/QWIIC Connectivity** - Standard digital interface with plug-and-play connector
- **Compact Form Factor** - PCB with castellated holes for flexible mounting options
- **Industrial Temperature Range** - -40°C to +85°C operation
- **RoHS Compliant** - Lead-free manufacturing process

# TECHNICAL SPECIFICATIONS

## Absolute Maximum Ratings

**Table 1: Absolute Maximum Ratings**

| Parameter | Symbol | Min | Max | Unit | Notes |
|-----------|--------|-----|-----|------|-------|
| Supply Voltage | VDD | -0.3 | 6.0 | V | Beyond operating range |
| Storage Temperature | TSTG | -55 | +125 | °C | Non-operating |
| Pressure Range (Absolute) | PABS | 0 | 1500 | hPa | Mechanical limit |

**WARNING:** Stresses beyond those listed under "Absolute Maximum Ratings" may cause permanent damage to the device. Exposure to absolute maximum rating conditions for extended periods may affect device reliability.

## Recommended Operating Conditions

### Sensor Specifications

**Table 2: Sensor Performance Specifications**

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| Pressure Range | 300-1250 | hPa | Absolute pressure |
| Pressure Accuracy | ±0.4 | hPa | At 25°C |
| Temperature Range | -40 to +85 | °C | Operating range |
| Humidity Range | 0-100 | %RH | Relative humidity |
| Interface | I2C | - | QWIIC compatible |

### Power Specifications

**Table 3: Electrical Characteristics**

| Parameter | Min | Typ | Max | Unit | Conditions |
|-----------|-----|-----|-----|------|------------|
| Supply Voltage | 3.0 | 3.3 | 5.0 | V | Normal Operation |
| Active Current | - | 1.2 | 2.0 | mA | Continuous measurement |
| Sleep Current | - | 0.1 | 0.5 | µA | Standby mode |
| Regulator Output | - | 1.8 | - | V | Internal LDO |

## Pinout

![Pinout Diagram](resources/unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.jpg)

**Table 4: Pin Configuration**

| Pin Label | Function    | Notes                             |
|-----------|-------------|-----------------------------------|
| VCC       | Power Supply| 3.3V or 5V                       |
| GND       | Ground      | Common ground for all components  |
| SDA       | I2C Data    | Serial data line                  |
| SCL       | I2C Clock   | Serial clock line                 |

## Dimensions

![Dimensions](resources/unit_dimension_v_1_0_0_icp10111_barometric_pressure_sensor.png)

## Topology

![Topology](resources/unit_topology_v_1_0_0_icp10111_barometric_pressure_sensor.png)

**Table 5: Component Reference**

| Ref. | Description                              |
|------|------------------------------------------|
| IC1  | ICP-10111 Barometric Pressure Sensor    |
| IC2  | BME688 Environmental Sensor             |
| L1   | Power On LED                             |
| U1   | ME6206A18XG 1.8V Regulator              | 
| JP1  | 2.54 mm Castellated Holes               |
| J1   | QWIIC Connector (JST 1 mm pitch) for I2C |


## Communication Interfaces

### I2C Interface
- **Address**: 0x63 (ICP-10111), 0x77 (BME688)
- **Speed**: Standard (100 kHz), Fast (400 kHz)
- **Features**: QWIIC compatible connector
- **Pull-up Resistors**: 4.7kΩ integrated

### Digital Interface Specifications
- **Logic Levels**: 3.3V CMOS compatible
- **Input High**: 2.0V minimum
- **Input Low**: 0.8V maximum
- **Output Drive**: 4mA typical

## Physical Characteristics

### Package Information

**Table 6: Physical Dimensions**

| Parameter | Value | Unit |
|-----------|-------|------|
| Package Type | Custom PCB | - |
| Dimensions | 25.4 x 15.24 x 3.2 | mm |
| Mounting | Castellated holes | 2.54mm pitch |
| Weight | 2.1 | g |

### Environmental Specifications

**Table 7: Environmental Operating Conditions**

| Parameter | Min | Max | Unit | Conditions |
|-----------|-----|-----|------|------------|
| Operating Temperature | -40 | +85 | °C | Full accuracy |
| Storage Temperature | -55 | +125 | °C | - |
| Humidity | 0 | 100 | %RH | Non-condensing |
| Pressure Range | 300 | 1250 | hPa | Absolute pressure |

## Software Support

### Development Environment
- **Arduino IDE**: Full library support
- **ESP-IDF**: Native driver integration
- **PlatformIO**: Cross-platform support
- **CircuitPython**: Python library available

### Key Libraries
- ICP-10111 pressure sensor driver
- BME688 environmental sensor library
- I2C communication protocols
- Data filtering and calibration

## Applications

The ICP-10111 module is ideal for:

1. **Weather Monitoring**
   - Atmospheric pressure measurement
   - Altitude determination
   - Weather prediction systems

2. **IoT Environmental Sensing**
   - Smart building automation
   - Agricultural monitoring
   - Air quality assessment

3. **Portable Devices**
   - Fitness trackers
   - Outdoor navigation devices
   - Drone altitude control

## Safety and Compliance

### Certifications
- **RoHS**: Compliant with EU directive
- **REACH**: Compliant with EU regulation
- **CE**: Electromagnetic compatibility

### Safety Features
- **ESD Protection**: ±2kV HBM on all pins
- **Reverse Polarity Protection**: Integrated
- **Thermal Protection**: Operating range monitoring

## References

- [ICP-10111 Datasheet](https://product.tdk.com/system/files/dam/doc/product/sensor/pressure/capacitive-pressure/data_sheet/ds-000177-icp-10111-v1.3.pdf)
- [BME688 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme688-ds000.pdf)
- [ME6206 Regulator Datasheet](https://www.microne.com.cn/uploads/file/20200904/ME6206.pdf)

## Ordering Information

**Table 8: Available Part Numbers**

| Part Number | Description | Package | MOQ |
|-------------|-------------|---------|-----|
| ICP10111-001 | Standard Module | Individual | 1 |
| ICP10111-DEV | Development Kit | Kit Box | 1 |
| ICP10111-BULK | Bulk Order | Tray | 100 |

## Revision History

**Table 9: Document Revision History**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-07-18 | Initial release |

## Schematics

![Circuit Schematic](resources/Schematics_icon.jpg)

---

*For technical support and additional information, visit our website or contact our engineering team.*
