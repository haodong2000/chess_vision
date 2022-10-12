# -*- coding:utf-8 -*-
# keras imports for the dataset and building our neural network
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Activation
from keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
# from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

from readImage import readImage, returnImage
from chessInfo import docuChessInfo
from chessInfo import renameImages
from vertifyModel import readPreImage, returnPreImage, dispResult
import sys
sys.dont_write_bytecode = True

import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mp # mpimg 用于读取图片
from PIL import Image
import numpy as np
import math
import os

img_h = 620
img_w = 620
channel = 1
classes = 10

# 训练cnn模型
# 这里的x_train,x_test里面存放的不是图像路径，而是读取图像之后的数组，与之前的x_train, x_test不一样
def trainModel(x_train, y_train, x_test, y_test):
    # 1. 数据预处理
    # 归一化处理（0~1）
    x_train = x_train.astype('float32') # 类型转化或者类型声明
    x_test = x_test.astype('float32')
    # x_test /= 255
    # x_train /= 255

    # 将类别向量转换为二进制（只有0和1）的矩阵类型表示
    y_train = to_categorical(y_train, classes)
    y_test = to_categorical(y_test, classes)

    printShape = "x_train.shape is: " # (480, 128, 128, 1)
    print(printShape, x_train.shape)
    print("-*-*-*- Step -> 1 -> Normalization Done！ -*-*-*-")

    # 2. 定义模型结构
    spoch_number = 10 # spoch number
    model = Sequential()
    # New model
    model.add(Conv2D(32, (3, 3), 
              activation='relu', padding='same', 
              data_format='channels_last', name='layer1_con1',
              input_shape=(img_h, img_w, channel)))
    model.add(Conv2D(32, (3, 3), 
              activation='relu', padding='same', 
              data_format='channels_last', name='layer1_con2'))
    model.add(MaxPool2D(pool_size=(2, 2),
              strides=(2,2), padding = 'same', 
              data_format='channels_last',name = 'layer1_pool'))
    model.add(Dropout(0.25)) # dropout层可以防止过拟合，每次有25%的数据将被抛弃
    model.add(Conv2D(64, (3, 3), 
              activation='relu', padding='same', 
              data_format='channels_last',name='layer2_con1'))
    model.add(Conv2D(64, (3, 3), 
              activation='relu', padding='same', 
              data_format='channels_last',name='layer2_con2'))
    model.add(MaxPool2D(pool_size=(2, 2),
              strides=(2,2), padding = 'same', 
              data_format='channels_last',name = 'layer2_pool'))

    # Old model
    # model.add(Conv2D(16, kernel_size=(5, 5), input_shape=(img_h, img_w, channel))) # 卷积
    # model.add(Activation('tanh'))
    # model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2))) # 池化
    # model.add(Conv2D(16, kernel_size=(5, 5)))
    # model.add(Activation('tanh'))
    # model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    # model.add(Conv2D(32, kernel_size=(5, 5)))
    # model.add(Activation('tanh'))
    # model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    # model.add(Conv2D(32, kernel_size=(5, 5)))
    # model.add(Activation('tanh'))
    # model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))  # 该全连接层共128个神经元
    model.add(Dense(10, activation='softmax')) # 一共分为10类，所以最后一层有10个神经元，并且采用softmax输出

    # model.add(Flatten())
    # model.add(Dense(1000, activation='relu')) # 全连接
    # model.add(Dropout(0.5))
    # model.add(Dense(classes, activation='softmax'))

    print("-*-*-*- Step -> 2 -> Model Building Done！ -*-*-*-")

    # 3. 编译
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("-*-*-*- Step -> 3 -> Model Compile Done！ -*-*-*-")

    # 4. 训练
    # history = model.fit(x_train, y_train, batch_size = 64, epochs = i, validation_data = (x_test, y_test))
    # print(history.history.keys())
    # 定义数据生成器用于数据提升，其返回一个生成器对象datagen，datagen每被调用一
    # 次其生成一组数据（顺序生成），节省内存，其实就是python的数据生成器
    datagen = ImageDataGenerator(
        featurewise_center=False,  # 是否使输入数据去中心化（均值为0），
        samplewise_center=False,  # 是否使输入数据的每个样本均值为0
        featurewise_std_normalization=False,  # 是否数据标准化（输入数据除以数据集的标准差）
        samplewise_std_normalization=False,  # 是否将每个样本数据除以自身的标准差
        zca_whitening=False,  # 是否对输入数据施以ZCA白化
        rotation_range=15,  # 数据提升时图片随机转动的角度(范围为0～180)
        width_shift_range=0.15,  # 数据提升时图片水平偏移的幅度（单位为图片宽度的占比，0~1之间的浮点数）
        height_shift_range=0.15,  # 同上，只不过这里是垂直
        horizontal_flip=False,  # 是否进行随机水平翻转
        vertical_flip=False)  # 是否进行随机垂直翻转

    # 计算整个训练样本集的数量以用于特征值归一化、ZCA白化等处理
    datagen.fit(x_train)

    # 利用生成器开始训练模型
    generator = datagen.flow(x_train, y_train, batch_size = 128)
    history = model.fit_generator(generator, 
        steps_per_epoch = len(x_train)/128,
        epochs = spoch_number, 
        validation_data = (x_test, y_test),
        verbose = 1.0)
    # Error occurred when finalizing GeneratorDataset iterator: Failed precondition:
    # Python interpreter state is not initialized. The process may be terminated.
    # 内存不足，将bach_size改小

    # 绘制训练 & 验证的准确率值
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # 绘制训练 & 验证的损失值
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    print("-*-*-*- Step -> 4 -> Training Done！ -*-*-*-")

    # 5. 评估模型
    score = model.evaluate(x_test, y_test)
    print('acc', score[1])

    # saving the model
    save_dir = "./model_save"
    model_name = "model" + "_" + str(spoch_number) + "_" + str(score[1]) + '.h5'
    model_path = os.path.join(save_dir, model_name)

    model.save(model_path)

    if not os.path.exists(save_dir): #判断是否存在
        os.makedirs(save_dir) #不存在则创建

    print("-*-*-*- Step -> 5 -> Model Evaluation Done！ -*-*-*-")

    print('Saved Trained Model at %s ' % save_dir + "/" + model_name)
    print("-*-*-*- CNN Training Model Done! -*-*-*-")

    # 6. 测试集显示

def main(): # 主函数
    docuChessInfo() # 记录信息
    x_train, y_train, x_test, y_test = readImage() # 测试集与训练集的分类整理（路径与对应人名编号）
    x_train_img, x_test_img = returnImage(x_train, x_test) # 图片读取
    trainModel(x_train_img, y_train, x_test_img, y_test) # CNN训练
    # 以下三个函数属于检验模块，详见 vertify.py
    test = readPreImage()
    Test = returnPreImage(test) # 检验模型的图片读取
    dispResult(Test, test) # 输出检验结果

# 调用函数
if __name__ == '__main__':
    main()

'''
Data: https://www.heywhale.com/mw/dataset/5fa3f55fca48e0003014d7b0/file
Date: 2021/04/08
'''