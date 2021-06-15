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
    print("size  -> ", len(chess_x), ", ", len(chess_y))
    size_x = len(chess_x)
    size_y = len(chess_y)
    if size_y == 32 and size_x == 32:
        print("Valid Image")
    else:
        print("size_y == 32 and size_x == 32 isn't satisfied!")
        return -777
    up = min(chess_y)
    down = max(chess_y)
    left = min(chess_x)
    right = max(chess_x)
    print("board ->", up, ", ", down, ", ", left, ", ", right)
    cube_width = round((down - up)/9.0)
    cube_height = round((right - left)/8.0)
    print("cube  -> ", cube_width, ", ", cube_height)

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

    for i in range(9):
        print(__board[i])

    __board_CN = []
    for i in range(9):
        __row = []
        for j in range(10):
            __row.append(load_data.int2cn(0))
        __board_CN.append(__row)

    # print(chess_int)
    print(" ")

    for index_cn in range(size_x):
        x = round((chess_x[index_cn] - left) / cube_width)
        y = round((chess_y[index_cn] - up) / cube_height)
        str_cn = load_data.int2cn(chess_int[index_cn] + 1)
        __board_CN[x][y] = str_cn

    for i in range(9):
        print(__board_CN[i])


def outOfRadius(width, height):
    img_width = Global_Params.M_norm_size
    img_height = Global_Params.M_norm_size
    radius = Global_Params.M_norm_size/2
    if (width - radius)*(width - radius) + (height - radius)*(height - radius) > radius*radius:
        return True
    return False



# def cal_axis(input_x, input_y):
#     x = round((input_x - left)/cube_width)
#     y = round((input_y - up)/cube_height)
#     return x, y

