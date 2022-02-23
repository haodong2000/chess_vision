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


# @TODO class step and generate backMsg


def chess_board_generator(chess_x, chess_y, chess_int):
    size_x = len(chess_x)
    size_y = len(chess_y)
    up = 0
    down = 0
    left = 0
    right = 0
    if size_x == 0 and size_y == 0:
        print("20210719  ->   size_x == 0 and size_y == 0")
    else:
        up = min(chess_y)
        down = max(chess_y)
        left = min(chess_x)
        right = max(chess_x)
    print("board ->", up, ", ", down, ", ", left, ", ", right)
    cube_height = round((down - up)/8.0)
    cube_width = round((right - left)/9.0)
    print("cube  -> ", cube_width, ", ", cube_height)

    up = Global_Params.M_up
    down = Global_Params.M_down
    left = Global_Params.M_left
    right = Global_Params.M_right
    cube_height = round((down - up)/8.0)
    cube_width = round((right - left)/9.0)

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
        __board[y][x] = "XX"
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

    __lastBoard = []
    __curBoard = []

    for index_cn in range(size_x):
        x = round((chess_x[index_cn] - left) / cube_width)
        y = round((chess_y[index_cn] - up) / cube_height)
        str_cn = load_data.int2cn(chess_int[index_cn] + 1)
        __board_CN[y][x] = str_cn
        msg = load_data.int2str(chess_int[index_cn]) + str(y) + str(x) + ", "
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


def string2matrix(string):
    print("[string2matrix] string type ->", type(string))
    matrix, matrix_cn = [], []
    for i in range(10):
        row = []
        row_cn = []
        for j in range(10):
            row.append(-1)
            row_cn.append(load_data.CHESS_CN[0])
        matrix.append(row)
        matrix_cn.append(row_cn)
    start, jump = 0, 0
    now_chess, now_pos, chess_str, pos_x_str, pos_y_str = False, False, [], '', ''
    chess, pos_x, pos_y = 0, 0, 0
    for index in range(len(string)):
        if string[index] == '>' and start == 0:
            start = index
            continue
        if start == 0:
            continue
        if jump > 0:
            jump -= 1
            continue
        if string[index] >= '0' and string[index] <= '9':
            chess_str.append(string[index])
        elif string[index] == ',':
            now_chess = True
            if len(chess_str) == 2:
                chess = 10 + (int(chess_str[1]) - int('0'))
            else:
                chess = int(chess_str[0]) - int('0')
            pos_x = int(string[index + 1]) - int('0')
            pos_y = int(string[index + 2]) - int('0')
            matrix[pos_x][pos_y] = chess
            # print(pos_x, pos_y, chess)
            jump = 2
            chess_str = []
    for i in range(10):
        for j in range(10):
            if matrix[i][j] != 0:
                matrix_cn[i][j] = load_data.CHESS_CN[matrix[i][j]]
    for i in range(9):
        print(matrix_cn[i])
    return matrix


if __name__ == '__main__':
    string = "connection<2>0,00;0,01;0,02;7,03;0,04;0,05;14,06;0,07;0,08;0,09;0,10;0,11;0,12;0,13;0,14;0,15;0,16;0,17;" \
             "0,18;0,19;3,20;0,21;4,22;7,23;0,24;0,25;14,26;11,27;0,28;10,29;2,30;0,31;0,32;0,33;0,34;0,35;0,36;0,37;" \
             "0,38;9,39;1,40;0,41;0,42;4,43;0,44;6,45;0,46;13,47;0,48;8,49;2,50;0,51;0,52;0,53;0,54;0,55;0,56;0,57;5,58;" \
             "9,59;3,60;0,61;0,62;12,63;0,64;0,65;14,66;13,67;0,68;10,69;0,70;0,71;6,72;0,73;0,74;0,75;0,76;0,77;0,78;" \
             "0,79;0,80;0,81;5,82;7,83;0,84;0,85;14,86;11,87;0,88;12,89;"
    string2matrix(string)
