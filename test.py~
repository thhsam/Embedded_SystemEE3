import time,machine,network
from machine import I2C,Pin,RTC
import VCNL4010,conf,TCS3472
from umqtt.simple import MQTTClient 
import ubinascii
import os,ujson
print('Hello world! I can count:')
i = 1

bus = I2C(scl = Pin(5),sda = Pin(4),freq=100000)
bus2= I2C(scl = Pin(13),sda = Pin(15),freq=100000)


pin12 = machine.Pin(12,machine.Pin.OUT)

deviceAddr = 19
colordeviceAddr = 41

VCNL4010.init_all(bus,deviceAddr)
TCS3472.set(bus,colordeviceAddr)

VCNL4010.init_all(bus2,deviceAddr)
TCS3472.set(bus2,colordeviceAddr)


while True:
	print(i)
	buf = VCNL4010.read_all(bus,deviceAddr)
	lum = buf[0]*256 +buf[1]
	pro = buf[2]*256 +buf[3]
	buf2= VCNL4010.read_all(bus2,deviceAddr)
	lum2= buf[0]*256 +buf[1]
	pro2= buf[2]*256 +buf[3]

	print ("bus0")
	print ("Luminance: %d lux" %lum)
	print ("Proximity: %d" %pro)
	print ("bus1")
	print ("Luminance: %d lux" %lum2)
	print ("Proximity: %d" %pro2)
