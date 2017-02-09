import time
import machine
import network
from machine import I2C,Pin
import VCNL4010,conf
from umqtt.simple import MQTTClient 
import ubinascii

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


#MQTT network SSID: EEERover  PW: exhibition
EESID = "EEERover"
EEPW = "exhibition"
TOPIC = "esys/ATeam"
BROKER_ADDRESS = "192.168.0.10"
CLIENT_ID = machine.unique_id()

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "192.168.0.10", 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"esys/ATeam",
    "eesid": b"EEERover",
    "eepw": b"exhibition"
}

load_config()

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
sta_if.connect(EESID, EEPW)
sta_if.isconnected()

client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
#client = MQTTClient(CLIENT_ID,BROKER_ADDRESS)

client.connect()

bus = I2C(scl = Pin(5),sda = Pin(4),freq=100000)
deviceAddr = 19

VCNL4010.init_all(bus,deviceAddr)

buf = bytearray(4)
lum = bytearray(2)
pro = bytearray(2)
data = "testdata"

while True:
	buf = VCNL4010.read_all(bus,deviceAddr)
	lum = buf[0]*256 +buf[1]
	pro = buf[2]*256 +buf[3]
	
	print ("Luminance: %d lux" %lum)
	print ("Proximity: %d" %pro)

	data = "Luminance: %d lux" %lum + "Proximity: %d" %pro
	client.publish(CONFIG['topic'], bytes(data, 'utf-8'))
	time.sleep(0.5)

print('END')
