# server
# Aleksis Vanags
# 31/10/2021

import socket
import threading

HEADER = 1024
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"
USERNAME_MESSAGE = "!USERNAME"
REQUEST_HISTORY = "!HISTORY"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

users = {}
connections = []


def handle_client(conn, addr):
    """ Detect and handle messages for all seperate clients """
    all_messages = []
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                elif msg.startswith(USERNAME_MESSAGE):
                    users[addr] = msg.split(" ", 1)[1]
                    connections.append(conn)
                elif msg == REQUEST_HISTORY:
                    requestAllMessages(conn, all_messages)
                if not msg.startswith(USERNAME_MESSAGE) and msg != REQUEST_HISTORY:
                    all_messages.append(f"\n[{users[addr]}] {msg}")
                    print(f"[{users[addr]}] {msg}")
                    update_clients()
        except ConnectionResetError:
            connected = False
            print(f"[{users[addr]}] {DISCONNECT_MESSAGE}")
    users.pop(addr)
    connections.remove(conn)
    conn.close()


def start():
    """ Start the server """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def update_clients():
    """ Send new messages to all clients """
    for conn in connections:
        message = all_messages[-1].encode(FORMAT)
        conn.send(message)


def requestAllMessages(conn, all_messages):
    """ A new connection can see the message history using a special command """
    for message in all_messages:
        conn.send(message.encode(FORMAT))

print("[SERVER] server is starting...")
start()
