
# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# VCNL4010
# This code is designed to work with the VCNL4010_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=VCNL4010_I2CS#tabs-0-product_tabset-2

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# VCNL4010 address, 0x13(19)
# Select command register, 0x80(128)
#		0xFF(255)	Enable ALS and proximity measurement, LP oscillator
bus.write_byte_data(0x13, 0x80, 0xFF)
# VCNL4010 address, 0x13(19)
# Select proximity rate register, 0x82(130)
#		0x00(00)	1.95 proximity measeurements/sec
bus.write_byte_data(0x13, 0x82, 0x00)
# VCNL4010 address, 0x13(19)
# Select ambient light register, 0x84(132)
#		0x9D(157)	Continuos conversion mode, ALS rate 2 samples/sec
bus.write_byte_data(0x13, 0x84, 0x9D)

time.sleep(0.8)

# VCNL4010 address, 0x13(19)
# Read data back from 0x85(133), 4 bytes
# luminance MSB, luminance LSB, Proximity MSB, Proximity LSB
data = bus.read_i2c_block_data(0x13, 0x85, 4)

# Convert the data
luminance = data[0] * 256 + data[1]
proximity = data[2] * 256 + data[3]

# Output data to screen
print "Ambient Light Luminance : %d lux" %luminance
print "Proximity of the Device : %d" %proximity
