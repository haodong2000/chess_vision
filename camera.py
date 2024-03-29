# -*-*- coding utf-8 -*-*-
# read image from computer camera(USE camera)

import cv2
import os # call system API
import datetime
from PIL import Image

import numpy as np
# import yaml

import Global_Params

IS_WEBCAM = True

def getOriginImage():
    print(cv2.__version__)
    capture = cv2.VideoCapture(2) if IS_WEBCAM else cv2.VideoCapture(-1)
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

    # skip_lines = 0
    # with open('./fisheye_parameter.yaml') as infile:
    #     for i in range(skip_lines):
    #         _ = infile.readline()
    #     data = yaml.load(infile)

    while(True):
        ret, origin_image = capture.read()
        mask_temp = np.zeros((1080, 1920), np.uint8)
        mask = cv2.rectangle(mask_temp, Global_Params.M_point_lefttop, Global_Params.M_point_rightbottom,
                             (255, 255, 255), -1)
        crop_cv_im = cv2.bitwise_and(origin_image, origin_image, mask=mask)
        _, thresh = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        crop_cv_im = crop_cv_im[Global_Params.M_point_lefttop[1]:Global_Params.M_point_rightbottom[1],
                     Global_Params.M_point_lefttop[0]:Global_Params.M_point_rightbottom[0]]
        origin_image = crop_cv_im
        # # 2021/07/15 fish eye
        # DIM = (1920, 1080)
        # [fu, fv, pu, pv] = data['cam0']['intrinsics']
        # K = np.asarray([[fu, 0, pu], [0, fv, pv], [0, 0, 1]])  # K(3,3)
        # D = np.asarray(data['cam0']['distortion_coeffs'])  # D(4,1)
        # h, w = origin_image.shape[:2]
        # cv2.fisheye.undistortImage(origin_image, origin_image, K, D, K, DIM)

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


def main():
    getOriginImage()


if __name__ == '__main__':
    main()
