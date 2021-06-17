# -*- coding: utf-8 -*-

"""
file: service.py
socket service
"""

import socket
import threading
import time
import sys
import Global_Params

HOST = Global_Params.M_HOST_TEST
PORT = Global_Params.M_PORT_TEST

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # init
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT)) # bonding
        s.listen(10) # monitor, backlog = 10
        # s.setblocking(True)
        # default value is True, if False, program throw an error if accept and recv have no data

    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Waiting connection...")

    while True:
        conn, addr = s.accept()
        # return (conn, address)
        # s.accept_ex(), have a return value, 0 is success and code if failure
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()
        # start a new thread, this line only execute once


def deal_data(conn, addr):
    print("Accept new connection from {0}".format(addr))
    databack = ("Hi " + format(addr) + ", Welcome to the server! ").encode()
    conn.send(databack)
    while True:
        data = conn.recv(1024) # 1024 is the longest length of string
        print('{0} client send data is {1}'.format(addr, data.decode()))
        # time.sleep(1)
        if data.decode() == "exit" or not data:
            print('{0} connection close'.format(addr))
            conn.send(bytes('Connection closed!'.encode("UTF-8")))
            break
        conn.send(bytes('Hello, {0}'.format(data.decode()), "UTF-8"))
    conn.close()


if __name__ == '__main__':
    socket_service()