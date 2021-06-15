import numpy as np
import cv2


def RgbMedianFilter(img_set, size):
    """
    对RGB图片集做中值滤波（暂时只考虑了奇数大小的窗口，如3x3、5x5）
    (中值滤波好像作用不大)
    :param img_set: 图片集, shape = [num, height, width, 3]
    :param size:    中值滤波窗口大小(size, size)
    :return: 中值滤波后的图片集
    """
    num = img_set.shape[0]
    height = img_set.shape[1]
    width = img_set.shape[2]
    filted_img_set = np.zeros((num, height, width, 3))
    edge = (int)(size/2)
    idx = 0
    for img in img_set:
        for i in range(height):
            for j in range(width):
                if i < edge or i > height-edge-1 or j < edge or j > width-edge-1:
                    filted_img_set[idx, i, j, :] = img[i, j, :]
                else:
                    for color in range(3):
                        filted_img_set[idx, i, j, color] = np.median(img[i-edge:i+edge, j-edge:j+edge, color])
        cv2.imshow("img", img/255.0)
        cv2.imshow("filted_img", filted_img_set[idx]/255.0)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        idx += 1

    return filted_img_set

def RedBlackBoost(img_set):
    '''
    增强图片中的红黑色（红色棋子增强红色，黑色棋子增强黑色）
    :param img_set: 图片集, shape = [num, height, width, 3]
    :return: 处理后的图片集
    '''
    num = img_set.shape[0]
    height = img_set.shape[1]
    width = img_set.shape[2]
    boosted_img_set = np.zeros((num, height, width, 3))
    hsv_img = np.zeros((height, width, 3))
    threshold = 0.02
    idx = 0
    count = 0
    for img in img_set:
        count += 1
        red_cnt = 0
        red_flag = False
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        for i in range(height):
            for j in range(width):
                if ((0 <= hsv_img[i, j, 0] <= 10) or (310 <= hsv_img[i, j, 0] <= 360)) and (70 <= hsv_img[i, j, 1]*255 <= 255) and (50 <= hsv_img[i, j, 2] <= 255):
                    red_cnt += 1
                    if red_cnt >= threshold * height * width:
                        red_flag = True
                        break
            if red_flag is True:
                break

        if red_flag is True:    # 红棋子红色增强
            print("RedBlackBoost   \t\t<", count, ">   \t\tred")
            for i in range(height):
                for j in range(width):
                    if ((0 <= hsv_img[i, j, 0] <= 10) or (310 <= hsv_img[i, j, 0] <= 360)) and (70 <= hsv_img[i, j, 1]*255 <= 255) and (50 <= hsv_img[i, j, 2] <= 255):
                        boosted_img_set[idx, i, j, :] = [0, 0, 255]
                    else:
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
        else:                   # 黑棋子黑色增强
            print("RedBlackBoost   \t\t<", count, ">   \t\tblack")
            for i in range(height):
                for j in range(width):
                    if (0 <= hsv_img[i, j, 0] <= 360) and (0 <= hsv_img[i, j, 1]*255 <= 255) and (0 <= hsv_img[i, j, 2] <= 120):
                        boosted_img_set[idx, i, j, :] = [0, 0, 0]
                    else:
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
        # if idx/359 == int(idx/359):
        #    cv2.imshow("img", img/255.0)
        #    cv2.imshow("boosted_img", boosted_img_set[idx]/255.0)
        #    cv2.waitKey(0)
        #    cv2.destroyAllWindows()
        # print("img" + str(idx) + " OK.")
        idx += 1

    del img_set
    return boosted_img_set
