# -*- coding: utf-8 -*-

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


def TrainCnnModel(data, label, size):
    """
    训练CNN模型
    :param data:  图像矩阵, rbg
    :param label: 图像对应的标签, one-hot
    :param size:  图片尺寸
    :return: 返回训练后的模型
    """
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense

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

    early_stopping = EarlyStopping(monitor='val_acc', min_delta=0.01, patience=2, mode='max')
    history = model.fit(data, label, batch_size=36, epochs=100, callbacks=[early_stopping], verbose=1,
                        validation_split=0.1)
    return model