def set(bus,deviceAddr):
	#set reg0 0
	bus.writeto_mem(deviceAddr,0x80,b'\x00')

	#set reg0 0x07
	bus.writeto_mem(deviceAddr,0x80,b'\xFF')
	
	bus.writeto_mem(deviceAddr,0x82,b'\x00')

	bus.writeto_mem(deviceAddr,0x84,b'\x9D')
	

def read(bus,deviceAddr):
	#bus.writeto(deviceAddr,b'\x85')
	#read from MSBreg7 LSBreg8
	return bus.readfrom_mem(deviceAddr,0x85,4)

