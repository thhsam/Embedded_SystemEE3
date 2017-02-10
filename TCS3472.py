def readC(bus,deviceAddr):
	#read clear
	return bus.readfrom_mem(deviceAddr,0x94,2) 

def readR(bus,deviceAddr):
	#read red
	return bus.readfrom_mem(deviceAddr,0x96,2) 

def readG(bus,deviceAddr):
	#read green
	return bus.readfrom_mem(deviceAddr,0x98,2) 

def readB(bus,deviceAddr):
	#read blue
	return bus.readfrom_mem(deviceAddr,0x9A,2) 

def readRGB(bus,deviceAddr):
	#read rgb
	return bus.readfrom_mem(deviceAddr,0x96,6) 

def readCRGB(bus,deviceAddr):
	#read RGBC
	return bus.readfrom_mem(deviceAddr,0x94,8) 



def set(bus,deviceAddr):
	#set reg0 0
	bus.writeto(deviceAddr,b'\x80')
	bus.writeto(deviceAddr,b'\x00')

	#write to rgbc timing reg1
	bus.writeto(deviceAddr,b'\x81')
	bus.writeto(deviceAddr,b'\xd5')

	#write to w8 time reg3 : (FF - val)*2.4*(WLONG==1 ? 12:1) ms
	bus.writeto(deviceAddr,b'\x83')
	bus.writeto(deviceAddr,b'\x30')

	#write to config regD : assert WLONG
	bus.writeto(deviceAddr,b'\x8D')
	bus.writeto(deviceAddr,b'\x00')

	#write to control regF: gain control
	bus.writeto(deviceAddr,b'\x8F')
	bus.writeto(deviceAddr,b'\x01')

	#set reg0 0x0b, to enable wait + reading
	bus.writeto(deviceAddr,b'\x80')
	bus.writeto(deviceAddr,b'\x0b')
