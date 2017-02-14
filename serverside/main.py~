import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.message_callback_add("esys/ATeam/B12S", board1_callback)
    client.subscribe("esys/ATeam/#")

# The callback for when a PUBLISH message is received from the server.
def board1_callback(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	data = "hahahahahahhaha"
	client.publish("eeys/ATeam/S2B1",data)


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	data = "hohoohohohohooh"
	client.publish("eeys/ATeam/S2B1",data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.10", 1883, 60)
client.loop_forever()

