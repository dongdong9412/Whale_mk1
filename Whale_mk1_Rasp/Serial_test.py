import Packet
import serial

connect_flag = False
ser = serial.Serial("COM3", 115200, timeout=1)
if ser.is_open:
    print("Serial Connected..")
else:
    print("Please Check Serial Port.")

Packet.Packet_Init(ser)

print("Hello")
