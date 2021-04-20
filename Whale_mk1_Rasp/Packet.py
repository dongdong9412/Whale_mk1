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
    result[3] = (packet_buf) & 0x00FF
    return result

def decode(packet):
    if check_checksum(packet):
        rw_buf = (packet >> 30) & 0x03
        id_buf = (packet >> 24) & 0x3F
        data_buf = (packet >> 8) & 0xFFFF

        return rw_buf, id_buf, data_buf
    else:
        print("Checksum Error!!")

if __name__ == '__main__':
    