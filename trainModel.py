# -*- coding: utf-8 -*-

from keras.utils.np_utils import to_categorical

import Global_Params
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
import argparse


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ratio', default=7, type=int, help='train & test ratio')
    return parser.parse_args()


def load_data(image_paths, norm_size, ratio, show_boost=False):
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
        # data.append(image)
        maker = str2int(each_image.split(os.path.sep)[-2])
        # label.append(maker)
        if count_image % ratio == 0:
            test_data.append(image)
            test_label.append(maker)
        else:
            data.append(image)
            label.append(maker)

    data = np.array(data)
    print("data shape =", data.shape, "===============================")
    data = filter.RedBlackBoost(data, show_boost, 5, THREAD=16) # SHEN
    data = data/255.0
    label = np.array(label)
    label = to_categorical(label, num_classes=classes)

    test_data = np.array(test_data)
    print("test_data shape =", test_data.shape, "===============================")
    test_data = filter.RedBlackBoost(test_data, show_boost, 5, THREAD=16) # SHEN
    test_data = test_data/255.0
    test_label = np.array(test_label)
    test_label = to_categorical(test_label, num_classes=classes)

    index = np.arange(data.shape[0])
    np.random.shuffle(index)
    data = data[index, :, :, :]
    label = label[index, :]

    test_index = np.arange(test_data.shape[0])
    np.random.shuffle(test_index)
    test_data = test_data[test_index, :, :, :]
    test_label = test_label[test_index, :]

    print("Data loaded.")
    return data, label, test_data, test_label


def main(TEST_MODE, TRAIN_MODEL):
    user_input = get_user_input()
    if TEST_MODE:
        pathChessChoose = Global_Params.M_data_per_360_path  # data path
        all_chess_data_path = docuChessInfo(pathChessChoose)
        data, label, test_data, test_label = load_data(all_chess_data_path, norm_size, user_input.ratio, show_boost=True)
        return
    pathChessChoose = Global_Params.M_data_360_path  # data path
    all_chess_data_path = docuChessInfo(pathChessChoose)
    data, label, test_data, test_label = load_data(all_chess_data_path, norm_size, user_input.ratio, show_boost=False)
    if TRAIN_MODEL:
        CNN_train.TrainCnnModel(data, label, norm_size, test_data, test_label)
        CNN_train_w.trainModel(data, label, norm_size, test_data, test_label)


if __name__ == '__main__':
    main(TEST_MODE=False, TRAIN_MODEL=True)
