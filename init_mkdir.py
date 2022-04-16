# -*- coding: utf-8 -*-

import os
import load_data
import Global_Params

DIRS = [
    Global_Params.M_data_new_path,
    Global_Params.M_data_gen_path,
    Global_Params.M_data_no_use_path,
    Global_Params.M_data_per_360_path,
    Global_Params.M_data_360_path,
    Global_Params.M_test_path,
    Global_Params.M_imageProcessTest_path,
    Global_Params.M_CIMC_Webcam,
    Global_Params.M_imageProcessTestAns_path,
    Global_Params.M_image_circle_test_path,
    Global_Params.M_pil_temp_copy_path,
    Global_Params.M_systemCamTest_path,
    Global_Params.M_model_save_path
]

def make_dirs():
    for path in DIRS:
        if os.path.exists(path) is False:
            os.mkdir(path)
            print("create ->", path)
    pre_360 = Global_Params.M_data_per_360_path
    trg_360 = Global_Params.M_data_360_path
    for name in load_data.CHESS_TABLE:
        path = os.path.join(pre_360, name)
        if os.path.exists(path) is False:
            os.mkdir(path)
            print("create ->", path)
        path = os.path.join(trg_360, name)
        if os.path.exists(path) is False:
            os.mkdir(path)
            print("create ->", path)


if __name__ == '__main__':
    make_dirs()
