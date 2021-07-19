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
        mask_temp = np.zeros((1080, 1920), np.uint8)
        mask = cv2.rectangle(mask_temp, Global_Params.M_point_lefttop, Global_Params.M_point_rightbottom,
                             (255, 255, 255), -1)
        crop_cv_im = cv2.bitwise_and(origin_image, origin_image, mask=mask)
        _, thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        crop_cv_im = crop_cv_im[Global_Params.M_point_lefttop[1]:Global_Params.M_point_rightbottom[1],
                     Global_Params.M_point_lefttop[0]:Global_Params.M_point_rightbottom[0]]
        origin_image = crop_cv_im
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
        time.sleep(0.01)
        web_path = Global_Params.M_imageProcessTest_path
        web_images = os.listdir(web_path)
        count_capture = 0
        while count_capture < Global_Params.M_Test_Webcam:
            ret, origin_image = capture.read()
            count_capture += 1
            mask_temp = np.zeros((1080, 1920), np.uint8)
            mask = cv2.rectangle(mask_temp, Global_Params.M_point_lefttop, Global_Params.M_point_rightbottom,
                                 (255, 255, 255), -1)
            crop_cv_im = cv2.bitwise_and(origin_image, origin_image, mask=mask)
            _, thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
            crop_cv_im = crop_cv_im[Global_Params.M_point_lefttop[1]:Global_Params.M_point_rightbottom[1],
                         Global_Params.M_point_lefttop[0]:Global_Params.M_point_rightbottom[0]]
            origin_image = crop_cv_im
            # print("count_webcam_capture = ", count_capture)
        temp_name = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        temp_name = temp_name + "_" + str(count) + ".jpg"
        # cv2.imshow(temp_name, origin_image) # imshow
        save_path = os.path.join(web_path, temp_name)
        cv2.imwrite(save_path, origin_image)
        web_images = sorted(web_images,
                            key=lambda files: os.path.getmtime(os.path.join(web_path, files)),
                            reverse=False)
        for web_image in web_images:
            os.remove(os.path.join(web_path, web_image))
            break
        cv2.imwrite(save_path, origin_image)
        print(temp_name, "   <saved>")



def main():
    getOriginImage()


if __name__ == '__main__':
    main()
