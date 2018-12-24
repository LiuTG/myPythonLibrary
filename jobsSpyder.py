# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:37:12 2017

@author: Administrator
"""
from bs4 import BeautifulSoup

import requests
import lxml
import sys
import re
import smtplib  # 加载smtplib模块
import itchat
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = 'ltg001235@163.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user = '603085386@qq.com'  # 收件人邮箱账号，为了后面易于维护，所以写成了变量

#itchat.auto_login(hotReload=True)



def mail(content):
    ret = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["三爷的考试监控", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["长官", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "证券从业考试作战情报"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, "q87623460")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 这句是关闭连接的意思
    except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    return ret


url = 'http://www.sac.net.cn/cyry/kspt/kstz/index.html'
r = requests.get(url)

if r.status_code == 200:
    the_soup = BeautifulSoup(r.content, 'lxml')
    the_soup = the_soup.find_all('a', attrs={'target': '_blank'})

    for one in the_soup:

        # print (one.get('title'))   #获取title字段
        if '3月' in one.get('title'):
            print(one)
            ret = mail(one.get('title'))
        else:
            print('考试报名时间暂未更新')
            #itchat.send('hw', toUserName='三爷')

