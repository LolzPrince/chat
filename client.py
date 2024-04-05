import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 12345))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

thread = threading.Thread(target=receive_messages)
thread.start()

while True:
    message = input()
    client.send(message.encode())
