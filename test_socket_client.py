import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
current_ip = input()
client.connect((str(current_ip), 2050))

while (True):
    data = client.recv(1024)
    print(data.decode("utf-8"))
    client.send(input().encode("utf-8"))