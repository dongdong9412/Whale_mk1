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
    command_queue = Queue()
    Host = '127.0.0.1'
#   Host = 'DongDong9412.iptime.org'
    Port = 8080
    server_socket = socket(AF_INET, SOCK_STREAM) 
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('', Port)) 
    server_socket.listen() 

    print("Server Start")
    client_socket, addr = server_socket.accept() 
    task1 = Thread(target=Server.encoding_image, args=(enclosure_queue, ))
    task1.start()

    task2 = Thread(target=Server.Gateway_task, args=(client_socket, addr, enclosure_queue, command_queue, ))
    task2.start()

    task3 = Thread(target=Server.Serial_task, args=(ser, command_queue, ))
    task3.start()

    task1.join()
    task2.join()
    task3.join()