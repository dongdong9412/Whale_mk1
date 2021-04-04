from socket import *
import cv2
import numpy
from queue import Queue

def encoding_image(queue):
    capture = cv2.VideoCapture(-1)

    while True:
        ret, frame = capture.read()

        if ret == False:
            continue

        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)

        data = numpy.array(imgencode)
        stringData = data.tostring()

        queue.put(stringData)

        key = cv2.waitKey(1)
        if key == 27:
            break
        # cv2.imshow('image', frame)

def transfer_image(client_socket, addr, queue):
    print('Connected by :', addr[0], ':', addr[1]) 

    while True:
        try:
            data = client_socket.recv(1)
            print(data)
            if not data:
                break
            elif data == '0':
                print("Control Area")
            elif data == '1':
                stringData = queue.get()
                client_socket.send(str(len(stringData)).ljust(16).encode())
                client_socket.send(stringData)
        
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
    client_socket.close()

        