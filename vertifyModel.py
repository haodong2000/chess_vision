# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib.image as mp # mp 用于读取图片
import os
from keras.models import load_model
import numpy as np
from PIL import Image
from imageProcess import preprocess

import sys
sys.dont_write_bytecode = True

img_h = 128
img_w = 128
channel=  1

classes_name_list = ["Cannons", "Elephant", "General", "King", "Knight",
                     "Mandarin", "Minister", "Pawns", "Rook", "Soldier"]

save_dir = "./modelSave/" # the model stored there

def readPreImage():

    chess_vertify_info_txt = "./chessVertify.txt"
    fvertify = open(chess_vertify_info_txt, 'w')

    testMatch = []
    pre_dir = "./test" # test images stored there
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
    TestMatch = []
    for i in range(len(testMatch)):
        diapStrTest = "TestMatch reading image data, current position: " + str(i)
        print(diapStrTest)
        TestMatch.append(preprocess(mp.imread(testMatch[i]), img_h, img_w))

    TestMatch = np.array(TestMatch) # 数组化处理
    print("TestMatch.shape is: ", TestMatch.shape)
    TestMatch = TestMatch.reshape(TestMatch.shape[0], TestMatch[0].shape[0], TestMatch[0].shape[1], channel).astype("float32")
    TestMatch = TestMatch/255 # 归一化
    print("Test image reading done!")
    return TestMatch # 里面存放图片数据

def dispResult(TestMatch, testMatch):
    # sort by last modified time
    model_lists = os.listdir(save_dir)
    model_lists = sorted(model_lists, 
        key = lambda files: os.path.getmtime(os.path.join(save_dir, files)))
    model_path_vertify = ""
    for modelLists in os.listdir(save_dir):
        model_path_vertify = os.path.join(save_dir, modelLists)
        print(model_path_vertify)

    if model_path_vertify == "": # if the pwd is NULL
        print("No model saved!")
        exit()

    model = load_model(model_path_vertify)
    print("model loaded!")
    pre_dir = "./test" # test images stored there
    testImage = os.listdir(pre_dir)
    print(testImage)

    result = [] # store the results
    for i in range(len(TestMatch)):
        img = TestMatch[i]
        img = np.expand_dims(img, 0) # 扩展至四维
        output = model.predict(img)
        result.append(output)
        print("----------------------------------------")
        print("No. ", str(i + 1))
        print("Test Image  -> ", testMatch[i])
        print("Test Result -> ",  classes_name_list[output.argmax()])
        print("Process Res -> (below this line)")
        print(output)
        # 显示图片与结果
        mat = Image.open(testMatch[i]) # load image
        plt.figure("Test Image")
        plt.imshow(mat)
        plt.axis("off") # 关掉坐标轴为 off
        title = "CNN Result: " + classes_name_list[output.argmax()]
        plt.title(title) # 图像题目
        plt.show()

    print("----------------------------------------")
    print("Test process done!")


def main():
    test = readPreImage()
    Test = returnPreImage(test)
    dispResult(Test, test)

# 调用函数
if __name__ == '__main__':
    main()