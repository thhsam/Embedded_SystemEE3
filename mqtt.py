from umqtt.simple import MQTTClient
import machine
import network

#MQTT network SSID: EEERover  PW: exhibition
EESID = "EEERover"
EEPW = "exhibition"

BROKER_ADDRESS = "192.168.0.10"
CLIENT_ID = machine.unique_id()
TOPIC = "esys/ATeam"

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "192.168.0.10",
    "sensor_pin": 0, 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"home",
}

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




data = "testdata"
client = MQTTClient(CLIENT_ID, BROKER_ADDRESS)
client.connect()
client.publish(TOPIC, bytes(data, 'utf-8'))

ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
sta_if.connect(EESID, EEPW)
sta_if.isconnected()
