# -*- coding: utf-8 -*-

M_data_new_path = "./data_new"
M_data_gen_path = "./data_360"
M_data_no_use_path = "./data_no_use"
M_data_per_360_path = "./data_pre_360"
M_data_360_path = "./data_360"
M_test_path = "./test"
M_test_image_process = "./test_image_process"

M_number_angle = 720

M_imageProcessTest_path = "./webcam"
M_CIMC_Webcam = "./webcam"
# M_imageProcessTest_path_old = "./test_image_process/imageProcessTest"
M_imageProcessTestAns_path = "./test_image_process/imageProcessTest_ans"
M_image_circle_test_path = "./test_image_process/image_circle_test"

M_pil_temp_copy_path = "./test_image_process/pil_temp_copy"

M_systemCamTest_path = "./test_image_process/systemCamTest"

M_origin_image_path = "./data/origin_image"

M_chess_info_txt = "./chessInfo.txt"
M_chess_vertify_txt = "./chessVertify.txt"

# M_model_save_path = "./model_save/boost_cnn_model.h5"

M_model_save_path = "./model_save"

M_epoch_number = 100

M_validation_split_rate = 0.1

M_num_classes = 14 + 1

M_valid_chess_number = 32

M_norm_size = 120

M_HOST_TEST = "127.0.0.1"  # IPV4 localhost
M_PORT_TEST = 6666

M_Test_Webcam = 5

M_point_up = 40 - 25
M_point_down = 1080 - 35
M_point_left = 300 - 50 - 5
M_point_right = 1920 - 500 - 10

M_up = (64)/1.0
M_down = (956)/1.0
M_left = (58)/1.0
M_right = (1056)/1.0

# board -> 54 ,  956 ,  54 ,  1068
# board -> 60 ,  970 ,  58 ,  1076
# board -> 66 ,  960 ,  66 ,  1078
# board -> 56 ,  964 ,  44 ,  1074
# board -> 50 ,  944 ,  60 ,  1086
# board -> 54 ,  956 ,  50 ,  1076
# board -> 60 ,  964 ,  56 ,  1082
# board -> 58 ,  968 ,  66 ,  1084
# board -> 68 ,  968 ,  74 ,  1092
# board -> 60 ,  968 ,  58 ,  1088
# board -> 60 ,  966 ,  56 ,  1088
# board -> 60 ,  966 ,  60 ,  1088
# board -> 62 ,  960 ,  64 ,  1086
# board -> 56 ,  910 ,  54 ,  1034
# board -> 56 ,  922 ,  56 ,  1036
# board -> 64 ,  934 ,  60 ,  1040
# board -> 62 ,  952 ,  44 ,  1046
# board -> 68 ,  954 ,  52 ,  830

# Premature end of JPEG file

M_point_lefttop = (M_point_left, M_point_up)
M_point_rightbottom = (M_point_right, M_point_down)

M_Circle_FLAG = False

M_GPU_ServerOne = False
