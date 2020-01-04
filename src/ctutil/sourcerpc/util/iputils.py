import socket
import struct


def ip2long(ipaddr):
    '''
    ip转换到long类型
    '''

    packed_ip = socket.inet_aton(ipaddr)
    return struct.unpack("!L", packed_ip)[0]

def long2ip(num):
    '''
    long类型转换到ip
    '''

    return socket.inet_ntoa(struct.pack('!L', num))
