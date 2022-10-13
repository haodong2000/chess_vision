import numpy as np
import cv2

import Global_Params
import algorithm

import threading


def RgbMedianFilter(img_set, size):
    """
    对RGB图片集做中值滤波(暂时只考虑了奇数大小的窗口,如3x3、5x5)(but好像作用不大)
    :param img_set: 图片集, shape = [num, height, width, 3]
    :param size: 中值滤波窗口大小 (size, size)
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

def RedBlackBoost_Original(img_set, IMAGE_SHOW_OR_NOT, IMAGE_SHOW_FREQUENCY):
    '''
    增强图片中的红黑色(红色棋子增强红色，黑色棋子增强黑色)
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
    radius = Global_Params.M_norm_size/2
    mid =Global_Params.M_norm_size/2.0
    mid = int(mid)
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
            for i in range(height):
                for j in range(width):
                    if algorithm.outOfRadius(j, i):
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
                        continue
                    if ((0 <= hsv_img[i, j, 0] <= 20) or (100 <= hsv_img[i, j, 0] <= 360)) and \
                            (66.0 <= hsv_img[i, j, 1]*255 <= 255) and (33.0 <= hsv_img[i, j, 2] <= 255):
                        boosted_img_set[idx, i, j, :] = [0, 0, 255]
                    else:
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
        else:                   # 黑棋子黑色增强
            for i in range(height):
                for j in range(width):
                    if algorithm.outOfRadius(j, i):
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
                        continue
                    if (0 <= hsv_img[i, j, 0] <= 360) and \
                            (0 <= hsv_img[i, j, 1]*255 <= 255) and (0 <= hsv_img[i, j, 2] <= 70):
                        boosted_img_set[idx, i, j, :] = [0, 0, 0]
                    else:
                        boosted_img_set[idx, i, j, :] = [255, 255, 255]
        if idx/30 == int(idx/30):
            print("RedBlackBoost Processing...  <cur idx =", idx, ">")
        if IMAGE_SHOW_OR_NOT and idx/IMAGE_SHOW_FREQUENCY == int(idx/IMAGE_SHOW_FREQUENCY):
            print("hsv_img[mid, mid, :] -> ", hsv_img[mid, mid, :])
            cv2.imshow("img_" + str(idx), img/255.0)
            cv2.imshow("boosted_img_" + str(idx), boosted_img_set[idx]/255.0)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        idx += 1

    del img_set
    return boosted_img_set

# def RedBlackBoost_SingleThread(img_set, IMAGE_SHOW_OR_NOT, IMAGE_SHOW_FREQUENCY, thread_idx):
#     '''
#     增强图片中的红黑色(红色棋子增强红色，黑色棋子增强黑色)
#     :param img_set: 图片集, shape = [num, height, width, 3]
#     :return: 处理后的图片集
#     '''
#     num = img_set.shape[0]
#     print("num =", num, "\t\tthread_idx =", thread_idx)
#     height = img_set.shape[1]
#     width = img_set.shape[2]
#     boosted_img_set = np.zeros((num, height, width, 3))
#     hsv_img = np.zeros((height, width, 3))
#     threshold = 0.02
#     idx = 0
#     count = 0
#     radius = Global_Params.M_norm_size/2
#     mid =Global_Params.M_norm_size/2.0
#     mid = int(mid)
#     for img in img_set:
#         count += 1
#         red_cnt = 0
#         red_flag = False
#         hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#         for i in range(height):
#             for j in range(width):
#                 if ((0 <= hsv_img[i, j, 0] <= 10) or (310 <= hsv_img[i, j, 0] <= 360)) and (70 <= hsv_img[i, j, 1]*255 <= 255) and (50 <= hsv_img[i, j, 2] <= 255):
#                     red_cnt += 1
#                     if red_cnt >= threshold * height * width:
#                         red_flag = True
#                         break
#             if red_flag is True:
#                 break

#         if red_flag is True:    # 红棋子红色增强
#             for i in range(height):
#                 for j in range(width):
#                     if algorithm.outOfRadius(j, i):
#                         boosted_img_set[idx, i, j, :] = [255, 255, 255]
#                         continue
#                     if ((0 <= hsv_img[i, j, 0] <= 20) or (100 <= hsv_img[i, j, 0] <= 360)) and \
#                             (66.0 <= hsv_img[i, j, 1]*255 <= 255) and (33.0 <= hsv_img[i, j, 2] <= 255):
#                         boosted_img_set[idx, i, j, :] = [0, 0, 255]
#                     else:
#                         boosted_img_set[idx, i, j, :] = [255, 255, 255]
#         else:                   # 黑棋子黑色增强
#             for i in range(height):
#                 for j in range(width):
#                     if algorithm.outOfRadius(j, i):
#                         boosted_img_set[idx, i, j, :] = [255, 255, 255]
#                         continue
#                     if (0 <= hsv_img[i, j, 0] <= 360) and \
#                             (0 <= hsv_img[i, j, 1]*255 <= 255) and (0 <= hsv_img[i, j, 2] <= 70):
#                         boosted_img_set[idx, i, j, :] = [0, 0, 0]
#                     else:
#                         boosted_img_set[idx, i, j, :] = [255, 255, 255]
#         if idx/30 == int(idx/30):
#             print("RedBlackBoost Processing...  <cur idx =", idx, ">,  <thread idx =", thread_idx, ">")
#         if IMAGE_SHOW_OR_NOT and idx/IMAGE_SHOW_FREQUENCY == int(idx/IMAGE_SHOW_FREQUENCY):
#             print("hsv_img[mid, mid, :] -> ", hsv_img[mid, mid, :])
#             cv2.imshow("img_" + str(idx), img/255.0)
#             cv2.imshow("boosted_img_" + str(idx), boosted_img_set[idx]/255.0)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()
#         idx += 1

#     del img_set
#     return boosted_img_set
#     print("RedBlackBoost thread #", thread_idx, "finished!")

def distribution(NUM_IMG, THREAD):
    print("num =", NUM_IMG, "\t\tthread =", THREAD)
    reminder = NUM_IMG%THREAD
    base = round((NUM_IMG - reminder)/THREAD)
    print("base =", base, "\t\treminder =", reminder)
    dis_list = [base for _ in range(THREAD)]
    idx_list = [0 for _ in range(THREAD)]
    for idx in range(reminder):
        dis_list[idx] += 1
    for idx in range(THREAD):
        if idx > 0:
            idx_list[idx] += dis_list[idx - 1] + idx_list[idx - 1]
        else:
            idx_list[idx] = 0
    print("distribution list =", dis_list)
    print("dis index list    =", idx_list)
    return dis_list, idx_list

def RedBlackBoost(img_set, IMAGE_SHOW_OR_NOT, IMAGE_SHOW_FREQUENCY, THREAD=12):
    num = img_set.shape[0]
    height = img_set.shape[1]
    width = img_set.shape[2]
    boosted_img_set_total = np.zeros((num, height, width, 3))

    distribution_list, dis_index_list = distribution(num, THREAD)
    # return

    def RedBlackBoost_SingleThread(img_set, IMAGE_SHOW_OR_NOT, IMAGE_SHOW_FREQUENCY, thread_idx):
        '''
        增强图片中的红黑色(红色棋子增强红色，黑色棋子增强黑色)
        :param img_set: 图片集, shape = [num, height, width, 3]
        :return: 处理后的图片集
        '''
        num = img_set.shape[0]
        print("num =", num, "\t\tthread_idx =", thread_idx, "\t\tdistribution_list[thread_idx] =", distribution_list[thread_idx])
        height = img_set.shape[1]
        width = img_set.shape[2]
        boosted_img_set = np.zeros((num, height, width, 3))
        hsv_img = np.zeros((height, width, 3))
        threshold = 0.02
        idx = 0
        count = 0
        radius = Global_Params.M_norm_size/2
        mid =Global_Params.M_norm_size/2.0
        mid = int(mid)
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
                for i in range(height):
                    for j in range(width):
                        if algorithm.outOfRadius(j, i):
                            boosted_img_set[idx, i, j, :] = [255, 255, 255]
                            continue
                        if ((0 <= hsv_img[i, j, 0] <= 20) or (100 <= hsv_img[i, j, 0] <= 360)) and \
                                (66.0 <= hsv_img[i, j, 1]*255 <= 255) and (33.0 <= hsv_img[i, j, 2] <= 255):
                            boosted_img_set[idx, i, j, :] = [0, 0, 255]
                        else:
                            boosted_img_set[idx, i, j, :] = [255, 255, 255]
            else:                   # 黑棋子黑色增强
                for i in range(height):
                    for j in range(width):
                        if algorithm.outOfRadius(j, i):
                            boosted_img_set[idx, i, j, :] = [255, 255, 255]
                            continue
                        if (0 <= hsv_img[i, j, 0] <= 360) and \
                                (0 <= hsv_img[i, j, 1]*255 <= 255) and (0 <= hsv_img[i, j, 2] <= 70):
                            boosted_img_set[idx, i, j, :] = [0, 0, 0]
                        else:
                            boosted_img_set[idx, i, j, :] = [255, 255, 255]
            if idx/30 == int(idx/30):
                print("RedBlackBoost Processing...  <cur idx =", idx, ">,  <thread idx =", thread_idx, ">")
            if IMAGE_SHOW_OR_NOT and idx/IMAGE_SHOW_FREQUENCY == int(idx/IMAGE_SHOW_FREQUENCY):
                print("hsv_img[mid, mid, :] -> ", hsv_img[mid, mid, :])
                cv2.imshow("img_" + str(idx), img/255.0)
                cv2.imshow("boosted_img_" + str(idx), boosted_img_set[idx]/255.0)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            idx += 1

        del img_set
        # return boosted_img_set
        boosted_img_set_total[dis_index_list[thread_idx]:dis_index_list[thread_idx] + distribution_list[thread_idx]] = boosted_img_set
        print("RedBlackBoost thread #", thread_idx, "finished!")

    threads = [threading.Thread(target=RedBlackBoost_SingleThread, \
                                args=(img_set[dis_index_list[i]:dis_index_list[i] + distribution_list[i]], \
                                    IMAGE_SHOW_OR_NOT, IMAGE_SHOW_FREQUENCY, i)) \
                                        for i in range(THREAD)]
    for i in range(THREAD):
        threads[i].start()
    for i in range(THREAD):
        threads[i].join()
    # cv2.imshow("img_" + str(99), img_set[99]/255.0)
    # cv2.imshow("boosted_img_" + str(99), boosted_img_set_total[99]/255.0)
    # flag = cv2.waitKey(0)
    # if flag == 27:
    #     cv2.destroyAllWindows()
    # return
    return boosted_img_set_total

"""
    num = img_set.shape[0]
    height = img_set.shape[1]
    width = img_set.shape[2]
    boosted_img_set = np.zeros((num, height, width, 3))
    hsv_img = np.zeros((height, width, 3))
    threshold = 0.02
    idx = 0
    count = 0
    radius = Global_Params.M_norm_size/2
    mid =Global_Params.M_norm_size/2.0
    mid = int(mid)
"""
