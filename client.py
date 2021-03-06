# client
# Aleksis Vanags
# 31/10/2021

import socket
import threading

HEADER = 1024
FORMAT = "utf-8"
PORT = 5050
SERVER = "192.168.1.101"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
USERNAME_MESSAGE = "!USERNAME"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    """Allows the client to send a message to the server"""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def recieve():
    """Allows the client to recive new messages from the server"""
    while True:
        print(client.recv(HEADER).decode(FORMAT))


thread = threading.Thread(target=recieve)
thread.start()
send(USERNAME_MESSAGE + " " + input("Enter your username:   "))
while True:
    send(input())
