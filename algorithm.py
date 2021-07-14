# -*-*- coding utf-8 -*-*-
# to hough circling and get chess image

import cv2
import os
import sys

import datetime

import numpy as np
from PIL import Image

import Global_Params
import load_data


def chess_board_generator(chess_x, chess_y, chess_int):
    size_x = len(chess_x)
    size_y = len(chess_y)
    up = min(chess_y)
    down = max(chess_y)
    left = min(chess_x)
    right = max(chess_x)
    # print("board ->", up, ", ", down, ", ", left, ", ", right)
    cube_width = round((down - up)/9.0)
    cube_height = round((right - left)/8.0)
    # print("cube  -> ", cube_width, ", ", cube_height)

    __board = []
    for i in range(9):
        __row = []
        for j in range(10):
            __row.append("__")
        __board.append(__row)

    # for i in range(9):
    #     print(__board[i][0:10])

    for index in range(size_x):
        x = round((chess_x[index] - left) / cube_width)
        y = round((chess_y[index] - up) / cube_height)
        __board[x][y] = "XX"
        # print(x, "", y)

    # print(__board)

    # for i in range(9):
    #     print(__board[i])

    __board_CN = []
    for i in range(9):
        __row = []
        for j in range(10):
            __row.append(load_data.int2cn(0))
        __board_CN.append(__row)

    # print(chess_int)
    print(" ")

    __lastBoard = []
    __curBoard = []

    for index_cn in range(size_x):
        x = round((chess_x[index_cn] - left) / cube_width)
        y = round((chess_y[index_cn] - up) / cube_height)
        str_cn = load_data.int2cn(chess_int[index_cn] + 1)
        __board_CN[x][y] = str_cn
        msg = load_data.int2str(chess_int[index_cn]) + str(x) + str(y) + ", "
        __curBoard.append(msg)

    for i in range(9):
        print(__board_CN[i])

    blackAlive = False
    redAlive = False
    for index_cn in range(size_x):
        if (chess_int[index_cn] + 1) == 1:
            blackAlive = True
        if (chess_int[index_cn] + 1) == 8:
            redAlive = True

    GameIsOn = blackAlive and redAlive

    whoWin = 2
    if GameIsOn == False:
        if blackAlive:
            whoWin = 0
        if redAlive:
            whoWin = 1

    return GameIsOn, whoWin, __curBoard


# def compare():
#     size_last = len(__lastBoard)
#     size_cur = len(__curBoard)
#     if size_cur != size_last:
#         return True
#
#     for index in range(size_cur):
#         cur_msg = __curBoard[index]
#         for index_2 in range(size_last):
#             if cur_msg != __lastBoard[index_2]:
#                 return True
#
#     __lastBoard.clear()
#     for index in range(size_cur):
#         cur_msg = __curBoard[index]
#         __lastBoard.append(cur_msg)
#     return False


def outOfRadius(width, height):
    img_width = Global_Params.M_norm_size
    img_height = Global_Params.M_norm_size
    radius = Global_Params.M_norm_size/2
    radius *= 0.90  # get rid of the circle edge of chesses
    if (width - radius)*(width - radius) + (height - radius)*(height - radius) > radius*radius:
        return True
    return False



# def cal_axis(input_x, input_y):
#     x = round((input_x - left)/cube_width)
#     y = round((input_y - up)/cube_height)
#     return x, y

