import paho.mqtt.client as mqtt
import time
import json


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.message_callback_add("esys/ATeam/BoardToServer", board1_callback)
    client.subscribe("esys/ATeam/#")

# The callback for when a PUBLISH message is received from the server.
def board1_callback(client, userdata, msg):
	global i		
	print(msg.topic+" "+str(msg.payload))	
	data = "data recieved from board, %d" %i + "th iteration"
	time.sleep(0.5)
	i = i + 1
	msgJ = json.loads(str(msg.payload))
	print(msgJ['Hue'])
	hue = msgJ['Hue']
	
	client.publish("esys/ATeam/ServerToBoard",data)


client = mqtt.Client()
client.on_connect = on_connect

i = 0
client.connect("192.168.0.10", 1883, 60)
print("successfully connected")
client.loop_forever()
