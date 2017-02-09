def read(bus,deviceAddr):
	#read from MSBreg5 LSBreg6
	return bus.readfrom_mem(deviceAddr,0x16,2) 

def set(bus,deviceAddr):
	#set reg0 0
	bus.writeto_mem(deviceAddr,0x00,b'\x00')

	#write to rgbc timing reg
	bus.writeto_mem(deviceAddr,0x84,b'\x0b')

	#write to w8 time reg : (FF - val)*2.4*(WLONG==1 ? 12:1) ms
	bus.writeto_mem(deviceAddr,0x03,b'\x30')

	#write to config reg : assert WLONG
	bus.writeto_mem(deviceAddr,0x84,b'\x00')

	#write to control : gain control
	bus.writeto_mem(deviceAddr,0x84,b'\x01')

	#set reg0 0x0b, to enable wait + reading
	bus.writeto_mem(deviceAddr,0x80,b'\x0b')

