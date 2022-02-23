# -*- coding: utf-8 -*-

"""
file: service.py
socket service
"""

import socket
import threading
import time
import sys

import algorithm

# HOST = "127.0.0.1"
# PORT = 6666
HOST = "127.0.0.1"
PORT = 9999

# __isStepGenerate = False


def socket_service():
    # __isStepGenerate = False
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
    databack = ("Hello, client from {0}".format(addr)).encode()
    conn.send(databack)
    while True:
        data = conn.recv(1024) # 1024 is the longest length of string
        print('{0} client send data is {1}'.format(addr, data.decode()))
        time.sleep(0.5)
        if data.decode() == "exit" or not data:
            print('{0} connection close'.format(addr))
            conn.send(bytes('Connection closed!'.encode("UTF-8")))
            break
        chess_board_string = data.decode()
        current_matrix, which_turn = algorithm.string2matrix(str(chess_board_string))
        backMsg_example = "1,4041"
        backMsg = bytes(backMsg_example.encode("UTF-8"))
        conn.send(backMsg)
        # conn.send(bytes(backMsg, "UTF-8"))
        # conn.send(bytes("Hello QT, from: {0}", "UTF-8"))
    conn.close()


if __name__ == '__main__':
    socket_service()
