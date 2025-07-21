/**
 * @file main.c
 * @brief Electronic Module - Main Example
 * @author DevLab Team
 * @date 2025
 * 
 * This example demonstrates basic communication with an electronic module
 * using I2C interface. Serves as a template for module integration.
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>

// I2C Configuration
#define I2C_BUS "/dev/i2c-1"
#define MODULE_I2C_ADDR 0x48

// Generic Module Commands
#define MODULE_CMD_READ_DATA 0x01
#define MODULE_CMD_READ_STATUS 0x02
#define MODULE_CMD_READ_VERSION 0x03

// Function prototypes
int init_i2c(const char* device, int addr);
int read_module_data(int fd, uint16_t* data);
int read_module_status(int fd, uint8_t* status);
void print_module_info(void);

/**
 * @brief Initialize I2C communication
 * @param device I2C device path
 * @param addr I2C slave address
 * @return File descriptor on success, -1 on error
 */
int init_i2c(const char* device, int addr) {
    int fd = open(device, O_RDWR);
    if (fd < 0) {
        fprintf(stderr, "Error opening I2C device %s: %s\n", device, strerror(errno));
        return -1;
    }
    
    if (ioctl(fd, I2C_SLAVE, addr) < 0) {
        fprintf(stderr, "Error setting I2C slave address 0x%02X: %s\n", addr, strerror(errno));
        close(fd);
        return -1;
    }
    
    return fd;
}

/**
 * @brief Read pressure from ICP-10111 sensor
 * @param fd I2C file descriptor
 * @param pressure Pointer to store pressure value (hPa)
 * @return 0 on success, -1 on error
 */
int read_pressure(int fd, float* pressure) {
    uint8_t cmd[3] = {0x48, 0xA3, 0x00}; // Pressure measurement command
    uint8_t data[9];
    
    // Send measurement command
    if (write(fd, cmd, 3) != 3) {
        fprintf(stderr, "Error sending pressure command: %s\n", strerror(errno));
        return -1;
    }
    
    // Wait for measurement
    usleep(100000); // 100ms
    
    // Read measurement data
    if (read(fd, data, 9) != 9) {
        fprintf(stderr, "Error reading pressure data: %s\n", strerror(errno));
        return -1;
    }
    
    // Convert raw data to pressure (simplified conversion)
    uint32_t raw_pressure = (data[0] << 16) | (data[1] << 8) | data[2];
    *pressure = (float)raw_pressure / 100.0f; // Convert to hPa
    
    return 0;
}

/**
 * @brief Read temperature from ICP-10111 sensor
 * @param fd I2C file descriptor
 * @param temperature Pointer to store temperature value (°C)
 * @return 0 on success, -1 on error
 */
int read_temperature(int fd, float* temperature) {
    uint8_t cmd[3] = {0x60, 0x9C, 0x00}; // Temperature measurement command
    uint8_t data[6];
    
    // Send measurement command
    if (write(fd, cmd, 3) != 3) {
        fprintf(stderr, "Error sending temperature command: %s\n", strerror(errno));
        return -1;
    }
    
    // Wait for measurement
    usleep(50000); // 50ms
    
    // Read measurement data
    if (read(fd, data, 6) != 6) {
        fprintf(stderr, "Error reading temperature data: %s\n", strerror(errno));
        return -1;
    }
    
    // Convert raw data to temperature (simplified conversion)
    uint16_t raw_temp = (data[0] << 8) | data[1];
    *temperature = (float)raw_temp / 100.0f - 40.0f; // Convert to °C
    
    return 0;
}

/**
 * @brief Print sensor information
 */
void print_sensor_info(void) {
    printf("========================================\n");
    printf("  ICP-10111 Barometric Pressure Sensor\n");
    printf("========================================\n");
    printf("I2C Address: 0x%02X\n", ICP10111_I2C_ADDR);
    printf("I2C Bus: %s\n", I2C_BUS);
    printf("Pressure Range: 300-1250 hPa\n");
    printf("Accuracy: ±0.4 hPa @ 25°C\n");
    printf("========================================\n\n");
}

/**
 * @brief Main function
 */
int main(void) {
    int fd;
    float pressure, temperature;
    int sample_count = 0;
    
    print_sensor_info();
    
    // Initialize I2C communication
    fd = init_i2c(I2C_BUS, ICP10111_I2C_ADDR);
    if (fd < 0) {
        fprintf(stderr, "Failed to initialize I2C communication\n");
        return EXIT_FAILURE;
    }
    
    printf("Starting continuous measurement...\n");
    printf("Press Ctrl+C to stop\n\n");
    printf("Sample | Pressure (hPa) | Temperature (°C)\n");
    printf("-------|----------------|------------------\n");
    
    // Continuous measurement loop
    while (1) {
        sample_count++;
        
        // Read pressure
        if (read_pressure(fd, &pressure) == 0) {
            // Read temperature
            if (read_temperature(fd, &temperature) == 0) {
                printf("%6d | %13.2f | %15.2f\n", sample_count, pressure, temperature);
            } else {
                printf("%6d | %13.2f | %15s\n", sample_count, pressure, "Error");
            }
        } else {
            printf("%6d | %13s | %15s\n", sample_count, "Error", "Error");
        }
        
        // Wait before next measurement
        sleep(1);
    }
    
    // Cleanup
    close(fd);
    return EXIT_SUCCESS;
}
