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

import cv2
import datetime
import os
from PIL import Image

import algorithm
import circle_multi
import Global_Params

import tensorflow as tf
import keras
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# os.environ["TF_GPU_ALLOCATOR"] = "cuda_malloc_async"
config = tf.compat.v1.ConfigProto(log_device_placement=True)
# dynamically grow the memory used on the GPU
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.5
sess = tf.compat.v1.Session(config=config)
# set this TensorFlow session as the default session for Keras.
tf.compat.v1.keras.backend.set_session(sess)

HOST = Global_Params.M_HOST_TEST
PORT = Global_Params.M_PORT_TEST


def init_webcam():
    print(cv2.__version__)
    capture = cv2.VideoCapture(0) # on Webcam
    default_size = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("old size: ", default_size)

    # set frame height and width
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    new_size = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("new size: ", new_size)

    cur_count = 0
    total_count = Global_Params.M_Test_Webcam
    test_ImageStore = Global_Params.M_imageProcessTest_path

    while(True):
        ret, origin_image = capture.read()

        temp_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        temp_name = temp_name + "_" + str(cur_count) + ".jpg"
        cur_count += 1
        print(temp_name, "  <", cur_count, "/", total_count, ">")
        cv2.imshow(temp_name, origin_image) # imshow

        mode = 0
        if mode == 0:
            flag = cv2.waitKey(0) # press enter to save image, and Esc to quit
            if flag == 27:
                print("Quit init_webcam()")
                cv2.destroyWindow(temp_name)
                break
            if flag != 13 and flag != 27:
                cv2.destroyWindow(temp_name)
                continue
        elif mode == 1:
            save_path = os.path.join(test_ImageStore, temp_name)
            cv2.imwrite(save_path, origin_image)
            cv2.destroyWindow(temp_name)
            print(save_path, "   <saved>")
            break
        else:
            print("mode error!!!!!  server_one.py  line:71")
            break


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
    databack = ("Hi QT " + format(addr) + ", Welcome to the server! ").encode()
    conn.send(databack)
    count = 0
    while True:
        data = conn.recv(1024) # 1024 is the longest length of string
        print('{0} client send data is {1}'.format(addr, data.decode()))
        time.sleep(0.05)
        if data.decode() == "exit" or not data:
            print('{0} connection close'.format(addr))
            conn.send(bytes('Connection closed!'.encode("UTF-8")))
            break
        time.sleep(0.05)
        __curBoard = []
        count += 1
        Global_Params.M_Circle_FLAG = True
        __curBoard = circle_multi.generate_board_message(count)
        Global_Params.M_Circle_FLAG = False
        time.sleep(4)
        if len(__curBoard) > 0:
            backMsg = generate_message(__curBoard)
        else:
            backMsg = "Null"
        conn.send(bytes(backMsg, "UTF-8"))
        # conn.send(bytes("Hello QT, from: {0}", "UTF-8"))
    conn.close()


def generate_message(__curBoard):
    ans = ""
    size = len(__curBoard)
    for index in range(size):
        ans += __curBoard[index]
    return ans


if __name__ == '__main__':
    # init_webcam()
    socket_service()
