def set(bus,deviceAddr):
	#set reg0 0
	bus.writeto_mem(deviceAddr,0x80,b'\x00')

	#set reg0 0x07
	bus.writeto_mem(deviceAddr,0x80,b'\x03')

def read(bus,deviceAddr):
	bus.writeto(deviceAddr,b'\x87')
	#read from MSBreg7 LSBreg8
	return bus.readfrom(deviceAddr,2)

