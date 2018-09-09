# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ZM_180701_mainW.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import crawler4HNkjtXMSB
import time
import sys
import threading

class Worker(QThread):
    trigger = pyqtSignal()

    def __init__(self):
        super(Worker,self).__init__()

    def run(self):
        print("Worker start");
        crawler4HNkjtXMSB.CrawlerThread()
        self.trigger.emit()

class Monitor(QThread):
    def __init__(self):
        super(Monitor,self).__init__()

    def run(self):
        print("Monitor start");
        while (crawler4HNkjtXMSB.crawler_start_flag == 1):
            time.sleep(1)
            print("CrawlerThread execute ing...\r\n")
        print("CrawlerThread finished...\r\n")


def SignalTestFunc():
    print("trigger 1 test signal\r\n")


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.PushButton = QtWidgets.QPushButton(Dialog)
        self.PushButton.setGeometry(QtCore.QRect(170, 230, 75, 23))
        self.PushButton.setObjectName("PushButton")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 361, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        self.PushButton.clicked.connect(self.ui_button_press)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.update_text("采集湖南省科技厅项目申报信息\r\n")
        self.update_text("采集的信息存储于软件所在路径download文件夹下\r\n")
        self.update_text("点击按钮  \"采集信息\"  开始信息采集（采集完成会有提示信息，采集过程可自行查看download文件夹内容）\r\n")

        self.thread = Worker()
        #self.threadMonitor = Monitor()
        self.thread.trigger.connect(self.update_crawler_finish_text)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "信息采集"))
        self.PushButton.setText(_translate("Dialog", "采集信息"))


    def ui_button_press(self):
        self.PushButton.setEnabled(0)
        print("ui_button_press\r\n")
        crawler4HNkjtXMSB.crawler_start_flag = 1
        self.thread.start()

        #self.threadMonitor.start()
        self.update_text("\r\n===》 信息采集开始")
        self.PushButton.setEnabled(0)

    def update_text(self, message):
        self.textBrowser.append(message)

    def update_crawler_finish_text(self):
        self.update_text("===》 信息采集结束")
        self.update_text("===》 请在文件夹 %s\download 下查看抓取的文件和信息\r\n"% sys.path[0])
        self.PushButton.setEnabled(1)