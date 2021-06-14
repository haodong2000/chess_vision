# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mp # mp 用于读取图片
from PIL import Image
import numpy as np
import math
import os

from imageProcess import preprocess
from chessInfo import docuChessInfo

from load_data import str2int

import sys
sys.dont_write_bytecode = True

img_h = 620 # 默认图片高度
img_w = 620 # 默认图片宽度
channel = 1 # 图片维度，由于经过灰度处理，故为一维
numberOfTrain = 12
numberOfTest = 8

pathOfData = "./data_360" # 所选的十个棋子的数据路径
chessInfoMatch = [] # 人名对
chessPathMatch = [] # 路径对
idNum = [] # ID

def readImage():

    for i in range(14):
        idNum.append(str(i))

    files = os.listdir(pathOfData) # 遍历文件夹
    index = 0

    # 建立txt文件记录数据
    chess_train_info_txt = "./chessTrainInfo.txt"
    ftrain = open(chess_train_info_txt, 'w')
    chess_test_info_txt = "./chessTestInfo.txt"
    ftest = open(chess_test_info_txt, 'w')

    for fileName in files:
        chessInfoMatch.append([str(index), fileName]) # 姓名与数字相匹配, 一共10组
        tempDir = pathOfData + "/" + fileName
        tempFile = os.listdir(tempDir) # 遍历
        for tempFileNames in tempFile:
            tempFilePath = pathOfData + "/" + fileName + "/" + tempFileNames
            chessPathMatch.append([idNum[index], tempFilePath]) # 路径与数字（即姓名）匹配, 一共10*359组
        index += 1

    imageIndex = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 记录每个数据集中的图片数量

    x_train = []
    y_train = []
    x_test = []
    y_test = []

    for x in chessPathMatch:
        nameIndex = int(x[0])
        if imageIndex[nameIndex] < numberOfTrain:
            x_train.append(x[1]) # 存放路径
            y_train.append(str2int(x[1].split(os.path.sep)[-2])) # 存放路径对应照片的label（姓名）
            imageIndex[nameIndex] += 1 # 数量+1
            docu_train_str = str2int(x[1].split(os.path.sep)[-2])+ " -> " + x[1] + "\n"
            ftrain.write(docu_train_str)
        else:
            x_test.append(x[1]) # 41及以后视为测试及数据
            y_test.append(idNum[nameIndex]) # 存放路径对应照片的label（姓名）
            docu_test_str =  x[0] + " -> " + x[1] + "\n"
            ftest.write(docu_test_str)

    print("image data x_train, y_train, x_test, y_test done!")
    return x_train, y_train, x_test, y_test


# 根据路径读入所有的图片，同时根据全局规定的图片尺寸要求进行裁剪,并按照模型输入要求reshape
def returnImage(x_train, x_test):
    X_train = [] # empty array
    for i in range(len(x_train)):
        printStringTrain = "x_train reading image data, current position: " + str(i)
        print(printStringTrain)
        X_train.append(preprocess(mp.imread(x_train[i]), img_h, img_w)) # 读取图片，preprocess为图像预处理
    X_train = np.array(X_train) # 数组化处理
    print("X_train.shape is = ", X_train.shape) # (...,128,128)
    X_train = X_train.reshape(X_train.shape[0], X_train[0].shape[0], X_train[0].shape[1], channel).astype('float32')
    # 与模型相匹配啦！
    # 需要reshape一下下！

    X_test = [] # 同理
    for i in range(len(x_test)):
        printStringTest = "x_test reading image data, current position: " + str(i)
        print(printStringTest)
        X_test.append(preprocess(mp.imread(x_test[i]), img_h, img_w))
    X_test = np.array(X_test)
    X_test = X_test.reshape(X_test.shape[0], X_test[0].shape[0], X_test[0].shape[1], channel).astype('float32')
    print("X_test.shape = ", X_test.shape)
    print("image read done!")
    return X_train, X_test


def main():
    docuChessInfo()
    x_train, y_train, x_test, y_test = readImage()
    x_train, x_test = returnImage(x_train, x_test)

# 调用函数
if __name__ == '__main__':
    main()
