from socket import *
import numpy as np
import cv2
import Packet
import struct

import time

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

#Host = 'DongDong9412.iptime.org'
Host = '127.0.0.1'
Port = 8080

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((Host, Port))

command = 0
rw = 1
id = 0
data = 0
while True:
    message = str(command)
    print(message)
    client_socket.send(message.encode())

    if message == '0':
        tx_buf = bytearray(2)
        tx_buf = Packet.encode(rw, id, data)
  
        data = (data + 1) % 256
        if data % 10 == 0:
            id = (id + 1) % 7
        client_socket.send(tx_buf)
        time.sleep(1)
    elif message == '1':
        length = recvall(client_socket, 16)
        stringData = recvall(client_socket, int(length))
        data = np.frombuffer(stringData, dtype='uint8')

        decimg=cv2.imdecode(data, 1)
        cv2.imshow('Image', decimg)
    
client_socket.close()