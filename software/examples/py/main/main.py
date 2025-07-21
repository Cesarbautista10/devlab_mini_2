#!/usr/bin/env python3
"""
Electronic Module - Main Example
=================================

This example demonstrates basic communication with an electronic module
using I2C interface through Python. Serves as a template for module integration.

Author: DevLab Team
Date: 2025
License: MIT
"""

import time
import sys
import signal
import logging
from typing import Tuple, Optional

try:
    import smbus2
except ImportError:
    print("Error: smbus2 library not found.")
    print("Install with: pip install smbus2")
    sys.exit(1)

# I2C Configuration
I2C_BUS = 1
MODULE_I2C_ADDR = 0x48

# Generic Module Commands
MODULE_CMD_READ_DATA = 0x01
MODULE_CMD_READ_STATUS = 0x02
MODULE_CMD_READ_VERSION = 0x03

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ElectronicModule:
    """
    Electronic Module Class
    
    This class provides methods to communicate with a generic electronic module
    and read data measurements. Serves as a template for module integration.
    """
    
    def __init__(self, bus_number: int = I2C_BUS, address: int = MODULE_I2C_ADDR):
        """
        Initialize the electronic module
        
        Args:
            bus_number (int): I2C bus number (default: 1)
            address (int): I2C device address (default: 0x48)
        """
        self.bus_number = bus_number
        self.address = address
        self.bus = None
        self._initialize_i2c()
    
    def _initialize_i2c(self) -> None:
        """Initialize I2C communication"""
        try:
            self.bus = smbus2.SMBus(self.bus_number)
            logger.info(f"I2C initialized on bus {self.bus_number}, address 0x{self.address:02X}")
        except Exception as e:
            logger.error(f"Failed to initialize I2C: {e}")
            raise
    
    def read_data(self) -> Optional[int]:
        """
        Read data from electronic module
        
        Returns:
            int: Module data value, or None if error
        """
        try:
            # Send read data command
            self.bus.write_byte(self.address, MODULE_CMD_READ_DATA)
            
            # Wait for response
            time.sleep(0.01)  # 10ms
            
            # Read data (2 bytes)
            data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
            
            # Convert to 16-bit value
            value = (data[0] << 8) | data[1]
            
            return value
            
        except Exception as e:
            logger.error(f"Error reading data: {e}")
            return None
    
    def read_status(self) -> Optional[int]:
        """
        Read status from electronic module
        
        Returns:
            int: Status byte, or None if error
        """
        try:
            # Send read status command
            self.bus.write_byte(self.address, MODULE_CMD_READ_STATUS)
            
            # Wait for response
            time.sleep(0.01)  # 10ms
            
            # Read status byte
            status = self.bus.read_byte(self.address)
            
            return status
            
        except Exception as e:
            logger.error(f"Error reading status: {e}")
            return None
    
    def read_version(self) -> Optional[str]:
        """
        Read firmware version from electronic module
        
        Returns:
            str: Version string, or None if error
        """
        try:
            # Send read version command
            self.bus.write_byte(self.address, MODULE_CMD_READ_VERSION)
            
            # Wait for response
            time.sleep(0.01)  # 10ms
            
            # Read version data (4 bytes)
            data = self.bus.read_i2c_block_data(self.address, 0x00, 4)
            
            # Convert to version string
            version = f"{data[0]}.{data[1]}.{data[2]}.{data[3]}"
            
            return version
            
        except Exception as e:
            logger.error(f"Error reading version: {e}")
            return None
    
    def close(self) -> None:
        """Close I2C connection"""
        if self.bus:
            self.bus.close()
            logger.info("I2C connection closed")

def print_module_info():
    """Print module information"""
    print("="*60)
    print("Electronic Module - Python Example")
    print("="*60)
    print(f"I2C Bus: {I2C_BUS}")
    print(f"I2C Address: 0x{MODULE_I2C_ADDR:02X}")
    print("Commands:")
    print(f"  Read Data: 0x{MODULE_CMD_READ_DATA:02X}")
    print(f"  Read Status: 0x{MODULE_CMD_READ_STATUS:02X}")
    print(f"  Read Version: 0x{MODULE_CMD_READ_VERSION:02X}")
    print("="*60)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down gracefully...")
    sys.exit(0)

def main():
    """Main function"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print_module_info()
    
    try:
        # Initialize module
        module = ElectronicModule()
        
        # Read version info
        version = module.read_version()
        if version:
            print(f"Module Version: {version}")
        
        print("\nStarting continuous data reading (Ctrl+C to stop)...")
        print("Time\t\tData\tStatus")
        print("-" * 40)
        
        while True:
            # Read data
            data = module.read_data()
            status = module.read_status()
            
            if data is not None and status is not None:
                timestamp = time.strftime("%H:%M:%S")
                print(f"{timestamp}\t{data}\t0x{status:02X}")
            else:
                print("Error reading from module")
            
            time.sleep(1)  # Read every second
            
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        try:
            module.close()
        except:
            pass

if __name__ == "__main__":
    main()
