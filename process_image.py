# -*- coding: utf-8 -*-

from keras.utils.np_utils import to_categorical
import filter
from load_data import docuChessInfo
from load_data import norm_size
from load_data import str2int
from load_data import CHESS_TABLE
import CNN_train
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
from imutils import paths
import sys
sys.dont_write_bytecode = True

def load_data(image_paths, norm_size):
    data = []
    label = []

    for each_image in image_paths:
        print(each_image)
        image = cv2.imread(each_image)
        image = cv2.resize(image, (norm_size, norm_size))
        image = img_to_array(image)
        data.append(image)
        maker = str2int(each_image.split(os.path.sep)[-2])
        label.append(maker)

    data = np.array(data)
    data = filter.RedBlackBoost(data)
    data = data/255.0
    label = np.array(label)
    label = to_categorical(label, num_classes=14+1)

    index = np.arange(data.shape[0])
    np.random.shuffle(index)
    data = data[index, :, :, :]
    label = label[index, :]

    print("Data loaded.")
    return data, label




def main(): # 主函数
    pathChessChoose = "./data_360"  # 人为选择的数据的路径
    all_chess_data_path = docuChessInfo(pathChessChoose)
    data, label = load_data(all_chess_data_path, norm_size)
    model = CNN_train.TrainCnnModel(data, label, norm_size)
    model.save("modelSave/boost_cnn_model.h5")
    print("Model saved.")

# 调用函数
if __name__ == '__main__':
    main()