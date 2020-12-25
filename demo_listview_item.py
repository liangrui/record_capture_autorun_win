# -*- coding: utf-8 -*-
"""
@author:liangrui
@file:test_win.py
@time:2020/12/25 9:36
@file_dese:
    解释与抽取表格数据
"""
from pywinauto import Application

app = Application().connect(path="C:\\Windows\\System32\\taskmgr.exe")
app["Windows 任务管理器"].window(title_re="进程", class_name="SysListView32").print_control_identifiers()
# 定位到控件
print("--"*30)
list1 = app["Windows 任务管理器"].child_window(title_re="进程",class_name="SysListView32")
c_count = list1.column_count()
cur_c = 1
for item in list1.items():
    cur_c += 1
    print(item.item_data()['text'], end=" ")
    if cur_c > c_count:
        print()
        cur_c = 1
