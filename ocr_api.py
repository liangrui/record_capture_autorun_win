# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:ocr_api.py
@time:2020/12/18 14:48
@file_dese: 
"""
import os

import requests
import base64
import json
import cv2
import numpy as np

IP = "81.71.*.*"


def img_to_base64(img_path):
    with open(img_path, 'rb')as read:
        b64 = base64.b64encode(read.read())
    return b64


def get_info(path):
    info = []
    url = 'http://%s:8089/api/tr-run/' % (IP)
    img_b64 = img_to_base64(path)
    res = requests.post(url=url, data={'img': img_b64})
    rs = json.loads(res.text)
    if rs["code"] == 200:
        data = rs["data"]
        # 这里还得需要一个信息显示的排序
        data_tmp = sorted(data["raw_out"], key=lambda x: x[0][1])
        # print(data_tmp)
        old_v = 0
        h = 0
        row_data = []
        for i, row in enumerate(data_tmp):
            # 首行
            # (x, y, w, h, 角度)
            if i == 0:
                old_v = row[0][1]
                h = row[0][3]
                continue

            # 当遇到新行了
            # print((row[0][1] + row[0][1] * 0.5),old_v + h * 0.5)
            if abs((row[0][1] + row[0][3] * 0.5) - (old_v + h * 0.5)) >= (row[0][3] + h) * 0.5 * 0.5:
                if len(row_data) > 0:
                    row_data = sorted(row_data)
                    info.append(row_data)
                    row_data = []

            old_v = row[0][1]
            h = row[0][3]
            # print(row[1], end=" ")
            row_data.append((row[0][0], row[1]))
        # 把最后一行信息加入其中
        if len(row_data) > 0:
            row_data = sorted(row_data)
            info.append(row_data)
            row_data = []
        print("时间:", data['speed_time'])
        # 显示处理图片
        base64_data = data["img_detected"].replace("data:image/jpeg;base64,", "")
        imgData = base64.b64decode(base64_data)
        nparr = np.fromstring(imgData, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite("./pics/_%s" % (os.path.split(path)[-1]), img_np)
        return info
    else:
        return None
        # cv2.imshow('IMG', img_np)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


infos = get_info("./pics/050.png")
for info in infos:
    for xsrc in info:
        print(xsrc[1], end=" ")
    print()
