import Packet
import serial
from queue import Queue
from threading import Thread

key

def key_input():
    global key
    key = input()
    print(key)

rx_queue = Queue()
tx_queue = Queue()

whaleInfo = {
    'uartConnect':False,
    'errorCount':0
}

connect_flag = False
ser = serial.Serial("COM3", 115200, timeout=1)
if ser.is_open:
    print("Serial Connected..")
else:
    print("Please Check Serial Port.")

Packet.uartInit(ser, whaleInfo)
print("Connect")

Task_Rx = Thread(target=Packet.rx_Task, args=(ser, rx_queue, whaleInfo,))

Task_Tx = Thread(target=Packet.tx_Task, args=(ser, tx_queue, whaleInfo,))

Task_Execute = Thread(target=Packet.execute_Command, args=(rx_queue, tx_queue, whaleInfo,))

Task_Keyboard = Thread(target=key_input)


Task_Rx.start()
Task_Tx.start()
Task_Execute.start()
Task_Keyboard.start()

Task_Rx.join()
Task_Tx.join()
Task_Execute.join()
Task_Keyboard.join()