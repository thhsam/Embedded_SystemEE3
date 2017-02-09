def setP(bus,deviceAddr):
	#set reg0 0
	bus.writeto_mem(deviceAddr,0x80,b'\x00')

	#set reg0 0x03, to read proximity
	bus.writeto_mem(deviceAddr,0x80,b'\x03')

def readP(bus,deviceAddr):
	bus.writeto(deviceAddr,b'\x87')
	#read from MSBreg7 LSBreg8
	return bus.readfrom(deviceAddr,2)

def setA(bus,deviceAddr):
	#set reg0 0
	bus.writeto_mem(deviceAddr,0x80,b'\x00')

	#write to reg4 : b'1xxx(rate)d
	bus.writeto_mem(deviceAddr,0x84,b'\x9d')

	#set reg0 0x05, to read ambient
	bus.writeto_mem(deviceAddr,0x80,b'\x05')

def read(bus,deviceAddr):
	#read from MSBreg5 LSBreg6
	return bus.readfrom_mem(deviceAddr,0x85,2) 

def init_all(bus,deviceAddr):
	#reset reg0 Contorl Reg to 0
	#bus.writeto_mem(deviceAddr,0x80,b'\x00')
	
	bus.writeto_mem(deviceAddr,0x80,b'\xFF')
	
	bus.writeto_mem(deviceAddr,0x82,b'\x00')
	#write to reg4 : b'1xxx(rate)d
	bus.writeto_mem(deviceAddr,0x84,b'\x9D')

def read_all(bus,deviceAddr):
    return bus.readfrom_mem(deviceAddr,0x85,4)

