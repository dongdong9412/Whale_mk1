def create_checksum(packet):
    buf_1 = (packet >> 12) & 0x0F
    buf_2 = (packet >> 8) & 0x0F
    buf_3 = (packet >> 4) & 0x0F
    checksum = buf_1 + buf_2 + buf_3
    checksum = (~checksum + 1)

    packet |= (checksum & 0x0F)

    return packet

def check_checksum(packet):
    buf_1 = (packet >> 12) & 0x0F
    buf_2 = (packet >> 8) & 0x0F
    buf_3 = (packet >> 4) & 0x0F
    buf_4 = packet & 0x0F

    checksum = buf_1 + buf_2 + buf_3 + buf_4
    checksum = checksum & 0x0F

    if checksum == 0:
        return True
    else:
        return False

def encode(rw, id, data):
    packet_buf = (rw << 15) | (id << 12) | (data << 4)
    packet_buf = create_checksum(packet_buf)

    result = bytearray(2)
    result[0] = (packet_buf & 0xFF00) >> 8
    result[1] = (packet_buf & 0x00FF)
    return result

def decode(packet):
    if check_checksum(packet):
        rw_buf = (packet >> 15) & 0x01
        id_buf = (packet >> 12) & 0x07
        data_buf = (packet >> 4) & 0xFF

        return rw_buf, id_buf, data_buf
    else:
        print("Checksum Error!!")

