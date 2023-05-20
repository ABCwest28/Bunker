import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostbyname_ex(socket.gethostname())[-1][-1])
server.bind((socket.gethostbyname_ex(socket.gethostname())[-1][-1], 2050))

server.listen()

while (True):
    user, address = server.accept()
    print("client connected")
    while (True):
        data = user.recv(1024)
        print(data.decode("utf-8"))
        #user.send(input().encode("utf-8"))
        #вызов функции и повторная прослушка - user.recv()