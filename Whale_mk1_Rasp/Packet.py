import struct
from queue import Queue
import time

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


def rx_Task(ser, rx_queue, whaleInfo):
    while whaleInfo['uartConnect']:
        rx_packet = ser.read_until(size=4)
        if not rx_queue.full():
            rx_queue.put(rx_packet)

def tx_Task(ser, tx_queue, whaleInfo):
    while whaleInfo['uartConnect']:
        if not tx_queue.empty():
            tx_packet = tx_queue.get()
            print("Tx: ", decode(tx_packet))
            ser.write(tx_packet)

def execute_Command(rx_queue, tx_queue, whaleInfo):
    while whaleInfo['uartConnect']:
        tx_rw = 0
        tx_id = 0
        tx_data = 0
        tx_packet = encode(tx_rw, tx_id, tx_data)
        tx_queue.put(tx_packet)
        if not rx_queue.empty():
            rx_packet = rx_queue.get()
            rw, id, data = decode(rx_packet)
            print("Rx: ", rw, id, data)
            print(whaleInfo['uartConnect'], whaleInfo['errorCount'])
            # Read Command #
            if rw == 0:
                # Software Version #
                if id == 0:
                    tx_rw = 2
                    tx_id = 0
                    tx_data = 1
                    tx_packet = encode(tx_rw, tx_id, tx_data)
                    tx_queue.put(tx_packet)

            # Write Command #

            # Answer Command #
            if rw == 2:
                if id == 0:
                    if data == 1:
                        if whaleInfo['errorCount'] > 0:
                            whaleInfo['errorCount'] = whaleInfo['errorCount'] - 1
                            tx_rw = 2
                        tx_id = 0
                        tx_data = 0
                        tx_packet = encode(tx_rw, tx_id, tx_data)
                        tx_queue.put(tx_packet)
                    else:
                        whaleInfo['errorCount'] = whaleInfo['errorCount'] + 1
                        if whaleInfo['errorCount'] == 1000:
                            whaleInfo['uartConnect'] = False
            
def uartInit(ser, whaleInfo):
    while not whaleInfo['uartConnect']:
        time.sleep(1)
        tx_rw = 0
        tx_id = 0
        tx_data = 1
        tx_packet = encode(tx_rw, tx_id, tx_data)
        ser.write(tx_packet)

        rx_packet = ser.read_until(size=4)
        rx_rw, rx_id, rx_data = decode(rx_packet)

        if rx_rw == 0:
            if rx_id == 0:
                tx_rw = 2
                tx_id = 0
                tx_data = 1
                tx_packet = encode(tx_rw, tx_id, tx_data)
                ser.write(tx_packet)
        elif rx_rw == 2:
            if rx_id == 0:
                if rx_data == 1:
                    whaleInfo['uartConnect'] = True
        
