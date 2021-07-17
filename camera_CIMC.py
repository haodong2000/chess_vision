# -*-*- coding utf-8 -*-*-
# read image from computer camera(USE camera)
import time

import cv2
import os # call system API
import datetime
from PIL import Image

import numpy as np
import yaml

import Global_Params

def getOriginImage():
    print(cv2.__version__)
    capture = cv2.VideoCapture(0) # on Webcam
    default_size = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("old size: ", default_size)

    # set frame height and width
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    new_size = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print("new size: ", new_size)

    test_ImageStore = Global_Params.M_systemCamTest_path
    ImageStorePath = Global_Params.M_origin_image_path
    count = 0

    skip_lines = 0
    with open('./fisheye_parameter.yaml') as infile:
        for i in range(skip_lines):
            _ = infile.readline()
        data = yaml.load(infile)

    while True:
        ret, origin_image = capture.read()

        temp_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        temp_name = temp_name + "_" + str(count) + ".jpg"
        cv2.imshow(temp_name, origin_image) # imshow

        flag = cv2.waitKey(0) # press enter to save image, and Esc to quit

        if flag == 13:
            # save_path = os.path.join(ImageStorePath, temp_name)
            save_path = os.path.join(test_ImageStore, temp_name)
            cv2.imwrite(save_path, origin_image)
            im_saved = Image.open(save_path)
            print(temp_name, " \tsaved. pixel: ", str(im_saved.size[0]), "*", str(im_saved.size[1]))
            cv2.destroyWindow(temp_name)
        count = count + 1

        if flag == 27:
            print("Quit: last image: " + temp_name)
            cv2.destroyWindow(temp_name)
            break

        if flag != 13 and flag != 27:
            cv2.destroyWindow(temp_name)
            continue

    while True:
        time.sleep(5)
        web_path = Global_Params.M_imageProcessTest_path
        web_images = os.listdir(web_path)
        count_capture = 0
        while count_capture < Global_Params.M_Test_Webcam:
            ret, origin_image = capture.read()
            count_capture += 1
            # print("count_webcam_capture = ", count_capture)
        temp_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        temp_name = temp_name + "_" + str(count) + ".jpg"
        # cv2.imshow(temp_name, origin_image) # imshow
        save_path = os.path.join(web_path, temp_name)
        for web_image in web_images:
            os.remove(os.path.join(web_path, web_image))
        cv2.imwrite(save_path, origin_image)
        print(temp_name, "   <saved>")



def main():
    getOriginImage()


if __name__ == '__main__':
    main()
