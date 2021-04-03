import serial
import Packet as pk
from threading import Thread
from socket import *
import cv2
import numpy
from queue import Queue
import Server

def encoding_image(queue):
    capture = cv2.VideoCapture(0)

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
            data = client_socket.recv(1024)

            if not data:
                break
            
            stringData = queue.get()
            client_socket.send(str(len(stringData)).ljust(16).encode())
            client_socket.sned(stringData)
        
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
    client_socket.close()

if __name__ == '__main__':
    while True:
        ser = serial.Serial("COM4", 115200, timeout=1)
        if ser.is_open:
            print("Serial Connected..")
            break
        else:
            print("Please Check Serial Port.")

    enclosure_queue = Queue()
    Host = 'DongDong9412.iptime.org'
    Port = 8080
    server_socket = socket(AF_INET, SOCK_STREAM) 
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', Port)) 
    server_socket.listen() 

    print("Server Start")
    client_socket, addr = server_socket.accept() 
    task1 = Thread(target=Server.encoding_image, args=(enclosure_queue))
    task1.start()

    task2 = Thread(target=Server.transfer_image, args=(client_socket, addr, enclosure_queue))
    task2.start()

    task1.join()
    task2.join()