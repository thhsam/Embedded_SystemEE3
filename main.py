import time,machine,network
from machine import I2C,Pin,RTC
import VCNL4010,conf,TCS3472
from umqtt.simple import MQTTClient 
import ubinascii
import os,ujson

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

def sub_nof(topic, msg):
    global Recv
    Recv = msg
    print((topic,msg))

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "192.168.0.10", 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"esys/ATeam",
    "eesid": b"EEERover",
    "eepw": b"exhibition"
}

pin12 = machine.Pin(12,machine.Pin.OUT)


load_config()
set_network(CONFIG['eesid'],CONFIG['eepw'])

client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
client.set_callback(sub_cb)
client.connect()
client.subscribe(b"esys/time", qos=1)

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

bus2 = I2C(scl = Pin(5),sda = Pin(16),freq=100000)
bus = I2C(scl = Pin(5),sda = Pin(4),freq=100000)

deviceAddr = 19
colordeviceAddr = 41

VCNL4010.init_all(bus,deviceAddr)
TCS3472.set(bus,colordeviceAddr)

VCNL4010.init_all(bus2,deviceAddr)
TCS3472.set(bus2,colordeviceAddr)

buf = bytearray(4)
lum = bytearray(2)
pro = bytearray(2)
buf1 = bytearray(4)
lum1 = bytearray(2)
pro1 = bytearray(2)
colour = ""
colour = ""


bufrgb = bytearray(6)
red = bytearray(2)
green = bytearray(2)
blue = bytearray(2)

bufrgb1 = bytearray(6)
red1 = bytearray(2)
green1 = bytearray(2)
blue1 = bytearray(2)


rtc=machine.RTC()
rtc.datetime((int(year), int(month), int(day),0, int(hh), int(mm), int(ss), 0))
rtc.datetime()

while True:
	buf = VCNL4010.read_all(bus,deviceAddr)
	lum = buf[0]*256 +buf[1]
	pro = buf[2]*256 +buf[3]
	
    buf1 = VCNL4010.read_all(bus2,deviceAddr)
    lum1 = buf1[0]*256 + buf1[1]
    pro1 = buf1[2]*256 +buf1[3]
    
    bufrgb = TCS3472.readRGB(bus, colordeviceAddr)
    red = bufrgb[0] + bufrgb[1]*256
    green = bufrgb[2] + bufrgb[3]*256
    blue = bufrgb[4] + bufrgb[5]*256
        
    bufrgb1 = TCS3472.readRGB(bus2, colordeviceAddr)
    red1 = bufrgb1[0] + bufrgb1[1]*256
    green1 = bufrgb1[2] + bufrgb1[3]*256
    blue1 = bufrgb1[4] + bufrgb1[5]*256

	hsvR = float(red * 1.0)
	hsvG = float(blue* 1.0)
	hsvB = float(green*1.0)
    
    hsvR1 = float(red1 * 1.0)
    hsvG1 = float(blue1* 1.0)
    hsvB1 = float(green1*1.0)

	if hsvR == hsvB == hsvG:
		hsv = 0
	elif hsvR < hsvG and hsvR < hsvB:
		hsv = 120 +  120*(hsvB - hsvR)/((hsvG - hsvR) + (hsvB - hsvR))
	elif hsvG < hsvB and hsvG < hsvR:
		hsv = 240 + 120*(hsvR - hsvG)/((hsvR - hsvG) + (hsvB - hsvG))
	else:
		hsv = 120*(hsvG - hsvB)/((hsvR - hsvB) + (hsvG - hsvB))
                
                
        if hsv > 160 and hsv < 170:
                colour = "Blue"
        elif hsv > 0 and hsv < 10:
                colour = "Red"
        elif hsv > 260 and hsv < 270:
                colour = "Green"
        elif hsv > 290 and hsv < 310:
                colour = "Yellow"
        elif hsv > 325 and hsv < 345:
                colour = "Orange"
        elif hsv > 190 and hsv < 220:
                colour = "Cream White"
        else: 
            colour = "undefined"

        if pro > 2300:
            pin12.value(1)
        else:
            pin12.value(0)

        t = rtc.datetime()
        
        print ("Red: %d" %red + " Green: %d" %green + " Blue: %d" %blue + " Hue: %d" %hsv)
        print ("Luminance: %d lux" %lum)
        print ("Proximity: %d" %pro)
        print ("Time: %d-" %t[0] + "%d-" %t[1] + "%d" %t[2], "%d:" %t[4], "%d:" %t[5], "%d" %t[6])
        print ("Colour: %s" %colour)

        data = "{\"Time\": %d-" %t[0] + "%d-" %t[1] + "%d " %t[2] + "%d" %t[4] + ":%d" %t[5] + ":%d, " %t[6] + "\"Luminance\": %d, " %lum + "\"Proximity\": %d, " %pro + "\"Hue\": %d }" %hsv

        #Put Data into JSON
        DATA = {
            "Time" : "%d-" %t[0] + "%d-" %t[1] + "%d " %t[2] + "%d" %t[4] + ":%d" %t[5] + ":%d, " %t[6],
            "Luminance" : "%d" %lum,
            "Proximity" : "%d" %pro,
            "Hue" : "%d" %hsv,
            "Colour" : "%s" %colour
        }

        #Publish data over MQTT
        #client.publish('esys/ATeam/BoardToServer', bytes(data, 'utf-8'))
        json_str = ujson.dumps(DATA)
        client.publish('esys/ATeam/BoardToServer', bytes(json_str, 'utf-8'), qos=1)

        #Put Device to sleep, and add delay
        time.sleep(0.5)
                
        #Recieve Ack from Server
        client.disconnect()
        client.connect()
        client.set_callback(sub_nof)
        client.subscribe(b"esys/ATeam/ServerToBoard", qos=1)
        time.sleep(0.5)
        client.check_msg()

print('END')
