# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:reco.py
@time:2020/12/22 10:30
@file_dese: 
"""
# Writer : wojianxinygcl@163.com

# Data  : 2020.3.21
import base64
import sys
from collections import Counter

import cv2
import cv2 as cv
import numpy as np

from ocr_api import get_info
from one_dim_cluster import one_dim_jenks_breaks

path = 'pics/0001_07.png'
# 目标识别中获取
infos, data = get_info(path=path, is_include_raw=True)
# [[[x, y, w, h, 角度],文本,准确率],[...]]
raw_out = data["raw_out"]
for row in raw_out:
    print(row)
# (int(row[0][0] - row[0][2] * 0.5), int(row[0][1] - row[0][3] * 0.5))
x_list = np.array([int(x[0][0] - x[0][2] * 0.5) for x in raw_out])
# print('Counter(data)\n', Counter(x_list))  # 调用Counter函数
# rs_list = dict(Counter(x_list))
# rs_list = list(sorted(rs_list.items(), key=lambda x: x[1], reverse=True))
# # one_dim_cluster_show(x_list)
jnb = one_dim_jenks_breaks(x_list)
groups = jnb.groups_
bound_x = []
# for group in groups:
#     print(group)
#     std = np.std(group)
#     mean = np.mean(group)
#     print(mean,std)

# bound_x = dict([(i, sys.maxsize) for i in lables])
print("数据组数:%s" % len(groups))
for group in groups:
    group_ = []
    std = np.std(group)
    mean = np.mean(group)
    for c in group:
        if mean - std <= c <= mean + std:
            group_.append(c)
        else:
            print("过滤:", c, group)
    print(len(group_), len(group))
    bound_x.append(np.min(group_))
# print(bound_x)

# 显示处理图片
# base64_data = raw_data["img_detected"].replace("data:image/jpeg;base64,", "")
# imgData = base64.b64decode(base64_data)
# nparr = np.fromstring(imgData, np.uint8)
# img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
# cv2.imshow('recog rs', img_np)

# 从图像上处理
img = cv.imread(path)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 50,150 为二值化时的阈值 apertureSize为Sobel滤波器的大小
edges = cv.Canny(gray, 50, 150, apertureSize=3)
for row in raw_out:
    # 画实心点
    cv2.circle(gray, (int(row[0][0] - row[0][2] * 0.5), int(row[0][1] - row[0][3] * 0.5)), 3, (0, 0, 255),
               -1)  # 第五个参数我设为 - 1，表明这是个实点。
# cv.imshow('Canny Result', edges)
# cv.imwrite('Canny_Result.jpg', edges)
# cv.waitKey(0)
# 高效的霍夫线检测算法
# image：必须是二值图像，推荐使用canny边缘检测的结果图像；
# rho：线段以像素为单位的距离精度，double类型的，推荐用1.0；
# theta：线段以弧度为单位的角度精度，推荐用numpy.pi/180；
# threshold：累加平面的阈值参数，int类型，超过设定阈值才被检测出线段，值越大，基本上意味着检出的线段越长，检出的线段个数越少。根据情况推荐先用100试试；
# lines：这个参数的意义未知，发现不同的lines对结果没影响，但是不要忽略了它的存在；
# minLineLength：线段以像素为单位的最小长度，根据应用场景设置；
# maxLineGap：同一方向上两条线段判定为一条线段的最大允许间隔（断裂），超过了设定值，则把两条线段当成一条线段，值越大，允许线段上的断裂越大，越有可能检出潜在的直线段。
lines = cv.HoughLinesP(edges, 1.0, np.pi / 180, threshold=50, minLineLength=300, maxLineGap=10)
obj_lines = []
left_top_point = [sys.maxsize, sys.maxsize]
right_bottom_point = [0, 0]
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv.line(gray, (x1, y1), (x2, y2), (0, 255, 0), 2)
    obj_lines.append(((x1, y1), (x2, y2)))
    left_top_point[0] = np.min([left_top_point[0], x1])
    left_top_point[1] = np.min([left_top_point[1], y1])
    right_bottom_point[0] = np.max([right_bottom_point[0], x2])
    right_bottom_point[1] = np.max([right_bottom_point[1], y2])
cv.line(gray, (left_top_point[0], left_top_point[1]), (left_top_point[0], right_bottom_point[1]), (0, 255, 0), 2)
cv.line(gray, (right_bottom_point[0], left_top_point[1]), (right_bottom_point[0], right_bottom_point[1]), (0, 255, 0),
        2)
for value_x in bound_x:
    cv.line(gray, (int(value_x), left_top_point[1]), (int(value_x), right_bottom_point[1]),
            (0, 0, 255), 1)
cv.imshow('Visible lines', gray)
# # cv.imwrite('HoughLines_Result.jpg', img)
# cv.waitKey(0)
# cv.destroyAllWindows()

mean_v_pix = []
pixex_grap = gray.copy()
for i in range(left_top_point[0], right_bottom_point[0]):
    # 找到两条记录的分隔线段，以相邻两行的平均像素差大于100为标准
    m = np.mean(gray[left_top_point[1]:right_bottom_point[1], i])
    mean_v_pix.append(m)
for i, p in enumerate(range(left_top_point[0], right_bottom_point[0])):
    pixex_grap[left_top_point[1]:right_bottom_point[1], p] = mean_v_pix[i]
    # 在图像上绘制线段
    # horizontal_lines.append([0, i, self.w, i])
    # cv2.line(self.image, (0, i), (self.w, i), (0, 255, 0), 2)
# 1. src： 输入图，只能输入单通道图像，通常来说为灰度图
# 2. maxval： 当像素值超过了阈值（或者小于阈值，根据type来决定），所赋予的值
# 3. thresh_type： 阈值的计算方法，包含以下2种类型：
#                  cv2.ADAPTIVE_THRESH_MEAN_C：            区域内均值
#                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C：    区域内像素点加权和，权重为一个高斯窗口
# 4. type：二值化操作的类型，与固定阈值函数相同，用于控制参数2 maxval，包含以下5种类型：
# cv2.THRESH_BINARY： 黑白二值
# cv2.THRESH_BINARY_INV：黑白二值反转
# cv2.THRESH_TRUNC：
# cv2.THRESH_TOZERO：
# cv2.THRESH_TOZERO_INV：
# 5. Block Size： 图片中区域的大小
# 6. C ：阈值计算方法中的常数项
AdaptiveThreshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, -2)
vertical = AdaptiveThreshold.copy()
cv.imshow('Adaptive binary results', vertical)
# cv.waitKey(0)
scale = 20
verticalsize = int(vertical.shape[0] / scale)
verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
# vertical = cv2.dilate(vertical, verticalStructure, (-1, -1))
# vertical = cv2.erode(vertical, verticalStructure, (-1, -1))
# cv.imshow('erode', vertical)
# # cv.waitKey(0)

# cv.imshow('dilate', vertical)
# cv.waitKey(0)
# cv2.imshow("垂直线", vertical)


cv.imshow('gray Result', gray)
cv.waitKey(0)
cv.destroyAllWindows()
