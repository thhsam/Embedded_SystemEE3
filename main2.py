#import machine
from machine import Pin,I2C
import ambient,proximity
import time

def readRegister(regNum,n):
	for i = 0:n
		print(bus.readfrom_mem(deviceAddr,0x80+regNum+i) + '\n')


#initiating the device serial ports
bus = I2C(Pin(5),Pin(4),freq=100000)

if(!deviceAddr = bus.scan())
	print('error: no devices detected')
	raise SystemExit

print(readRegister(0))

i = 1
while True:
	buf = readAmbient()
	print(i + ':')
	print(buf)
	i+=1
	time.sleep(1.0)
