#!/usr/bin/env python
# encoding=utf-8

# 引入模块
import time
import codecs
from bs4 import BeautifulSoup
import requests
import os
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import ZM_180701_mainW as ZM_180701_mainW
import threading




# 程序下载的文件根目录
DOWNLOAD_FILE_ROOT_PATH = './download'

# 科技厅项目申报页面
HUNAN_KJT_XMSB_BASE_URL = 'http://www.hnst.gov.cn/xxgk/xmxx/xmsb/'

REQUESTS_TIMEOUT_SEC = 8
SIMU_SLEEP_SEC_TIME = 2



def sleepSec(sec):
    time.sleep(sec)
    return None

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


## 功能：用于读取网页和保存网页信息
## 返回：网页信息
def read_page_info(url, fileName):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    }
    res = requests.get(url, headers=header, timeout=REQUESTS_TIMEOUT_SEC)
    if(res):
        res.encoding = 'utf-8'
        #print(res.text)
        #保存网页信息
        with codecs.open(fileName, 'wb', encoding='utf-8') as fp:
            fp.write(res.text)
        return res.content
    else:
        print('read_page_info error')
        return None


## 功能：下载制定链接的文件并保存为指定名字
def download_file(url, fileName):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    }
    resDoc = requests.get(url, headers=header, timeout=REQUESTS_TIMEOUT_SEC)
    if(resDoc):
        with codecs.open(fileName, 'wb') as fpDoc:
            fpDoc.write(resDoc.content)
    else:
        print('download_file error')
    return None


## 功能：对单个项目的页面进行解析，下载正文到txt并下载附件
def parse_kjtXMSB_item_html(html, url_path, url_name, url):
    soup = BeautifulSoup(html, "html.parser")
    if(soup):
        main_soup = soup.find('div', attrs={'class': 'tys-main-zt-show'})
        if(main_soup):
            main_soup_info_file_name = url_name+'.txt'
            #print(main_soup)
            for download_link in main_soup.find_all('a'):
                try:
                    #print(download_link)
                    #print(download_link.text)
                    #print(download_link['href'])
                    #print(url_path+'/'+download_link.text)
                    #print(url+'/../'+download_link['href'])
                    sleepSec(SIMU_SLEEP_SEC_TIME)
                    download_file(url+'/../'+download_link['href'], url_path+'/'+download_link.text)
                except KeyError as e:
                    print('except: ', e)
            #input("输入任意字符进入下一个页面")

    return None


## 功能：解析科技厅项目申报页面的目录，并深入目录进行下一步解析
def parse_kjtXMSB_base_html(html, resFileName):
    soup = BeautifulSoup(html, "html.parser")
    if(soup):
        link_list_soup = soup.find('div', attrs={'class': 'tyl-main-right-list clearfix1'})
        if(link_list_soup):
            link_list = link_list_soup.find('tbody')
            if(link_list):
                #print(link_list)

                # 解析出来的内容写入文件
                #fp = codecs.open(resFileName, 'wb', encoding='utf-8')

                for link_tr in link_list.find_all('tr'):
                    detail = link_tr.find('td', attrs={'style':'width:773px'})
                    detail_time = link_tr.find('td', attrs={'align':'center'})
                    if(detail):
                        #解析出来的内容进行打印
                        #print(detail)
                        if(detail_time):
                            print(detail_time.text)
                        link_name = detail.find('a')
                        print(link_name['title'])
                        #print(link_name['href'])
                        #解析出来的内容写入文件
                        #fp.write(link_name['title'])
                        #fp.write('\r\n')
                        #fp.write(link_name['href'])
                        #fp.write('\r\n\r\n')

                        if (detail_time):
                            pathName = DOWNLOAD_FILE_ROOT_PATH + '/' + detail_time.text + ' ' + link_name['title']
                        else:
                            pathName = DOWNLOAD_FILE_ROOT_PATH + '/' + link_name['title']

                        mkdir(pathName)

                        item_url = HUNAN_KJT_XMSB_BASE_URL+link_name['href']
                        #print(item_url)
                        item_page_info_file_name = pathName + '/' + link_name['title'] + '.html'

                        sleepSec(SIMU_SLEEP_SEC_TIME)
                        html = read_page_info(item_url, item_page_info_file_name)
                        if(html):
                            parse_kjtXMSB_item_html(html, pathName, pathName+'/'+link_name['title'], item_url)

    return None

## 功能：抓取科技厅项目申报页面的信息并存储
def CrawlerFunc():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    mkdir(DOWNLOAD_FILE_ROOT_PATH)

    kjt_url = HUNAN_KJT_XMSB_BASE_URL+'index'+'.html'
    kjt_url_html_info_file_name = './hn_kjt_xmsb_url_'+'index'+'_html_info.html'
    kjt_url_parse_res_file_name = './hn_kjt_xmsb_url_'+'index'+'_parse_info.txt'
    index_val = 1
    while kjt_url:
        sleepSec(SIMU_SLEEP_SEC_TIME)
        html = read_page_info(kjt_url, kjt_url_html_info_file_name)
        if(html):
            parse_kjtXMSB_base_html(html, kjt_url_parse_res_file_name)
            kjt_url = HUNAN_KJT_XMSB_BASE_URL + 'index_' + str(index_val) + '.html'
            kjt_url_html_info_file_name = './hn_kjt_xmsb_url_' + 'index' + str(index_val) + '_html_info.html'
            kjt_url_parse_res_file_name = './hn_kjt_xmsb_url_' + 'index' + str(index_val) + '_parse_info.txt'
            index_val+=1
        else:
            kjt_url = None





# 功能：测试PYQT
def QtTest():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget();
    window.show()
    sys.exit(app.exec_())


#功能：带UI的  CrawlerFunc
def CrawlerFunc_UI():
    global MainWindow
    print("CrawlerFunc_UI() start")

    app = QApplication(sys.argv)

    MainWindow = QWidget()

    ui = ZM_180701_mainW.Ui_Dialog()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


def CrawlerThread():
    global crawler_start_flag
    global MainWindow
    if(crawler_start_flag==1):
        print("开始采集信息\r\n")
        #sleepSec(3)
        CrawlerFunc()
        crawler_start_flag = 0



## 主函数：下载科技厅项目申报页面的附件和正文
crawler_start_flag = 0


def main():
    print("start func")

    uiThread = threading.Thread(target=CrawlerFunc_UI(), name="UIThread")

    uiThread.join()

if __name__ == '__main__':
    main()