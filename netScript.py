import socket
try:
   import cPickle as pickle
except:
   import pickle
import random
import bge.logic as logic
IPAddress = '192.168.0.33'
owner = logic.getCurrentController().owner
g = logic.globalDict
try:
    hostname = g['hostname']
except:
    g['hostname'] = random.randrange(9999)
    hostname = g['hostname']
playerAdder = owner.actuators["addPlayer"]
def addPlayer(id):
    print("new peer connected")
    playerAdder.instantAddObject()
    newPlayerObject = playerAdder.objectLastCreated
    g['playerList'][id]=newPlayerObject
def handleResponse(response):
    id = response[0]
    messageType = response[1]
    #player is sending status update
    if(messageType == "s"):
        position = response[2]
        orientation = response[3]
        g['playerList'][id].position = position
        g['playerList'][id].orientation = orientation
    #new player is joining
    if(messageType == "j"):
        print("adding player "+str(id))
        if(id!=hostname):
            addPlayer(id)
        else:
            print("we joined the game")
    #player has exists already in the game
    if(id not in g['playerList']):
        addPlayer(id)
try:
    obj = g['playerQuad']
    ori = [list(obj.orientation[0]),list(obj.orientation[1]),list(obj.orientation[2])]
    pos = list(obj.position)
    
    message = [hostname,"s",pos,ori];
except:
    print("waiting for setup")
    message = [hostname,"j"];
    g['playerList'] = {}

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((IPAddress, 8089))
clientsocket.send(pickle.dumps(message,protocol=2))
#receive
buffer = clientsocket.recv(1024)
if len(buffer) > 0:
    response = pickle.loads(buffer)
    handleResponse(response)

