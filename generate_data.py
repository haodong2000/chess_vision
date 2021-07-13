# -*- coding: utf-8 -*-
# generate data by resizing and rotation range(360)
# LI Haodong

import cv2
import os

import numpy as np

from load_data import norm_size

import datetime

from PIL import Image

import Global_Params

number_angle = Global_Params.M_number_angle
IMAGE_SHOW = True

def clear(data_gen_path, data_no_use_path):
    data_no_use = os.listdir(data_no_use_path)
    for file in data_no_use:
        os.remove(os.path.join(data_no_use_path, file))
    print(data_no_use_path, " removed")

    one_level = os.listdir(data_gen_path)
    for two_level in one_level:
        temp_path = os.path.join(data_gen_path, two_level)
        temp_files = os.listdir(temp_path)
        print(two_level, " removed")
        for file in temp_files:
            os.remove(os.path.join(temp_path, file))


def generate_data(data_new_path, data_gen_path, data_no_use_path):
    img_width = norm_size
    img_height = norm_size

    ret_img = []

    origin_images = os.listdir(data_new_path)
    for origin_image in origin_images:
        im = Image.open(os.path.join(data_new_path, origin_image))
        im = im.resize((img_width, img_height))
        cv_im = cv2.imread(os.path.join(data_new_path, origin_image))
        cv_im = cv2.resize(cv_im, (img_width, img_height))
        print(os.path.join(data_new_path, origin_image), "pixel -> ", im.size[0], "*", im.size[1])

        # cv2.imshow(origin_image, cv_im)
        # flag = cv2.waitKey(0)
        # if flag == 27:
        #     cv2.destroyWindow(origin_image)
        # else:
        #     print("generate_data.py, line:24, esc expected")

        # create mask
        mask = []

        cv_im_gray = cv2.imread(os.path.join(data_new_path, origin_image), cv2.IMREAD_GRAYSCALE)
        cv_im_gray = cv2.resize(cv_im_gray, (img_width, img_height))
        circles = cv2.HoughCircles(cv_im_gray, 
                                   cv2.HOUGH_GRADIENT, 
                                   1.0, 
                                   im.size[0]/8.0, 
                                   param1=450,
                                   param2=30,
                                   minRadius=round(min(im.size[0], im.size[1])/50.0),
                                   maxRadius=round(max(im.size[0], im.size[1])/20.0))
        
        # only one circle
        only_one_x = []
        only_one_y = []
        only_one_w = []
        only_one_h = []
        count_circle = 0
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
                radius = indexCircle[2] # circle radius
                cv2.circle(cv_im, center, radius, (255, 0, 255), 3)
                mask_temp = np.zeros((im.size[0], im.size[1]), np.uint8)
                cv2.circle(mask_temp, center, radius, (255, 255, 255), thickness=-1)
                mask.append(mask_temp)
        if count_circle == 0:
            print("count_circle = 0, no circles found!")
            continue
        else:
            print("count_circle = ", count_circle)

        if IMAGE_SHOW:
            cv2.imshow(origin_image + "  <circle>", cv_im)
            flag = cv2.waitKey(0)
            if flag == 27:
                cv2.destroyWindow(origin_image + "  <circle>")
            elif flag == 13:
                new_origin_name = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "_circle_" + origin_image
                cv2.imwrite(os.path.join(data_no_use_path, new_origin_name), cv_im)
                cv2.destroyWindow(origin_image + "  <circle>")
                print("===============" + new_origin_name + "==SAVED===================")
            else:
                print("generate_data.py, line:55, esc or enter expected")

        crop_result = []

        for index in range(count_circle):
            # Copy that image using that mask
            print(cv_im.shape, " ", mask[index].shape)
            crop_cv_im = cv2.bitwise_and(cv_im, cv_im, mask=mask[index])
            # apply threshold
            _, thresh = cv2.threshold(mask[index], 1, 255, cv2.THRESH_BINARY)
            # find contour
            # contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            crop_cv_im = crop_cv_im[only_one_y[index]:only_one_y[index] + only_one_h[index],
                                    only_one_x[index]:only_one_x[index] + only_one_w[index]]
            crop_result.append(crop_cv_im)

        for index in range(count_circle):
            index -= 1
            if IMAGE_SHOW:
                cv2.imshow(origin_image + "  <crop>", crop_result[index])
                flag = cv2.waitKey(0)
                if flag == 27:
                    cv2.destroyWindow(origin_image + "  <crop>")
                elif flag == 13:
                    new_origin_name = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "_crop_" + origin_image
                    cv2.imwrite(os.path.join(data_no_use_path, new_origin_name), crop_result[index])
                    cv2.destroyWindow(origin_image + "  <crop>")
                    print("===============" + new_origin_name + "==SAVED===================")
                else:
                    print("generate_data.py, line:24, esc expected")

        ret_img.append(crop_cv_im)  # ensure that only one image is stored

    return ret_img

def generate_date_360(data_per_360_path, data_360_path):

    origin_images = os.listdir(data_per_360_path)
    count = 0
    for origin_image in origin_images:
        im = Image.open(os.path.join(data_per_360_path, origin_image))
        # print(origin_image[5:11])
        data_360_path_spec = data_360_path + "/" + origin_image[5:11]
        print("============================== " + data_360_path_spec + "  <saving> ==============================")
        for angle in range(number_angle):
            im_ro = im.rotate(angle * (360/number_angle))
            data_360_path_spec_save = data_360_path_spec + "/" + str(angle) + "_" + origin_image[5:11] + ".jpg"
            im_ro.save(data_360_path_spec_save, quality=95, subsampling=0)
            print(data_360_path_spec_save + "   \t\t\t<<<  angle = " + str(angle) + "  >>>   \t\t\t" + str(count))
            count += 1


# use for debug
def main():
    data_new_path = Global_Params.M_data_new_path
    data_gen_path = Global_Params.M_data_gen_path
    data_no_use_path = Global_Params.M_data_no_use_path
    data_per_360_path = Global_Params.M_data_per_360_path
    data_360_path = Global_Params.M_data_360_path
    clear(data_gen_path, data_no_use_path)
    circle_img = generate_data(data_new_path, data_gen_path, data_no_use_path)
    generate_date_360(data_per_360_path, data_360_path)

# 调用函数
if __name__ == '__main__':
    main()