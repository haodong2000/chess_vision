# -*- coding: utf-8 -*-

import socket
import sys

HOST = "127.0.0.1"
PORT = 6666

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
        print("from server to client: ", s.recv(1024).decode())
        if data.decode() == "exit":
            break
    s.close()


if __name__ == '__main__':
    socket_client()