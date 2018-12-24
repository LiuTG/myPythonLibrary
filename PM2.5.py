# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 17:37:12 2017

@author: Administrator
"""
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdate
from pylab import *
from datetime import datetime, timedelta
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

import time
import datetime
import requests
import lxml
import sys
import re
import pymysql
import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = 'ltg001235@163.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user = '603085386@qq.com'  # 收件人邮箱账号，为了后面易于维护，所以写成了变量

#itchat.auto_login(hotReload=True)



def incomeLine(x,y):
    #设置表格主题
    plt.style.use('seaborn-whitegrid')

    #定义x,y轴取值范围
    ax = plt.axis([0,366,1,600])

    #设置刻度
    xmajorLocator = MultipleLocator(1)
    #设置是否多附图在一个页面
    ax = subplot(111)
    ax.xaxis.set_major_locator(xmajorLocator)

    #marker参数：点的标记符号
    plt.plot(x,y,marker='o')
    #设置刻度标记字体大小
    plt.tick_params(axis='both',which='major',labelsize=10)
    plt.show();


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



#插入数据库
def insertMysql(date,pm25,city,startDate,endDate):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    #规避数据缺少时的错误
    if len(date) == len(pm25) + 2:
        index = 0
        insertCount = 0
        while index < len(pm25):
            #日期校验，不在起始时间内的日期不插入数据库
            if date[index] >= startDate and date[index] <= endDate:
                # SQL 插入语句
                sql = "insert into weather(wdate,pm25,city) values ('%s','%s','%s');" %(date[index],pm25[index],city)

                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                    index = index + 1
                    insertCount = index
                except Exception:
                    # 如果发生错误则回滚
                    db.rollback()

                    print(str(Exception))
            else:
                index = index + 1
    # 关闭数据库连接
    db.close()
    print("此次共插入"+str(insertCount)+"条天气数据")


#查询数据库（支持城市，起始日期筛选）
def selectMysql(city,startDate):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()


    if(startDate != None):
        sql ="select * from weather where STR_TO_DATE(wdate, '%%Y-%%m-%%d') >= '%s' and city = '%s'" % (startDate,city)
    else:
        sql = "select * from weather where city = '%s'" % (city)
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


#抓取PM25数据
def getPM25(startDate,endDate):

    # 输入参数合法性校验，比较是否输入的时间大于当前时间
    # python中字符串的大小比较，是按照字符顺序，从前往后依次比较字符的ASCII数值，例如‘abc’要小于‘abd’。因此，时间字符串也可以直接比大小。
    nowDate = time.strftime("%Y-%m-%d", time.localtime())
    if startDate > nowDate or endDate > nowDate:
        print(nowDate)

    # 从中提取年份，月份
    startYear = startDate[0:4]
    endYear = endDate[0:4]

    startMonth = startDate[5:7]
    endMonth = endDate[5:7]

    # 将01的月份转换为1
    if startMonth[0:1] == '0':
        startMonth = startMonth[1:2]

    if endMonth[0:1] == '0':
        endMonth = endMonth[1:2]


    # index从1开始
    index = int(startMonth)
    # 小于几代表抓取到该年几月分的值
    while index <= int(endMonth):
        #大多数网站采取了异步返回的方式，所以不能直接爬网站而是要直接调接口
        #上海，西安，北京，杭州
        #将年月分开，从而方便进行日期选择

        #当结束年份大于起始年份的，因为之前判断过起始日期必须小于结束日期，所以如果结束年份不大于起始年份时，只可能为相同年份下月份不同或同月不同日
        #if endYear > startYear:

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!暂时不支持跨年抓数据!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        urlYear = startDate[0:4]
        #由于月份从1开始所以位置指示器index从1开始，00为占0位用
        urlMonth = ['00','01','02','03','04','05','06','07','08','09','10','11','12']
        shUrl = 'http://tianqi.2345.com/t/wea_history/js/' + urlYear + urlMonth[index] + '/58362_' + urlYear + urlMonth[index] + '.js'
        xaUrl = 'http://tianqi.2345.com/t/wea_history/js/' + urlYear + urlMonth[index] + '/57036_' + urlYear + urlMonth[index] + '.js'
        bjUrl = 'http://tianqi.2345.com/t/wea_history/js/' + urlYear + urlMonth[index] + '/54511_' + urlYear + urlMonth[index] + '.js'
        hzUrl = 'http://tianqi.2345.com/t/wea_history/js/' + urlYear + urlMonth[index] + '/58457_' + urlYear + urlMonth[index] + '.js'



        #创建城市URL数组
        cityUrl = [shUrl,xaUrl,bjUrl,hzUrl]
        city = ['sh','xa','bj','hz']

        header_info = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://www.baidu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }

        cityIndex = 0
        while cityIndex < 4:
            #r为返回的对象，r.text为返回的正文
            r = requests.get(cityUrl[cityIndex],headers=header_info)
            #print(cityUrl[cityIndex])

            if r.status_code == 200 :
                #匹配并提取aqi:'97'中的97
                apiPattern = re.compile(r"aqi:\'(\d+)\'")
                #匹配日期，格式为：2018-08-07
                datePattern = re.compile(r'\d{4}-\d{2}-\d{2}')

                #先判断日期是否为在这区间内的是的话再去匹配污染物，在区间的话存入数据库
                dateResult = datePattern.findall(r.text)
                aqiResult = apiPattern.findall(r.text)

                insertMysql(dateResult,aqiResult,city[cityIndex],startDate,endDate)
                #print(aqiResult,dateResult)

            #循环控制位加1
            cityIndex = cityIndex + 1
        index = index + 1



#大于指定PM2.5数值的天数统计
#val为指定大小的PM2.5
#不限制日期范围时，传入None参数
def valPM25Day(val,startDate):
    bjResult = selectMysql("bj",startDate)
    shResult = selectMysql("sh",startDate)
    xaResult = selectMysql("xa",startDate)
    hzResult = selectMysql("hz",startDate)
    bjPM25 = []
    shPM25 = []
    xaPM25 = []
    hzPM25 = []
    xLine = []

    for row in bjResult:
        bjPM25.append(int(row[2]))
    for row in shResult:
        shPM25.append(int(row[2]))
    for row in xaResult:
        xaPM25.append(int(row[2]))
    for row in hzResult:
        hzPM25.append(int(row[2]))

    bjDays = 0
    shDays = 0
    xaDays = 0
    hzDays = 0

    for pm25 in bjPM25:
        if( pm25 > val ):
            bjDays = bjDays + 1

    for pm25 in shPM25:
        if (pm25 > val):
            shDays = shDays + 1

    for pm25 in xaPM25:
        if (pm25 > val):
            xaDays = xaDays + 1

    for pm25 in hzPM25:
        if (pm25 > val):
            hzDays = hzDays + 1

    print("--------------------------------------------------------")
    if (startDate != None):
        print("从" + startDate + "日开始统计的天气中：")
    print("西安PM2.5大于" + str(val) + "，共有" + str(xaDays) + "天")
    print("北京PM2.5大于" + str(val) + "，共有" + str(bjDays) + "天")
    print("上海PM2.5大于" + str(val) + "，共有" + str(shDays) + "天")
    print("杭州PM2.5大于" + str(val) + "，共有" + str(hzDays) + "天")
    print("--------------------------------------------------------")




#计算各个候选城市中PM2.5为最高值的出现天数
def maxPM25Day():
    bjResult = selectMysql("bj",None)
    shResult = selectMysql("sh",None)
    xaResult = selectMysql("xa",None)
    hzResult = selectMysql("hz",None)


    bjPM25 = []
    shPM25 = []
    xaPM25 = []
    hzPM25 = []
    xLine = []

    #从数据库中取出PM2.5的值
    for row in bjResult:
        bjPM25.append(int(row[2]))
    for row in shResult:
        shPM25.append(int(row[2]))
    for row in xaResult:
        xaPM25.append(int(row[2]))
    for row in hzResult:
        hzPM25.append(int(row[2]))




    index = 0
    maxPM25City = []
    maxPM25 = []
    while index < len(bjPM25):
        if bjPM25[index] - shPM25[index] > 0:
            if bjPM25[index] - xaPM25[index] > 0:
                if bjPM25[index] - hzPM25[index] >0:
                    maxPM25City.append("bj")
                    maxPM25.append(bjPM25[index])
                else:
                    maxPM25City.append("hz")
                    maxPM25.append(hzPM25[index])
            else:
                if xaPM25[index] - hzPM25[index] >0:
                    maxPM25City.append("xa")
                    maxPM25.append(xaPM25[index])
                else:
                    maxPM25City.append("hz")
                    maxPM25.append(hzPM25[index])
        else:
            if shPM25[index] - xaPM25[index] > 0:
                if shPM25[index] - hzPM25[index] >0:
                    maxPM25City.append("sh")
                    maxPM25.append(shPM25[index])
                else:
                    maxPM25City.append("hz")
                    maxPM25.append(hzPM25[index])
            else:
                if xaPM25[index] - hzPM25[index] > 0:
                    maxPM25City.append("xa")
                    maxPM25.append(xaPM25[index])
                else:
                    maxPM25City.append("hz")
                    maxPM25.append(hzPM25[index])
        index = index + 1

    print("----------------------------------------------------------------------------------------------------")
    print("西安在这几座城市中PM2.5值最高的天数为：" + str(maxPM25City.count("xa")) + "；PM2.5最大值为：" + str(max(xaPM25)))
    print("北京在这几座城市中PM2.5值最高的天数为：" + str(maxPM25City.count("bj")) + "；PM2.5最大值为：" + str(max(bjPM25)))
    print("上海在这几座城市中PM2.5值最高的天数为：" + str(maxPM25City.count("sh")) + "；PM2.5最大值为：" + str(max(shPM25)))
    print("杭州在这几座城市中PM2.5值最高的天数为：" + str(maxPM25City.count("hz")) + "；PM2.5最大值为：" + str(max(hzPM25)))
    print("----------------------------------------------------------------------------------------------------")




#实时更新到当天天气
#暂时不支持跨年抓数据（getPM25不支持）
def updateNow():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    # 取最后一条数据
    sql = "select  *  from  weather  order  by  id  desc  limit  1"


    # 执行SQL语句
    cursor.execute(sql)

    # 获取所有记录列表
    results = cursor.fetchall()

    lastDate = results[0][1]

    nowDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    # 数据库中不是最新天气
    if lastDate < nowDate:
        # 字符串转日期格式并加1天，从而形成起始时间
        d1 = datetime.datetime.strptime(lastDate, '%Y-%m-%d') + timedelta(days = 1)
        startDate = d1.strftime('%Y-%m-%d')
        getPM25(startDate,nowDate)


    # 关闭数据库连接
    db.close()


valPM25Day(150,"2018-01-01")







