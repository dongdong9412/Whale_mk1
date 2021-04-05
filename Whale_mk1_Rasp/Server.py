from socket import *
import cv2
import numpy
from queue import Queue
import Packet

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

        # cv2.imshow('image', frame)

def Gateway_task(client_socket, addr, image_queue, command_queue):
    print('Connected by :', addr[0], ':', addr[1]) 

    while True:
        try:
            data = client_socket.recv(1)
            data = data.decode()
            if not data:
                break
            elif data == '0':
                # Control Area #
                rx_buf = client_socket.recv(2)
                packet_buf = int.from_bytes(rx_buf, "big")
                command_queue.put(packet_buf)
                rw, id, data = Packet.decode(packet_buf)
                print(rw, id, data)
            elif data == '1':
                # Monitor Area #
                stringData = image_queue.get()
                client_socket.send(str(len(stringData)).ljust(16).encode())
                client_socket.send(stringData)
        
        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break
    client_socket.close()

def Serial_task(serial, command_queue):
    while True:
        temp_buf = command_queue.get()
        rw, id, data = Packet.decode(temp_buf)
        tx_buf = Packet.encode(rw, id, data)
        serial.write(tx_buf)
        