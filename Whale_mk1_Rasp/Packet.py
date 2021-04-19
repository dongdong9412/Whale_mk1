import struct
from queue import Queue

def create_checksum(packet):
    buf_1 = (packet >> 24) & 0xFF
    buf_2 = (packet >> 16) & 0xFF
    buf_3 = (packet >> 8) & 0xFF
    checksum = buf_1 + buf_2 + buf_3
    checksum = (~checksum + 1)

    packet |= (checksum & 0xFF)

    return packet

def check_checksum(packet):
    buf_1 = (packet >> 24) & 0xFF
    buf_2 = (packet >> 16) & 0xFF
    buf_3 = (packet >> 8) & 0xFF
    buf_4 = packet & 0xFF

    checksum = buf_1 + buf_2 + buf_3 + buf_4
    checksum = checksum & 0xFF

    if checksum == 0:
        return True
    else:
        return False

def encode(rw, id, data):
    packet_buf = (rw << 30) | (id << 24) | (data << 8)
    packet_buf = create_checksum(packet_buf)

    result = bytearray(4)
    result[0] = (packet_buf >> 24) & 0x00FF
    result[1] = (packet_buf >> 16) & 0x00FF
    result[2] = (packet_buf >> 8) & 0x00FF
    result[3] = (packet_buf >> 0) & 0x00FF
    return result

def decode(packet):
    packet_int = int.from_bytes(packet, "big", signed=False)

    if check_checksum(packet_int):
        rw_buf = (packet_int >> 30) & 0x03
        id_buf = (packet_int >> 24) & 0x3F
        data_buf = (packet_int >> 8) & 0xFFFF

        return rw_buf, id_buf, data_buf
    else:
        print("Checksum Error!!")


def rx_Task(ser):
    connect_flag = 0

    rx_packet = ser.read_until(size=4)

    rw, id, data = decode(rx_packet)

    print(rx_packet, rw, id, data)

    if rw == 0:
        if id == 0:
            rw = 2
            id = 0
            data = 0
            tx_packet = encode(rw, id, data)
            ser.write(tx_packet)
            #print("Send Data: ", tx_packet)
    elif rw == 2:
        if id == 0:
            if data == 0:
                connect_flag = True

    return connect_flag

def tx_Task(ser, serviceID):
    if serviceID == 0:
        rw = 0
        id = 0
        data = 0xFFFF
        tx_packet = encode(rw, id, data)
        ser.write(tx_packet)

def Packet_Init(ser):
    connect_flag = False
    
    while not connect_flag:
        tx_Task(ser, 0)
        connect_flag = rx_Task(ser)
    
        tx_Task(ser, 0)
        connect_flag = rx_Task(ser)