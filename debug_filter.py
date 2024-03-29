# -*- coding: utf-8 -*-

from keras.utils.np_utils import to_categorical

import Global_Params
import algorithm
import filter
from load_data import docuChessInfo
from load_data import norm_size
from load_data import str2int
from load_data import CHESS_TABLE
import CNN_train
import CNN_train_w
import numpy as np
import tensorflow as tf
import cv2
import os
from keras.preprocessing.image import img_to_array
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Activation
from keras.layers import Dense, Dropout, Flatten
from keras.preprocessing.image import ImageDataGenerator
# from imutils import paths
import sys
sys.dont_write_bytecode = True


def RgbMedianFilter(img_set, size):
    """
    对RGB图片集做中值滤波（暂时只考虑了奇数大小的窗口，如3x3、5x5）
    (中值滤波好像作用不大)
    :param img_set: 图片集, shape = [num, height, width, 3]
    :param size:    中值滤波窗口大小(size, size)
    :return: 中值滤波后的图片集
    """
    num = img_set.shape[0]
    height = img_set.shape[1]
    width = img_set.shape[2]
    filted_img_set = np.zeros((num, height, width, 3))
    edge = (int)(size/2)
    idx = 0
    for img in img_set:
        for i in range(height):
            for j in range(width):
                if i < edge or i > height-edge-1 or j < edge or j > width-edge-1:
                    filted_img_set[idx, i, j, :] = img[i, j, :]
                else:
                    for color in range(3):
                        filted_img_set[idx, i, j, color] = np.median(img[i-edge:i+edge, j-edge:j+edge, color])
        cv2.imshow("img", img/255.0)
        cv2.imshow("filted_img", filted_img_set[idx]/255.0)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        idx += 1

    return filted_img_set

def RedBlackBoost(img_set, IMAGE_SHOW_OR_NOT, IMAGE_SHOW_FREQUENCY):
    '''
    增强图片中的红黑色（红色棋子增强红色，黑色棋子增强黑色）
    :param img_set: 图片集, shape = [num, height, width, 3]
    :return: 处理后的图片集
    '''
    num = img_set.shape[0]
    height = img_set.shape[1]
    width = img_set.shape[2]
    boosted_img_set = np.zeros((num, height, width, 3))
    hsv_img = np.zeros((height, width, 3))
    threshold = 0.02
    idx = 0
    count = 0
    radius = Global_Params.M_norm_size/2
    mid =Global_Params.M_norm_size/2.0
    mid = int(mid)
    for img in img_set:
        count += 1
        red_cnt = 0
        red_flag = False
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for i in range(height):
            for j in range(width):
                if ((0 <= hsv_img[i, j, 0] <= 10) or (310 <= hsv_img[i, j, 0] <= 360)) and (70 <= hsv_img[i, j, 1]*255 <= 255) and (50 <= hsv_img[i, j, 2] <= 255):
                    red_cnt += 1
                    if red_cnt >= threshold * height * width:
                        red_flag = True
                        break
            if red_flag is True:
                break

        if red_flag is True:    # 红棋子红色增强
            # print("RedBlackBoost   \t\t<", count, ">   \t\tred")
            for i in range(height):
                for j in range(width):
                    if algorithm.outOfRadius(j, i):
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
                        continue
                    if ((0 <= hsv_img[i, j, 0] <= 17) or (345 <= hsv_img[i, j, 0] <= 360)) and \
                            (66.0 <= hsv_img[i, j, 1]*255 <= 255) and (33.0 <= hsv_img[i, j, 2] <= 255):
                        boosted_img_set[idx, i, j, :] = [0, 0, 255]
                    else:
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
        else:                   # 黑棋子黑色增强
            # print("RedBlackBoost   \t\t<", count, ">   \t\tblack")
            for i in range(height):
                for j in range(width):
                    if algorithm.outOfRadius(j, i):
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
                        continue
                    if (0 <= hsv_img[i, j, 0] <= 360) and \
                            (0 <= hsv_img[i, j, 1]*255 <= 255) and (0 <= hsv_img[i, j, 2] <= 70):
                        boosted_img_set[idx, i, j, :] = [0, 0, 0]
                    else:
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
        print("RedBlackBoost Processing...")
        print("hsv_img[mid, mid, :] -> ", hsv_img[mid, mid, :])
        cv2.imshow("img_" + str(idx), img/255.0)
        cv2.imshow("boosted_img_" + str(idx), boosted_img_set[idx]/255.0)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        idx += 1

    del img_set
    return boosted_img_set


def load_data(image_paths, norm_size):
    data = []
    label = []
    test_data = []
    test_label = []

    classes = Global_Params.M_num_classes

    count_image = 0
    for each_image in image_paths:
        count_image += 1
        print(each_image)
        image = cv2.imread(each_image)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)
        maker = str2int(each_image.split(os.path.sep)[-2])
        label.append(maker)
        if count_image % 10 == 0:
            test_data.append(image)
            test_label.append(maker)

    data = np.array(data)
    print("data shape      = ", data.shape, " ===============================")
    data = RedBlackBoost(data, True, 30)
    data = data/255.0
    label = np.array(label)
    label = to_categorical(label, num_classes=classes)

    print("Data loaded.")
    return data, label, test_data, test_label


def main(): # 主函数
    pathChessChoose = Global_Params.M_data_per_360_path
    all_chess_data_path = docuChessInfo(pathChessChoose)
    data, label, test_data, test_label = load_data(all_chess_data_path, norm_size)

# 调用函数
if __name__ == '__main__':
    main()
