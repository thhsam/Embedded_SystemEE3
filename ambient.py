def set(bus,deviceAddr):
	#set reg0 0
	bus.writeto_mem(deviceAddr,0x80,b'\x00')

	#write to reg4 : b'1xxx(rate)d
	bus.writeto_mem(deviceAddr,0x84,b'\x9d')

	#set reg0 0x07
	bus.writeto_mem(deviceAddr,0x80,b'\x05')

def read(bus,deviceAddr):
	#read from MSBreg5 LSBreg6
	return bus.readfrom_mem(deviceAddr,0x85,2) 
