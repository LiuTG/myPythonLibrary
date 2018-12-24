# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:37:12 2017

@author: Administrator
"""
from bs4 import BeautifulSoup

import pymysql
import requests
import lxml
import sys
import re
import smtplib  # 加载smtplib模块
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



#每天查询多次，将匹配中的之前未汇报过的演出进行推送

#将演出详情保存下来，由我进行打标签，那些是想去的，那些不想去进行机器学习


#插入数据库
def insertMysql(pdate,title,http,location):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python",charset="utf8")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    index = 0
    while index < len(title):
        # SQL 插入语句
        sql = "insert ignore into performance(pdate,title,http,location) values ('%s','%s','%s','%s');" %(pdate[index],title[index],http[index],location[index])

        try:
             # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            index = index + 1
        except Exception:
            # 如果发生错误则回滚
            db.rollback()

            print(str(Exception))

    # 关闭数据库连接
    db.close()


#查询数据库
def selectMysql(title):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python",charset="utf8")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "select * from performance where title = '%s'" % (title)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

        return results
    except:
        print("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()





def getPerformanceContent(urls):
    for url in urls:
        r = requests.get(url)

        if r.status_code == 200:
            the_soup = BeautifulSoup(r.content, 'lxml')

            # 寻找已经售空的票位
            sellOut = the_soup.find_all('div', attrs={'class': 'ticket normal-list-item list-disabled'})

            for one in sellOut:

                # 在售的票位
                #sellNow = one.find_all('div',)

                res = one.get("data-price")

                print(res)




#搜索结果的列表页数据获取
def getPerformanceList(keyword):
    # 存放找到的演出结果：标题，链接，演出时间，场馆
    shTitle = []
    shHttp = []
    shTime = []
    shLocation = []
    for kw in keyword:
        url = 'https://www.tking.cn/search/' + kw
        r = requests.get(url)

        if r.status_code == 200:
            the_soup = BeautifulSoup(r.content, 'lxml')
            # 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False .
            # 查找到节目信息的总父节点
            the_soup = the_soup.find_all('a', attrs={'class': 'show-items sa_entrance'})

            for one in the_soup:
                # 找到父节点中存储标题的子节点
                son = one.find('div', attrs={'class': 'show-name'})
                # 由于摩天轮网站搜索结果不精确所以再里面二次判断下是否确实有关键字，有再判断是否是上海的
                # 如：搜索“肯尼基”会出现：【上海站】英国肯尼斯·布拉纳剧团戏剧放映：《冬天的故事》
                for check in keyword:
                    if check in son.get('title'):
                        # 查找大字符串中的小字符串
                        # 查找上海有无表演
                        if "上海" in son.get('title'):
                            # 获取标题与链接
                            # print (son.get('title') + one.find('div',attrs={'class': 'show-time'}).get_text() + one.get('href')+one.find('div', attrs={'class': 'show-addr'}).get_text())

                            shTitle.append(son.get('title'))
                            shHttp.append("https://www.tking.cn" + one.get('href'))
                            shTime.append(one.find('div', attrs={'class': 'show-time'}).get_text())
                            shLocation.append(one.find('div', attrs={'class': 'show-addr'}).get_text())
    getPerformanceContent(shHttp)

    #insertMysql(shTitle, shHttp, shTime, shLocation)
    print(str(shTitle)+'\n'+str(shHttp))







keyword = ["萨克斯", "李宗盛", "林子祥", "郑中基", "肯尼基"]
getPerformanceList(keyword)