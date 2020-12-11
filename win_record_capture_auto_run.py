# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:win_record_capture_auto_run.py
@time:2020/11/27 10:04
@file_dese:
 1. windows系统下的录屏功能；
 2. windows系统下的截图功能；
 3. 自动启动应用程序功能
"""
import threading
import time
import win32api
from win32api import GetSystemMetrics

import cv2
import numpy as np
from PIL import ImageGrab, ImageChops, Image
from pywinauto.application import Application

is_stop = False


class AutoCmpPics(threading.Thread):
    def __init__(self):
        print("初始化...")
        threading.Thread.__init__(self)

    def window_capture_pil(self, path, x=0, y=0):
        width, heigh = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)  # 获得分辨率
        # 参数说明
        # 第一个参数 开始截图的x坐标
        # 第二个参数 开始截图的y坐标
        # 第三个参数 结束截图的x坐标
        # 第四个参数 结束截图的y坐标
        bbox = (x, y, width, heigh)
        im = ImageGrab.grab(bbox)

        # 参数 保存截图文件的路径
        im.save(path)

    def run(self):
        pic_base_file = "./pics/base.jpg"
        self.window_capture_pil(pic_base_file)
        for i in range(100):
            time.sleep(1)
            next_file = "./pics/%s.jpg" % i
            self.window_capture_pil(next_file)
            diff = ImageChops.difference(Image.open(pic_base_file), Image.open(next_file))
            if diff.getbbox():
                diff.save("./pics/diff_%s.png" % (i))
            pic_base_file = next_file

            if is_stop:
                break


class AutoAvi(threading.Thread):
    def __init__(self):
        print("初始化...")
        threading.Thread.__init__(self)

    def run(self):
        print("运行...")
        # 自动录屏
        fps, width, heigh = 14, GetSystemMetrics(0), GetSystemMetrics(1)  # 获得分辨率
        size = (width, heigh)
        video = cv2.VideoWriter("record_op.mp4", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
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
    # 启动自动录屏
    avi_thread = AutoAvi()
    avi_thread.setDaemon(True)
    avi_thread.start()

    # 启动屏幕变化检测
    pic_thread = AutoCmpPics()
    pic_thread.setDaemon(True)
    pic_thread.start()

    time.sleep(2)
    # 自动操作记事本
    app = Application().start('notepad.exe')
    time.sleep(1)
    app[' 无标题 - 记事本 '].menu_select("编辑(&E) -> 替换(&R)..")
    time.sleep(1)
    app['替换'].取消.click()
    time.sleep(1)
    # 没有with_spaces 参数空格将不会被键入。请参阅SendKeys的这个方法的文档，因为它是SendKeys周围的薄包装。
    app[' 无标题 - 记事本 '].Edit.type_keys("来自python程序的自动输入：你好，世界！！！", with_spaces=True)
    time.sleep(1)
    app[' 无标题 - 记事本 '].Edit.type_keys("自动化输入第二行信息：你好，中国！！！", with_spaces=True)
    time.sleep(1)
    app[' 无标题 - 记事本 '].Edit.type_keys("自动化输入第三行信息：你好，python！！！", with_spaces=True)
    app[' 无标题 - 记事本 '].menu_select('文件(&F) -> 退出(&X)')
    time.sleep(1)
    # app['记事本'].print_control_identifiers()
    app['记事本'].Button2.click()
    time.sleep(1)

    # 设置结束标记
    is_stop = True
    avi_thread.join()
    pic_thread.join()
