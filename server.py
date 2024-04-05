import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 12345))
server.listen(5)

sockets_list = [server]
clients = {}

print("Server started, waiting for connections...")

def broadcast_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message)

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])
    
    for sock in read_sockets:
        if sock == server:
            client_socket, client_address = server.accept()
            sockets_list.append(client_socket)
            print(f"Client {client_address} connected")
            client_socket.send("Welcome to the chat! Please enter your name: ".encode())
        else:
            try:
                data = sock.recv(1024).decode()
                if data:
                    if sock not in clients:
                        clients[sock] = data
                        broadcast_message(sock, f"{data} joined the chat\n".encode())
                        print(f"New client: {data}")
                    else:
                        message = f"{clients[sock]}: {data}"
                        broadcast_message(sock, message.encode())
                        print(message)

            except Exception as e:
                print(f"Client {clients[sock]} has left the chat")
                broadcast_message(sock, f"{clients[sock]} has left the chat\n".encode())
                sockets_list.remove(sock)
                del clients[sock]
                continue
