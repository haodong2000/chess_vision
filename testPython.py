# -*- coding: utf-8 -*-
# for test
import tensorflow as tf
import os
import keras
import platform

import sys
sys.dont_write_bytecode = True

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
print(tf.__version__)
print(keras.__version__)
print(platform.python_version())

# test os
pathOfModel = "./model_save"
if not os.path.exists(pathOfModel): #判断是否存在
    os.makedirs(pathOfModel) #不存在则创建
pathOfModel = pathOfModel + "/"
# sort by last modified time
model_lists = os.listdir(pathOfModel)
model_lists = sorted(model_lists, 
    key = lambda files: os.path.getmtime(os.path.join(pathOfModel, files)))
modelPath = ""
for modelLists in os.listdir(pathOfModel):
    modelPath = os.path.join(pathOfModel, modelLists)
    print(modelPath)
    print(os.path.getmtime(modelPath))

if modelPath == "":
    print("NULL")
    exit()

print("model loaded!")