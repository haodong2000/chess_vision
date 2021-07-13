# -*-*- coding utf-8 -*-*-
# to hough circling and get chess image

import cv2
import os
import sys

import datetime

import numpy as np
from PIL import Image

img_height = -1
img_width = -1

def read_origin_image():
    origin_image_path = "./test_image_process/imageProcessTest"
    # origin_image_path = "./test_image_process/systemCamTest"
    images = os.listdir(origin_image_path)
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
    for index in range(0, count_image):
        origin_image = cv2.imread(origin_image_list[index], cv2.IMREAD_COLOR)

        if origin_image is None:
            print("ERROR: circle.py line: 36, image loading failed!")
            return -888

        gray_origin_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
        gray_origin_image = cv2.medianBlur(gray_origin_image, 5) # 高斯滤波

        pil_origin_image = Image.open(origin_image_list[index])
        origin_image_height = pil_origin_image.size[0]
        origin_image_width = pil_origin_image.size[1]
        img_height = origin_image_height
        img_width = origin_image_width

        # print("grey image show: index = ", index)
        window_name = "grey of " + origin_image_list[index]
        cv2.imshow(window_name, gray_origin_image)

        flag = cv2.waitKey(0)
        if flag == 13: # press enter to save the image
            save_path = "./test_image_process/imageProcessTest_ans/grey_" + str(index) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".jpg"
            cv2.imwrite(save_path, gray_origin_image)
            print(save_path, " saved")
            cv2.destroyWindow(window_name)
        elif flag == 27:
            cv2.destroyWindow(window_name)
        else:
            print("ERROR: file circle.py, line 56, flag invalid!")

        circles = cv2.HoughCircles(
            gray_origin_image, # input image, greyscale
            cv2.HOUGH_GRADIENT,
            1.0, # dp, the inverse ratio of resolution
            round(min(img_height, img_width)/10.5), # Minimum distance between detected centers
            param1=450, # Upper threshold for the internal Canny edge detector
            param2=30, # Threshold for center detection
            minRadius=round(min(img_height, img_width)/50.0), # Minimum radius to be detected, default 0
            maxRadius=round(min(img_height, img_width)/20.0) # Maximum radius to be detected, default 0
        )

        # print(round(min(img_height, img_width)/8.0),
        #       round(min(img_height, img_width)/100.0),
        #       round(min(img_height, img_width)/20.0))

        count_circle = 0
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for indexCircle in circles[0, :]:
                # print("count_circle = ", count_circle)
                count_circle = count_circle + 1
                center = (indexCircle[0], indexCircle[1]) # circle center
                radius = indexCircle[2] # circle radius
                cv2.circle(origin_image, center, radius, (255, 0, 255), 3)
        if count_circle == 0:
            print("count_circle = 0, no circles found!")

        print("count_circle = ", count_circle)

        # print("hough circle image show: index = ", index)
        window_name = "hough circle of " + origin_image_list[index] # or np.array(origin_image_list)[index]
        cv2.imshow(window_name, origin_image)
        print(str(index) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".jpg")

        flag = cv2.waitKey(0)
        if flag == 13: # press enter to save the image
            save_path = "./test_image_process/imageProcessTest_ans/circle_" + str(index) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".jpg"
            cv2.imwrite(save_path, origin_image)
            print(save_path, " saved")
            cv2.destroyWindow(window_name)
        elif flag == 27:
            cv2.destroyWindow(window_name)
        else:
            print("ERROR: file circle.py, line 88, flag invalid!")



# use for debug
def main():
    oriImg, cnt = read_origin_image()
    hough_circle(oriImg, cnt)

# 调用函数
if __name__ == '__main__':
    main()