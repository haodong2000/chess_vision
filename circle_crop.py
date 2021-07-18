# -*-*- coding utf-8 -*-*-
# to hough circling and get chess image

import cv2
import os
import sys

import datetime

import numpy as np
from PIL import Image

import algorithm
import Global_Params
from keras.models import load_model
from keras.preprocessing.image import img_to_array

import filter
import server_one
import time

from load_data import str2int

# img_height = -1
# img_width = -1

CHESS_IMAGE_SHOW = True

def read_origin_image():
    origin_image_path = Global_Params.M_imageProcessTest_path
    # origin_image_path = "./test_image_process/systemCamTest"

    images = os.listdir(origin_image_path)
    images = sorted(images,
                    key=lambda files: os.path.getmtime(os.path.join(origin_image_path, files)),
                    reverse=False)

    count_image = 0
    origin_image_list = []
    for image in images:
        image_full_path = os.path.join(origin_image_path, image)
        img = Image.open(image_full_path)
        print(image_full_path, " pixel: " + str(img.size[0]) + "*" + str(img.size[1])) # debug
        count_image = count_image + 1
        origin_image_list.append(image_full_path)

    print("image list done! count = ", count_image)

    if count_image == 0:
        print("ERROR: no image in path: ", origin_image_path)
        return -999

    return origin_image_list, count_image

def hough_circle(origin_image_list, count_image):
    save_dir = Global_Params.M_model_save_path + "/"  # the model stored there
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

    # for index in range(0, count_image):
    index = 0
    origin_image = cv2.imread(origin_image_list[index], cv2.IMREAD_COLOR)
    print(origin_image_list[index])

    if origin_image is None:
        print("ERROR: circle.py line: 36, image loading failed!")
        return -888

    pil_origin_image = Image.open(origin_image_list[index])
    origin_image_height = pil_origin_image.size[1]
    origin_image_width = pil_origin_image.size[0]
    img_height = origin_image_height
    img_width = origin_image_width

    gray_origin_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
    gray_origin_image = cv2.medianBlur(gray_origin_image, 5) # 高斯滤波
    # gray_origin_image = cv2.resize(gray_origin_image, (img_width, img_height))

    # print("grey image show: index = ", index)
    window_name = "grey of " + origin_image_list[index]

    if CHESS_IMAGE_SHOW:
        cv2.imshow(window_name, gray_origin_image)
        flag = cv2.waitKey(0)
        if flag == 13: # press enter to save the image
            save_path = Global_Params.M_imageProcessTestAns_path + "/grey_" + str(index) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".jpg"
            cv2.imwrite(save_path, gray_origin_image)
            print(save_path, " saved")
            cv2.destroyWindow(window_name)
        elif flag == 27:
            cv2.destroyWindow(window_name)
        else:
            print("ERROR: file circle.py, line 56, flag invalid!")

    # create mask
    mask = []

    circles = cv2.HoughCircles(
        gray_origin_image, # input image, greyscale
        cv2.HOUGH_GRADIENT,
        1.0, # dp, the inverse ratio of resolution
        round(min(img_height, img_width)/10.5), # Minimum distance between detected centers
        param1=425, # Upper threshold for the internal Canny edge detector
        param2=30, # Threshold for center detection
        minRadius=round(min(img_height, img_width)/40.0), # Minimum radius to be detected, default 0
        maxRadius=round(min(img_height, img_width)/20.0) # Maximum radius to be detected, default 0
    )

    # print(round(min(img_height, img_width)/8.0),
    #       round(min(img_height, img_width)/100.0),
    #       round(min(img_height, img_width)/20.0))

    count_circle = 0
    only_one_x = []
    only_one_y = []
    only_one_w = []
    only_one_h = []
    chess_x = []
    chess_y = []
    temp_origin = cv2.imread(origin_image_list[index], cv2.IMREAD_COLOR)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for indexCircle in circles[0, :]:
            only_one_x.append(indexCircle[0] - indexCircle[2])
            only_one_y.append(indexCircle[1] - indexCircle[2])
            only_one_w.append(indexCircle[2]*2)
            only_one_h.append(indexCircle[2]*2)
            # print("count_circle = ", count_circle)
            count_circle = count_circle + 1
            center = (indexCircle[0], indexCircle[1]) # circle center
            chess_x.append(indexCircle[0])
            chess_y.append(indexCircle[1])
            radius = indexCircle[2] # circle radius
            cv2.circle(temp_origin, center, radius, (255, 0, 255), 3)
            mask_temp = np.zeros((pil_origin_image.size[1], pil_origin_image.size[0]), np.uint8)
            cv2.circle(mask_temp, center, radius, (255, 255, 255), thickness=-1)
            mask.append(mask_temp)
    if count_circle == 0:
        print("count_circle = 0, no circles found!")

    print("count_circle   = ", count_circle)

    # print("hough circle image show: index = ", index)
    window_name = "hough circle of " + origin_image_list[index] # or np.array(origin_image_list)[index]
    # cv2.imshow(window_name, temp_origin)
    # print(str(index) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".jpg")

    if CHESS_IMAGE_SHOW:
        cv2.imshow(window_name, temp_origin)
        flag = cv2.waitKey(0)
        if flag == 13: # press enter to save the image
            save_path = Global_Params.M_imageProcessTestAns_path + "/circle_" + str(index) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".jpg"
            cv2.imwrite(save_path, temp_origin)
            print(save_path, " saved")
            cv2.destroyWindow(window_name)
        elif flag == 27:
            cv2.destroyWindow(window_name)
        else:
            print("ERROR: file circle.py, line 88, flag invalid!")

    data = []

    for index_circle in range(count_circle):
        # Copy that image using that mask
        # print(origin_image.shape, " ", mask[index_circle].shape)
        crop_cv_im = cv2.bitwise_and(origin_image, origin_image, mask=mask[index_circle])
        # apply threshold
        _, thresh = cv2.threshold(mask[index_circle], 1, 255, cv2.THRESH_BINARY)
        # find contour
        # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        crop_cv_im = crop_cv_im[only_one_y[index_circle]:only_one_y[index_circle] + only_one_h[index_circle],
                                only_one_x[index_circle]:only_one_x[index_circle] + only_one_w[index_circle]]
        # cv2.imshow(str(index_circle + 1) + " <crop>", crop_cv_im)
        # print(str(index_circle + 1), "  \t<crop>  ", crop_cv_im.shape)
        data_no_use_path = Global_Params.M_image_circle_test_path

        if CHESS_IMAGE_SHOW:
            cv2.imshow(str(index_circle + 1) + " <crop>", crop_cv_im)
            flag = cv2.waitKey(0)
            if flag == 27:
                cv2.destroyWindow(str(index_circle + 1) + " <crop>")
            elif flag == 13:
                crop_cv_im = cv2.resize(crop_cv_im, (Global_Params.M_norm_size, Global_Params.M_norm_size))
                new_origin_name = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "_crop_" + str(index) + ".jpg"
                cv2.imwrite(os.path.join(data_no_use_path, new_origin_name), crop_cv_im)
                cv2.destroyWindow(str(index_circle + 1) + " <crop>")
                print("===============" + new_origin_name + "==SAVED===================")
            else:
                print("generate_data.py, line:24, esc expected")

        crop_cv_im = cv2.resize(crop_cv_im, (Global_Params.M_norm_size, Global_Params.M_norm_size))
        crop_cv_im = img_to_array(crop_cv_im)
        data.append(crop_cv_im)
        # data = np.array(data)
        # data = filter.RedBlackBoost(data)
        # data = data / 255.0
        # crop_cv_im = data[0]
        # crop_cv_im = np.expand_dims(crop_cv_im, 0)  # 扩展至四维
        # output = model.predict(crop_cv_im)
        # print(str(index_circle + 1) + " <crop>    CNN: ", output.argmax())
        # chess_int.append(output.argmax())
        # data = [] # clear

    data = np.array(data)
    print("board data shape      = ", data.shape, " ===============================")

    print("chess_x.size   = ", len(chess_x))
    print("chess_y.size   = ", len(chess_y))

    del model
    return chess_x, chess_y  # only one picture!!!


def generate_board_message(count):
    print("Chess Detection Count = ", count)
    oriImg, cnt = read_origin_image()
    chess_x, chess_y = hough_circle(oriImg, cnt)



# use for debug
def main():
    generate_board_message(1)


# 调用函数
if __name__ == '__main__':
    main()