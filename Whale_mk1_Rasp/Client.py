from socket import *
import numpy as np
import cv2

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

Host = 'DongDong9412.iptime.org'
Port = 8080

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((Host, Port))

command = 0
while True:
    message = str(command)
    print(message)
    client_socket.send(message.encode())

    if message == '1':
        length = recvall(client_socket, 16)
        stringData = recvall(client_socket, int(length))
        data = np.frombuffer(stringData, dtype='uint8')

        decimg=cv2.imdecode(data, 1)
        cv2.imshow('Image', decimg)

    command = (command + 1) % 2
    key = cv2.waitKey(1)
    if key == 27:
        break
    
client_socket.close()