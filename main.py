import time,machine,network
from machine import I2C,Pin,RTC
import VCNL4010,conf,TCS3472
from umqtt.simple import MQTTClient 
import ubinascii
import os

def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")


def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")

def set_network(EESID, EEPW):
    import network
    #Disable Automatic Access Point(AP) to reduce Overheads
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
    #Connect to a specificed WiFi Network
        print('connecting to netowrk...')
    
        sta_if.active(True)
        sta_if.connect(EESID, EEPW)
        while not sta_if.isconnected():
            pass

    print('network config:', sta_if.ifconfig())



def sub_cb(topic, msg):
    global Tmsg
    Tmsg = msg
    print((topic, msg))

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "192.168.0.10", 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"esys/ATeam",
    "eesid": b"EEERover",
    "eepw": b"exhibition"
}

load_config()
set_network(CONFIG['eesid'],CONFIG['eepw'])

client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
client.set_callback(sub_cb)
client.connect()
client.subscribe(b"esys/time")

client.wait_msg()

s = str(Tmsg)
year = s[11]+s[12]+s[13]+s[14]
month = s[16]+s[17]
day = s[19]+s[20]
hh = s[22]+s[23]
mm = s[25]+s[26]
ss = s[28]+s[29]        

client.disconnect() 
client.connect()

bus = I2C(scl = Pin(5),sda = Pin(4),freq=100000)
deviceAddr = 19
colordeviceAddr = 41

VCNL4010.init_all(bus,deviceAddr)
TCS3472.set(bus,colordeviceAddr)

buf = bytearray(4)
lum = bytearray(2)
pro = bytearray(2)

bufrgb = bytearray(6)
red = bytearray(2)
green = bytearray(2)
blue = bytearray(2)

rtc=machine.RTC()
rtc.datetime((int(year), int(month), int(day),0, int(hh), int(mm), int(ss), 0))
rtc.datetime()

while True:
	buf = VCNL4010.read_all(bus,deviceAddr)
	lum = buf[0]*256 +buf[1]
	pro = buf[2]*256 +buf[3]
	
        bufrgb = TCS3472.readRGB(bus, colordeviceAddr)
        red = bufrgb[0]*256 + bufrgb[1]
        blue = bufrgb[2]*256 + bufrgb[3]
        green = bufrgb[4]*256 + bufrgb[5]
        
        t = rtc.datetime()
        
        print ("RBG: %d" %red + " Green: %d" %green + " Blue: %d" %blue)
	print ("Luminance: %d lux" %lum)
	print ("Proximity: %d" %pro)
        print ("Time: %d-" %t[0] + "%d-" %t[1] + "%d" %t[2], "%d:" %t[4], "%d:" %t[5], "%d" %t[6])

        #time = str(t[0])+ "_" + str(t[1]) + "_" + str(t[2))
        #data = "{Timestamp: %d_%d_%d:%d:%d:%d" (%t[0],%t[1],%t[2],%t[3],%t[4],%t[5])
	data = "{Luminance: %d," %lum + "Proximity: %d}" %pro

	client.publish(CONFIG['topic'], bytes(data, 'utf-8'))
        time.sleep(0.5)

print('END')
