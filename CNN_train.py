# -*- coding: utf-8 -*-

import Global_Params
from keras.callbacks import EarlyStopping
import filter
import numpy as np
import tensorflow as tf
import cv2
import os
from keras.utils import to_categorical
from keras.preprocessing.image import img_to_array
from keras.callbacks import EarlyStopping
from imutils import paths
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

validation_split_rate = Global_Params.M_validation_split_rate


def TrainCnnModel(data, label, size, x_test, y_test):
    """
    训练CNN模型
    :param data:  图像矩阵, rbg
    :param label: 图像对应的标签, one-hot
    :param size:  图片尺寸
    :return: 返回训练后的模型
    """
    epoch_number = Global_Params.M_epoch_number
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

    early_stopping = EarlyStopping(monitor='val_accuracy', min_delta=0.01, patience=2, mode='max')
    history = model.fit(data, label, batch_size=36, epochs=epoch_number, callbacks=[early_stopping], verbose=1,
                        validation_split=validation_split_rate)

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
    #
    # data_size = len(label)
    #
    # for data_index in range(data_size):
    #     if (data_index + 1) % 10 == 0:
    #         x_test.append(data[data_index])
    #         y_test.append(label[data_index])

    score = model.evaluate(x_test, y_test)
    print('acc', score[1])

    # saving the model
    save_dir = Global_Params.M_model_save_path
    model_name = "model"+str(epoch_number) + "_" + str(score[1]) + "z.h5"
    model_path = os.path.join(save_dir, model_name)

    model.save(model_path)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    print('Saved trained model at %s ' % model_path)
    print("train model done!")

    return model