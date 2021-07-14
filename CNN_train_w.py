# -*- coding: utf-8 -*-

# keras imports for the dataset and building our neural network
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Activation
from keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.utils import to_categorical
# from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.callbacks import EarlyStopping

import Global_Params

import matplotlib

import matplotlib.image as mp # mpimg 用于读取图片
from PIL import Image
import numpy as np
import math
import os

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt # plt 用于显示图片

validation_split_rate = Global_Params.M_validation_split_rate

# 训练cnn模型
# 这里的x_train,x_test里面存放的不是图像路径，而是读取图像之后的数组，与之前的x_train, x_test不一样
def trainModel(x_train, y_train, size, x_test, y_test):
    i = Global_Params.M_epoch_number # epoch number
    # 2. 定义模型结构
    # 迭代次数：第一次设置为30，后为了优化训练效果更改为100，后改为50
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding='same',
                     input_shape=(size, size, 3), activation='relu'))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.3))
    model.add(Dense(2500, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1500, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(15, activation='softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])

    early_stopping = EarlyStopping(monitor='val_accuracy', min_delta=0.0000000001, patience=2, mode='max')
    history = model.fit(x_train, y_train, batch_size=36, epochs=i, callbacks=[early_stopping], verbose=1,
                        validation_split=validation_split_rate)

    # 4. 训练
    # history = model.fit(x_train, y_train, batch_size=64, epochs=i, validation_data=(x_test, y_test))
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
        vertical_flip=False,  # 是否进行随机垂直翻转
        # validation_split=0.1
    )

    # # 计算整个训练样本集的数量以用于特征值归一化、ZCA白化等处理
    # datagen.fit(x_train)
    #
    # # 利用生成器开始训练模型
    # history = model.fit_generator(datagen.flow(x_train, y_train,
    #                                            batch_size=128), epochs=i)  # steps_per_epoch=x_train.shape[0],

    # 绘制训练 & 验证的准确率值
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
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

    # x_test = []
    # y_test = []

    data_size = len(y_train)
    print("train  len  = ", data_size)

    # for data_index in range(data_size):
    #     if (data_index + 1) % 10 == 0:
    #         x_test.append(x_train[data_index])
    #         y_test.append(y_train[data_index])

    # count_data = 0
    # for data_index in x_train:
    #     count_data += 1
    #     if count_data % 10 == 0:
    #         x_test.append(data_index)
    #
    # count_label = 0
    # for label_index in y_train:
    #     count_label += 1
    #     if count_label % 10 == 0:
    #         y_test.append(label_index)

    print("x_test size = ", len(x_test))
    print("y_test size = ", len(y_test))

    score = model.evaluate(x_test, y_test)
    print('acc', score[1])

    # saving the model
    save_dir = Global_Params.M_model_save_path
    model_name = "model"+str(i) + "_" + str(score[1]) + "w.h5"
    model_path = os.path.join(save_dir, model_name)

    model.save(model_path)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print('Saved trained model at %s ' % model_path)
    print("train model done!")