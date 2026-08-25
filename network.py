# Python program to implement client side of chat room.
import socket
import select
import sys
import bge.logic as logic
import pickle
cont = logic.getCurrentController()
own = cont.owner
scene = logic.getCurrentScene()
player = scene.objects['networkQuad']
def setup():
    logic.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logic.serverIP = socket.gethostname()
    print(logic.serverIP)
    logic.myIP = socket.gethostname()
    logic.serverPort = 5068
    logic.server.connect((logic.serverIP, logic.serverPort))

def run():
    # maintains a list of possible input streams
    sockets_list = [logic.server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[],0.0)
    for socks in read_sockets:
        messageIn = socks.recv(2048)
        messageIn = pickle.loads(messageIn)
        player.position = messageIn['position']
        player.orientation = messageIn['rotation']
        
    out = {"origin":logic.myIP,"subject":"positionUpdate","position":list(own.position),"rotation":[list(own.orientation[0]),list(own.orientation[1]),list(own.orientation[2])]}
    messageOut = pickle.dumps(out)
    logic.server.send(messageOut)
def main():
    if hasattr(logic, 'networkReady'):
        run()
    else:
        setup()
    logic.networkReady = True
main()