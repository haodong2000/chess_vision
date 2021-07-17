# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mp # mp 用于读取图片
import os
from keras.models import load_model
import numpy as np
from PIL import Image
import cv2
from keras.preprocessing.image import img_to_array

import load_data
import Global_Params
import filter

import sys
sys.dont_write_bytecode = True

img_h = Global_Params.M_norm_size
img_w = Global_Params.M_norm_size

save_dir = Global_Params.M_model_save_path + "/"  # the model stored there


def readPreImage():

    chess_vertify_info_txt = Global_Params.M_chess_vertify_txt
    fvertify = open(chess_vertify_info_txt, 'w')

    testMatch = []
    pre_dir = Global_Params.M_test_path # test images stored there
    files = os.listdir(pre_dir) # 遍历文件夹
    index = 0
    for file in files:
        tempDir = pre_dir + "/" + file
        testMatch.append(tempDir)
        dispVertify = str(index + 1) + " -> " + tempDir + "\n"
        fvertify.write(dispVertify)
        index += 1
    print("test data testMatch done!")
    return testMatch # 里面存放路径

# 根据路径读入所有的图片，同时根据全局规定的图片尺寸要求进行裁剪,并按照模型输入要求reshape
def returnPreImage(testMatch):
    data = []
    label = []
    size = len(testMatch)
    count = 0
    for each_image in testMatch:
        count += 1
        print(each_image)
        image = cv2.imread(each_image)
        image = cv2.resize(image, (img_w, img_h))
        image = img_to_array(image)
        data.append(image)

    data = np.array(data)
    print("data shape      = ", data.shape, " ===============================")
    data = filter.RedBlackBoost(data, False, 99)
    data = data/255.0

    print("Test image reading done!")
    return data # 里面存放图片数据


def dispResult(TestMatch, testMatch):
    # sort by last modified time
    model_lists = os.listdir(save_dir)
    model_lists = sorted(model_lists, 
                         key=lambda files: os.path.getmtime(os.path.join(save_dir, files)),
                         reverse=False)
    model_path_vertify = ""
    for modelLists in os.listdir(save_dir):
        model_path_vertify = os.path.join(save_dir, modelLists)
        print(model_path_vertify)

    if model_path_vertify == "": # if the pwd is NULL
        print("No model saved!")
        exit()

    model = load_model(model_path_vertify)
    print("model loaded!")
    pre_dir = Global_Params.M_test_path # test images stored there
    testImage = os.listdir(pre_dir)
    print(testImage)

    count_vertify = 0
    for i in range(len(TestMatch)):
        img = TestMatch[i]
        img = np.expand_dims(img, 0) # 扩展至四维
        output = model.predict(img)
        print(output)
        print(output.argmax(), "   \t-> ", load_data.int2str(output.argmax()))
        mat = Image.open(testMatch[i]) # load image
        plt.figure("Test Image")
        plt.imshow(mat)
        plt.axis("off") # 关掉坐标轴为 off
        count_vertify += 1
        title = "CNN Result: " + load_data.int2str(output.argmax()) + "  (num = " + str(count_vertify) + ")"
        plt.title(title) # 图像题目
        plt.show()

    print("----------------------------------------")
    print("Test process done!")


def main():
    test = readPreImage()
    data = returnPreImage(test)
    dispResult(data, test)

# 调用函数
if __name__ == '__main__':
    main()