from lxml import *
from xml.dom import *
from xml.dom.minidom import parseString
from bluetooth import *
from serial import *
import time

server_addr = "B:27:EB:01:B1:FF"
port = 1
backlog = 1
server_sock = BluetoothSocket(RFCOMM)
server_sock.setblocking(True)
server_sock.bind((server_addr, port))
server_sock.listen(backlog)
print("lancement application")
client_socket, address = server_sock.accept()


def analyse_xml(root):
    if not root.hasChildNodes():
        ChangementAffichage(root.nodeValue, root.parentNode.nodeName)
    else : 
        for node in root.childNodes :
            analyse_xml(node)


def ChangementAffichage(a,b):
        print(a, " ----", b)
        if(b == "nom"):
            print("prout")
        

while 1:
    try:
        data = client_socket.recv(1024).decode('utf-8')
        root = parseString(data)
        print(root)
        analyse_xml(root)
    except btcommon.BluetoothError :
        client_socket, address = server_sock.accept() 

