# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:37:12 2017

@author: Administrator
"""
from bs4 import BeautifulSoup

import pymysql
import requests
import lxml
import json
import threading
import sys
import re
import time
import io
import os
import smtplib  # 加载smtplib模块
import jieba
import datetime
import jieba.posseg as pseg
from collections import Counter
from email.mime.text import MIMEText
from email.utils import formataddr

#获取我的文章数据
def getMyPageData():
    # 点击
    pageClicks = []
    totalClicks = 0

    #url = 'http://www.woshipm.com/'
    #r = requests.get(url)
    path = os.path.expanduser(r"~/Desktop/1.txt")
    f = open(path, 'r')
    # 将文件读取光标回到文章开头

    content = f.read()

    #if r.status_code == 200:
    the_soup = BeautifulSoup(content, 'lxml')
    # 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False .


    the_soupSon = the_soup.find_all('div', attrs={'class': 'u-floatRight meta'})


    for one in the_soupSon:
        #分割字符串函数split，不带分隔符参数时，默认为空格为分隔符，返回数组
        pageClicks.append(one.get_text().split()[0])
        totalClicks = totalClicks + int(one.get_text().split()[0])


    print("总计阅读量：" + str(totalClicks))




