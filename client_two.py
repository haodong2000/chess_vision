# -*- coding: utf-8 -*-

import socket
import sys

import Global_Params

HOST = Global_Params.M_HOST_TEST
PORT = Global_Params.M_PORT_TEST

def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print(s.recv(1024))  # 目的在于接受：Accept new connection from (...
    while 1:
        data = input("please input work: ").encode()
        s.send(data)
        # return the length of string has sent
        # s.sendall() try all data, call s.send() in recursion
        print("from server to c-two: ", s.recv(1024))
        if data.decode() == "exit":
            break
    s.close()


if __name__ == '__main__':
    socket_client()