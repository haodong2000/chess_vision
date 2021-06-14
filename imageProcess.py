# -*- coding:utf-8 -*-
from keras.models import Sequential, load_model
import matplotlib.pyplot as plt  # plt 用于显示图片
import matplotlib.image as mp  # mpimg 用于读取图片
import numpy as np
from PIL import Image
from keras.models import Model
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn import svm
from numpy import array
from skimage.filters import gaussian,hessian,frangi
from skimage.filters import threshold_otsu

# 128， 128
img_h = 620
img_w = 620

# RGB图得到灰度图
def rgb2gray(rgb):
  return np.dot(rgb[...,:3], [0.299, 0.587, 0.114]) # Y=0.3R+0.59G+0.11B

# 直接改变各种图像的像素值
def produceImage(image_in, height, width):
    image = Image.fromarray(np.uint8(image_in)) # 将 numpy 数组转换为 PIL 图片
    image_out = image.resize((width, height), Image.ANTIALIAS) # 修改图像的大小（像素）
    image_out = np.array(image_out) # 将 PIL Image 图片转换为 numpy 数组
    return image_out

# 灰度图得到二值化图形
# TODO: in order to read image from different camps(black and red)
def gray2binary(gray):
    bn_pre = gray > threshold_otsu(gray)
    bn = np.zeros((bn_pre.shape[0], bn_pre.shape[1]))
    for i in range(bn.shape[0]):
        for j in range(bn.shape[1]):
            if bn_pre[i][j]:
                bn[i][j] = 1 # 大于阈值的设置为1
    return bn

# 只进行提取特征处理，不裁剪缩放
def preprocess(img, img_h, img_w):
    # print(image.shape)  # for debug: tuple index out of range
    # img = rgb2gray(image) # 由于img本身已经是单通道图，不需要灰度处理
    bn = produceImage(gray2binary(img), img_h, img_w)
    # 将图片转化为数组输出
    low = gaussian(img, sigma=4)
    # 高斯模糊处理
    high = img - low
    high = produceImage(high, img_h, img_w)
    for i in range(high.shape[0]):
        for j in range(high.shape[1]):
            if bn[i][j] == 1:
                high[i][j] = 0

    return high
