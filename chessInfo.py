# -*- coding: UTF-8 -*-
import tarfile
import os

import tensorflow as tf
import keras
import platform

import sys
sys.dont_write_bytecode = True

def renameImages():
    path = "./data_360"  # 解压数据的路径
    files = os.listdir(path)
    for file in files:
        pathImage = path + "/" + file
        ImageFiles = os.listdir(pathImage)
        n = 0
        for image in ImageFiles:
            oldName = pathImage + "/" + image
            newName = pathImage + "/" + file + "_" + str(n + 1) + ".jpg"
            os.rename(oldName, newName)
            print(oldName, " --> ", newName)
            n += 1


def docuChessInfo():
    # environment
    print("tensorflow->", tf.__version__)
    print("keras     ->", keras.__version__)
    print("python    ->", platform.python_version())

    pathChessChoose = "./data_360" # 人为选择的数据的路径

    # 遍历数据集，并存入inf列表
    # 建立txt文件记录数据
    chess_info_txt = "./chessInfo.txt"
    f = open(chess_info_txt, 'w')

    # 遍历
    count = 0
    files = os.listdir(pathChessChoose)
    for filename in files:
        printFilename = "Name -> " + str(count) + " -> " + filename
        print(printFilename)
        count += 1

    index = 0

    # 写入txt文件中
    for filename in files:
        tempDir = pathChessChoose + "/" + filename
        tempFiles = os.listdir(tempDir)
        for tempFilename in tempFiles:
            fileDir = str(index) + " " + filename + " " + tempFilename + "\n"
            f.write(fileDir) # 编号 姓名 图片路径与图片名
        index += 1 # 编号+1

    print("chess information documentation done!")


# use for debug
def main():
    # renameImages()
    docuChessInfo()

# 调用函数
if __name__ == '__main__':
    main()