#---------------------------------------------------------------
# Code used to collect data from boards
# Able to connect to board through mqtt messages, return 
# information based on calculations. The status of both boards
# will also be visible through a GUI.
# A right click is required to enable mqtt transmission.
#
# In full version, it will be able to connect multiple boards,
# select between different board games, and is able to check
# validity of current status, and hint players of valid following
# moves
#
# 2017. Imperial Colege London
#---------------------------------------------------------------

import paho.mqtt.client as mqtt
import time
import json
from cb import GameBoard
import Tkinter as tk
import chess

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.message_callback_add("esys/ATeam/BoardToServer", board1_callback)
    client.subscribe("esys/ATeam/#")

# The callback for when a PUBLISH message is received from the server.
def board1_callback(client, userdata, msg):
	global board,chesstype
	# printing debug messages
	print(msg.topic+" "+str(msg.payload))	
	msgJ = json.loads(str(msg.payload))
	print("t45" + str(msgJ['t45']))
	print("t46" + str(msgJ['t46']))

	
	if msgJ['t45'] != "U":
		board.removepiece("t45")
		board.addpiece("t45",chesstype[msgJ['t45']],4,5)
	else:
		board.removepiece("t45")
	if msgJ['t46'] != "U":
		board.removepiece("t46")
		board.addpiece("t46",chesstype[msgJ['t46']],4,6)
	else:
		board.removepiece("t46")
	#sending chessboard data to the board(s); in full version, will consist of data for the entire board.
	DATA = {
	    "Name": 'Server',
	    "t11": 1
	}
	board.update()
	client.publish("esys/ATeam/ServerToBoard",json.dumps(DATA))

def _main(event):
	global client
	global board
	print event.x, event.y

	client = mqtt.Client()
	client.on_connect = on_connect
	client.connect("192.168.0.10", 1883, 60)
	client.loop_forever()
if __name__ == "__main__":

	#setting up the board with default pieces, since the full version is not acquirable
	root = tk.Tk()
	board = GameBoard(root)
	
	chesstype = {}
	chesstype["R"] = tk.PhotoImage(file = "queenB.gif")
	chesstype["G"] = tk.PhotoImage(file = "kingB.gif")
	chesstype["B"] = tk.PhotoImage(file = "bishopB.gif")
	chesstype["Y"] = tk.PhotoImage(file = "knightB.gif")
	chesstype["O"] = tk.PhotoImage(file = "rookB.gif")
	chesstype["C"] = tk.PhotoImage(file = "pawnB.gif")

	chesstype["R2"] = tk.PhotoImage(file = "queenW.gif")
	chesstype["G2"] = tk.PhotoImage(file = "kingW.gif")
	chesstype["B2"] = tk.PhotoImage(file = "bishopW.gif")
	chesstype["Y2"] = tk.PhotoImage(file = "knightW.gif")
	chesstype["O2"] = tk.PhotoImage(file = "rookW.gif")
	chesstype["C2"] = tk.PhotoImage(file = "pawnW.gif")



	for i in range(0,7):
		board.addpiece("player%d"%i, chesstype["C2"], 1,i)
		board.addpiece("player%d"%(i+8), chesstype["C"], 6,i)
	board.removepiece("player13")
	board.removepiece("player9")
	board.removepiece("player14")
	board.addpiece("player9", chesstype["C"] , 5 ,1)
	board.addpiece("player15", chesstype["C"] , 4 ,7)
	board.addpiece("player16", chesstype["G2"], 0,2)
	board.addpiece("player17", chesstype["Y2"], 2,5)	
	
	
	empty = tk.PhotoImage(file = "Blank.gif")
	board.addpiece("t45",empty,4,5)
	board.addpiece("t46",empty,4,6)

	board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
	root.bind("<Button-3>", _main)

	#entering the GUI loop
	root.mainloop()

