# -*-*- coding utf-8 -*-*-
# read image from computer camera(USE camera)

import cv2
import os # call system API
import datetime
from PIL import Image

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

    test_ImageStore = "./test_image_process/systemCamTest";
    ImageStorePath = "./data/origin_image";
    count = 0;

    while(True):
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


# use for debug
def main():
    getOriginImage()

# 调用函数
if __name__ == '__main__':
    main()