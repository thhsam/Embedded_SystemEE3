import time
from machine import I2C,Pin
import change,ambient,proximity

print('shit')

bus = I2C(scl = Pin(5),sda = Pin(4),freq=100000)

deviceAddr = 19

proximity.set(bus,deviceAddr)

i = 1
buf = bytearray(2)

while True:
	buf = proximity.read(bus,deviceAddr)
	print(buf)
	i +=1
	time.sleep(0.5)

print('fin')
