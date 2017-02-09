import time
from machine import I2C,Pin
import change,ambient,proximity

<<<<<<< HEAD
print('START')
=======
boogie = bytearray(1)

boogie = b'\x09'
print(boogie)
>>>>>>> 9c44a466d590fd50f67dcd33d85e10d45c1b6fb3

bus = I2C(scl = Pin(5),sda = Pin(4),freq=100000)

deviceAddr = 19

proximity.set(bus,deviceAddr)

i = 1
buf = bytearray(4)
lum = bytearray(2)
pro = bytearray(2)

while True:
	buf = proximity.read(bus,deviceAddr)
<<<<<<< HEAD
#	print(buf)
	
	lum = buf[0]*256 +buf[1]
	pro = buf[2]*256 +buf[3]
	

	print ("Ambient Light Luminance: %d lux" %lum)
	print ("Proximity of the Device: %d" %pro)
	time.sleep(0.8)
=======
	print(str(buf))
	i += 1
	time.sleep(1.5)
>>>>>>> 9c44a466d590fd50f67dcd33d85e10d45c1b6fb3

print('fin')
