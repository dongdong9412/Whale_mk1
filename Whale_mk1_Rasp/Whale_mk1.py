import serial
import Packet as pk
from threading import Thread
from socket import *
from queue import Queue
import Server

if __name__ == '__main__':
#    while True:
#        ser = serial.Serial("COM4", 115200, timeout=1)
#        if ser.is_open:
#            print("Serial Connected..")
#            break
#        else:
#            print("Please Check Serial Port.")

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