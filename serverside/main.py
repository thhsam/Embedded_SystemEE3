import paho.mqtt.client as mqtt
import time
import json
from cb import GameBoard
import Tkinter as tk

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
	
	DATA = {
	    "Name": 'Server',
	    "iteration": i,
	    "1c": 1
	}
	board.update()
	client.publish("esys/ATeam/ServerToBoard",json.dumps(DATA))
def _main(event):
	global client
	global board
	print event.x, event.y
	board.removepiece("player0")
'''
	client = mqtt.Client()
	client.on_connect = on_connect
	client.connect("192.168.0.10", 1883, 60)
	client.loop_forever()
'''
i = 0

root = tk.Tk()
board = GameBoard(root)
pwnW = tk.PhotoImage(file = "0.gif")
pwnB = tk.PhotoImage(file = "1.gif")
for i in range(0,8):
	board.addpiece("player%d"%i, pwnW, 1,i)
	board.addpiece("player%d"%(i+8), pwnB, 6,i)

board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
root.bind("<Button-1>", _main)

root.mainloop()

