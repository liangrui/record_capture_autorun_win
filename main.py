# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:demo.py
@time:2020/11/27 10:04
@file_dese:
"""
import sys
import threading

from pywinauto.application import Application
import time

from PIL import ImageGrab
from win32api import GetSystemMetrics
import numpy as np
# import cv2
import PlayMusic
from PlayMusic import PalySound

is_stop = False


class AutoAvi(threading.Thread):
    def __init__(self):
        print("初始化...")
        threading.Thread.__init__(self)

    def run(self):
        print("运行...")
        # 自动录屏
        fps, width, heigh = 14, GetSystemMetrics(0), GetSystemMetrics(1)  # 获得分辨率
        size = (width, heigh)
        video = cv2.VideoWriter("1.mp4", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
        count = 1
        while 1:
            print("图像%s" % (count))
            bbox = (0, 0, width, heigh)  # 四个参数代表了开始截图的x,y，结束截图的x,y，后两个可以看电脑
            im = ImageGrab.grab(bbox)
            video.write(np.array(im))  # 将img convert ndarray
            if is_stop:
                print("视频录取完成...")
                video.release()
                break
            count += 1


if __name__ == '__main__':
    # time.sleep(2)
    # # 启动自动录屏
    # avi_thread = AutoAvi()
    # avi_thread.setDaemon(True)
    # avi_thread.start()
    #
    # # 启动屏幕变化检测
    # pic_thread = AutoCmpPics()
    # pic_thread.setDaemon(True)
    # pic_thread.start()

    # 用来记录刷新次数
    n_total_count = 0
    app = Application().connect(path='D:\zd_ghzq\TdxW.exe')
    main_app = app["国海证券金探号超级终端V7.00"]
    # 第一次刷新
    main_app['刷新'].click()
    list1 = main_app.child_window(title_re="List1", class_name="SysListView32")
    items = list1.items()
    c_count = list1.column_count()
    cur_c = 1
    for i, item in enumerate(items):
        print(item['text'])
        print(item)
        cur_c += 1
        print(item.GetItem(), end=" ")
        if cur_c > c_count:
            print()
            cur_c = 1
    pre_count = list1.item_count()
    n_total_count += 1
    print("第%s次刷新，共有%s条记录." % (n_total_count, pre_count))
    while True:
        time.sleep(5)
        main_app = app["国海证券金探号超级终端V7.00"]
        main_app['刷新'].click()
        list1 = main_app.child_window(title_re="List1", class_name="SysListView32")
        c_count = list1.item_count()
        n_total_count += 1
        print("第%s次刷新，共有%s条记录." % (n_total_count, pre_count))
        # if c_count > pre_count:
        print("记录有更新.")
        sound_thread = PalySound()
        # sound_thread.setDaemon(True)
        sound_thread.start()
        a = input("请输入任意值继续...")
        sound_thread.terminate()
        # else:
        #     print("记录不变.")
        pre_count = c_count



    # ListViewWrapper.Items
    # count = 0
    # while True:
    #     app['国海证券金探号超级终端V7.00']['刷新'].click()
    #     time.sleep(1)
    #     if count > 50:
    #         break
    #     count += 1

    # is_stop = True
    # avi_thread.join()
    # pic_thread.join()
