#.................................................
# INFO:
# The A-Team (IChess) Production Code v1
# Date: 21/02/17
# Author: thh13, hsl113, yw11614, lpl214
#
# Imperial College London 2017
#..................................................

import time,machine,network, ubinascii, os, ujson, VCNL4010,conf,TCS3472
from machine import I2C,Pin,RTC
from umqtt.simple import MQTTClient


#function to load config file to set MMQT topics and broker
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

#function to save config settings
def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")

#function to connect to wifi
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

#Callback function to set global time to broker time
def sub_cb(topic, msg):
    global Tmsg
    Tmsg = msg
    print((topic, msg))

#Callback function to receive message from the server side
def sub_nof(topic, msg):
    global Recv
    Recv = msg
    print((topic,msg))

#function to find the hue settings
def find_hue(r,g,b):
	hsvR = float(r * 1.0)
	hsvG = float(b * 1.0)
	hsvB = float(g * 1.0)

	if hsvR == hsvB == hsvG:
		hsv = 0
	elif hsvR < hsvG and hsvR < hsvB:
		hsv = 120 +  120*(hsvB - hsvR)/((hsvG - hsvR) + (hsvB - hsvR))
	elif hsvG < hsvB and hsvG < hsvR:
		hsv = 240 + 120*(hsvR - hsvG)/((hsvR - hsvG) + (hsvB - hsvG))
	else:
		hsv = 120*(hsvG - hsvB)/((hsvR - hsvB) + (hsvG - hsvB))
	return hsv

#function to find the colour
def find_color(hsv):
    #Blue Bishop
    if hsv > 160 and hsv < 170:
        colour = "B"
    #Red Queen
    elif hsv > 0 and hsv < 10:
        colour = "R"
    #Green King
    elif hsv > 260 and hsv < 270:
        colour = "G"
    #Yellow Knight
    elif hsv > 290 and hsv < 315:
        colour = "Y"
    #Orange Castle
    elif hsv > 325 and hsv < 345:
        colour = "O"
    #Cream Whie Paw
    elif hsv > 190 and hsv < 220:
        colour = "C"
    else: 
        #Undefined
        colour = "U"
    return colour

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "192.168.0.10", 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"esys/ATeam",
    "eesid": b"EEERover",
    "eepw": b"exhibition"
}

#Declare buffer for results from sensors
buf = bytearray(4)
lum = [None]*3
pro = [None]*3
col = [None]*3
bus = [None]*3
hue = [None]*3


#Declare array of GPIO pins
pin = [None]*3
pin[0] = machine.Pin(12,machine.Pin.OUT)
pin[1] = machine.Pin(0,machine.Pin.OUT)
#pin[2] = machine.Pin(2,machine.Pin.OUT)        #used to connect with the third set of sensor

#Connect to MQTT WIFI
load_config()
set_network(CONFIG['eesid'],CONFIG['eepw'])

#Connect to MQTT Broker
client = MQTTClient(CONFIG['client_id'], CONFIG['broker'])
client.set_callback(sub_cb)
client.connect()
#Subscrib to Sys Time using QoS = 1
client.subscribe(b"esys/time", qos=1)
client.wait_msg()

#Arrange Sys Time format
s = str(Tmsg)
year = s[11]+s[12]+s[13]+s[14]
month = s[16]+s[17]
day = s[19]+s[20]
hh = s[22]+s[23]
mm = s[25]+s[26]
ss = s[28]+s[29]

#Set System time
rtc=machine.RTC()
rtc.datetime((int(year), int(month), int(day),0, int(hh), int(mm), int(ss), 0))
rtc.datetime()

#Reset MQTT connection
client.disconnect() 
client.connect()

#Set I2C pins
bus[0] = I2C(scl = Pin(5),sda = Pin(4),freq=100000)
bus[1] = I2C(scl = Pin(5),sda = Pin(16),freq=100000)
#bus[2] = I2C(scl = Pin(5),sda = Pin(14),freq=100000)

#Sensor I2C Address
deviceAddr = 19
colordeviceAddr = 41

#Init Sensors
for index in range(0,2):
	VCNL4010.init_all(bus[index],deviceAddr)
	TCS3472.set(bus[index],colordeviceAddr)

bufrgb = bytearray(6)


#We have used polling instead of interrupt, this is becasue we want to constantly know the status of the board.
#


#Main LOOP
while True:
    
    for i in range(0,2):
        #Read Data from Sensor
        buf = VCNL4010.read_all(bus[i],deviceAddr)
        lum[i] = buf[0]*256 +buf[1]
        pro[i] = buf[2]*256 +buf[3]

        bufrgb = TCS3472.readRGB(bus[i], colordeviceAddr)
        hue[i] = find_hue(bufrgb[0] + bufrgb[1]*256,bufrgb[2] + bufrgb[3]*256,bufrgb[4] + bufrgb[5]*256)		            
        col[i] = find_color(hue[i])            

        if pro[i] > 2300:
            pin[i].value(1)
        else:
            pin[i].value(0)
            col[i] = "U"

        t = rtc.datetime()
		
        #for debug
        print ("\nblock%d:")
        print ("Luminance: %d lux" %lum[i])
        print ("Proximity: %d" %pro[i])
        print ("Time: %d-" %t[0] + "%d-" %t[1] + "%d" %t[2], "%d:" %t[4], "%d:" %t[5], "%d" %t[6])
        print ("Colour: %s" %hue[i])
        print ("Colour: %s" %col[i])

    data = "{\"Time\": %d-" %t[0] + "%d-" %t[1] + "%d " %t[2] + "%d" %t[4] + ":%d" %t[5] + ":%d, " %t[6] + "\"Luminance\": %d, " %lum[i] + "\"Proximity\": %d, " %pro[i] + "\"Hue\": %d }" %hue[i]


    #Put Data into JSON
    DATA = {
        "Time" : "%d-" %t[0] + "%d-" %t[1] + "%d " %t[2] + "%d" %t[4] + ":%d" %t[5] + ":%d, " %t[6],
        "t45" : "%s" %col[0],
        "t46" : "%s" %col[1],
        "t55" : "%s" %col[2]
    }


    #Publish data over MQTT using QoS 1
    #client.publish('esys/ATeam/BoardToServer', bytes(data, 'utf-8'))
    json_str = ujson.dumps(DATA)
    client.publish('esys/ATeam/BoardToServer', bytes(json_str, 'utf-8'), qos=1)

    #Put Device to sleep, and add delay
    time.sleep(0.5)
        
    '''    
    #Recieve Ack from Server
    client.disconnect()
    client.connect()
    client.set_callback(sub_nof)
    client.subscribe(b"esys/ATeam/ServerToBoard", qos=1)
    time.sleep(0.5)
    client.check_msg()
    '''
print('END')
