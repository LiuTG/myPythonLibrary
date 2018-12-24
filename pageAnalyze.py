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
import os
import smtplib  # 加载smtplib模块
import jieba
import datetime
import jieba.posseg as pseg
from collections import Counter
from email.mime.text import MIMEText
from email.utils import formataddr




#插入数据库
def insertMysql(pageTitle,length,paragraph,type,pageAuthor,pageLike,pageCollect,pageClicks,pageDate):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python",charset="utf8")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    index = 0
    while index < len(pageTitle):
        # SQL 插入语句
        # 插入抓到数据时的当前时间
        sql = "insert ignore into page(title,type,date,words,paragraph,author,likes,collect,clicks,inserttime) values ('%s','%d','%s','%d','%d','%s','%d','%d','%s','%s');" %(pageTitle[index],type,str(pageDate[index]),int(length[index]),int(paragraph[index]),str(pageAuthor[index]),int(pageLike[index]),int(pageCollect[index]),str(pageClicks[index]),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #print(sql)
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





def getPageContent(pageTitle,pageHttp,path,type,pageAuthor,pageLike,pageCollect,pageClicks,pageDate):
    #存储每篇文章长度
    length = []
    #每篇文章段数
    paragraph = []

    for url in pageHttp:
        #初始化长度数组
        lengthTemp = 0
        r = requests.get(url)

        if r.status_code == 200:
            the_soup = BeautifulSoup(r.content, 'lxml')
            article = the_soup.find('article')
            #由于其内容都存在P标签中，所以如此获得网页内容
            the_soup = article.find_all('p')
            #文章的标题获取，文章的所有标题都存在h2标签中
            the_title = article.find_all('h2')
            #print(the_title)


            #拿到本篇文章的段数，实际就是有多少个P标签
            paragraph.append(len(the_soup))
            for one in the_soup:
                lengthTemp = lengthTemp + len(one.get_text())


        length.append(lengthTemp)

    index = 0

    #存储方案1：mysql中
    #传入：标题，文字长度，段数的集合,type0代表热门，type1代表最新
    insertMysql(pageTitle,length,paragraph,type,pageAuthor,pageLike,pageCollect,pageClicks,pageDate)

    #存储方案2：txt文件中
    '''
    #使用a+将会在文件不存在时，自动创建文件
    f = open(path, 'a+', encoding='gbk')
    #将文件读取光标回到文章开头
    f.seek(0)
    lines = f.readlines()  # 读取所有行
    if(len(lines)==0):
        last_line = ''
    else:
        last_line = lines[-2]  # 取最后第二行
        f.close()


    #本网站默认为12条数据分页，判断是否更新文章，更新了再插入
    #-1代表数组最后一个值，比较从网站抓取到的文章名称的最后一条是否与文件的最后一条相同
    if pageTitle[-1] in last_line:
        print("网站未更新最新文章")
    else:
        f = open(path, 'a')
        for one in pageTitle:
            strtemp = one + '\n' + str(length[index]) + '；段数：' + str(paragraph[index]) + '\n'
            f.write(strtemp)

            #print(one,length[index],'\n')
            index = index + 1
        print("抓取完成！更新了" + str(index) + "条数据 " + path)
        f.close()
    '''

#最新文章列表页数据获取
def getPageList():
    # 存放找到的标题，链接，作者，点赞，收藏，点击量，发布日期
    pageTitle = []
    pageHttp = []
    pageAuthor = []
    pageLike = []
    pageCollect = []
    pageClicks = []
    pageDate = []
    url = 'http://www.woshipm.com/'
    r = requests.get(url)


    if r.status_code == 200:
            the_soup = BeautifulSoup(r.content, 'lxml')
            # 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False .


            the_soupSon = the_soup.find_all('h2', attrs={'class': 'post-title'})
            #作者，点赞，收藏
            the_soupSon2 = the_soup.find_all('div', attrs={'class': 'stream-list-meta'})

            for one in the_soupSon:
                # 找到父节点中存储标题的子节点
                son = one.find('a')
                pageTitle.append(son.get('title'))
                pageHttp.append(son.get("href"))
            #抓取作者，点赞，收藏
            for one in the_soupSon2:

                son1 = one.find('span',attrs={'class': 'author'})
                pageAuthor.append((son1.get_text()).strip())
                son2 = one.find('time')
                pageDate.append((son2.get_text()).strip())
                sons = one.find_all('span', attrs={'class': 'post-meta-item'})
                # 将汉字万转换为数字
                if(str(sons[0].get_text())[-1] == '万'):
                    pageClicks.append(int(float(sons[0].get_text()[:-1])*10000))
                else:
                    pageClicks.append(sons[0].get_text())
                pageCollect.append(sons[1].get_text())
                pageLike.append(sons[2].get_text())



            print("最新文章标题，地址抓取完毕，开始抓取正文......")
            path = os.path.expanduser(r"~/Desktop/words.txt")
            type = 1
            getPageContent(pageTitle,pageHttp,path,type,pageAuthor,pageLike,pageCollect,pageClicks,pageDate)




#7日最热文章列表页数据获取
def getHotPageList():
    # 存放找到的标题，链接，作者，点赞，收藏，点击量，发布日期
    pageTitle = []
    pageHttp = []
    pageAuthor = []
    pageLike = []
    pageCollect = []
    pageClicks = []
    pageDate = []

    url = 'http://www.woshipm.com/__api/v1/browser/popular'
    r = requests.get(url)

    if r.status_code == 200:
            # 获取响应内容
            allData = json.loads(r.text)
            #解析Json
            content = allData['payload']

            for item in content:
                pageTitle.append(item['title'])
                pageHttp.append(item['permalink'])
                pageAuthor.append(item['author']['name'])
                pageLike.append(item['like'])
                pageCollect.append(item['bookmark'])
                #将汉字万转换为数字
                if (str(item['view'])[-1] == '万'):
                    pageClicks.append(int(float(item['view'][:-1]) * 10000))

                else:
                    pageClicks.append(item['view'])

                pageDate.append(item['date'])

            print("7日最热文章标题，地址抓取完毕，开始抓取正文......")
            path = os.path.expanduser(r"~/Desktop/hotwords.txt")
            type = 0

            getPageContent(pageTitle, pageHttp, path, type, pageAuthor, pageLike, pageCollect, pageClicks, pageDate)







# 创建多个线程
if __name__ == "__main__":
    startTime = time.time()
    # 生成一个线程实例
    t1 = threading.Thread(target=getHotPageList())
    # 生成另一个线程实例
    t2 = threading.Thread(target=getPageList())
    # 启动线程
    t1.start()
    t2.start()

    print("共用时" + str(time.time() - startTime))




#创建停用词列表
def stopwordslist():
    stopwords = ['，','段数','；','：',' ','的','（','）','+','.','“','”',"!","！","，",'?','？','了','、','｜',';']
    return stopwords

#将文章进行分词并统计元素出现次数
def wordsAly2():
    try:
        path = os.path.expanduser(r"~/Desktop/hotwords.txt")
        f = open(path, 'r', encoding='GB2312')
        lines = ''
        #用空格换掉换行符
        for line1 in f.readlines():
            lines = lines + line1.replace("\n"," ")
        #print(lines)

        # 默认是精确模式分词
        seg_list = jieba.cut(lines)
        # 这里加载停用词的路径
        stopwords = stopwordslist()
        outstr = []
        for word in seg_list:
            if word not in stopwords:
                if word != '\t':
                    outstr.append(word)

        print(outstr)



        f.close()
        #统计数组中元素出现次数
        print(Counter(outstr))

        # 分词后并标注词性
        words = pseg.cut(lines)

        # flag为词性
        #for word, flag in words:
            #print('%s %s' % (word, flag))
    except FileNotFoundError:
        print(path)
        print("异常：文件不存在")



def wordsAly():
    try:
        path = os.path.expanduser(r"~/Desktop/words.txt")
        f = open(path, 'r', encoding='GB2312')
        lines = ''
        #用空格换掉换行符
        for line1 in f.readlines():
            lines = lines + line1.replace("\n"," ")
        #print(lines)

        # 默认是精确模式分词
        seg_list = jieba.cut(lines)

        # 将序列中的元素以指定的字符连接生成一个新的字符串
        print(seg_list)

        f.close()
        #统计数组中元素出现次数
        print(Counter(seg_list))


        #分词后并标注词性
        words = pseg.cut(lines)

        #flag为词性
        #for word, flag in words:
            #print('%s %s' % (word, flag))
    except FileNotFoundError:
        print(path)
        print("异常：文件不存在")


#计算点赞因子数量
def likesAly():
    title = []
    likes = []
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "python", charset="utf8")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # 查询总点赞数
    sql = "select SUM(%s) from page" % ('likes')
    sql2 = "select title,likes from page"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.execute(sql2)
        results2 = cursor.fetchall()

        #调试代码
        #print(sql)
        #print(results[0][0])
        #总点赞数
        countLikes = results[0][0]
        #取标题与点赞数
        for row in results2:
            title.append(row[0])
            likes.append(row[1])
    except:
        print("Error: unable to fecth data")

    # 关闭数据库连接
    db.close()

    #开始分词
    #存储结果
    outstr = []
    #未去重的分词结果
    allStr = []
    score = []

    # 默认是精确模式分词
    titleLen = len(title)
    index = 0
    while(index < titleLen):
        seg_list = jieba.cut(title[index])
        # 这里加载停用词的路径
        stopwords = stopwordslist()

        for word in seg_list:
            if word not in stopwords:
                # 判断word是不是在数组中，是返回ture
                if word in outstr:
                    #取索引号，更新分数，将相同的元素的分数进行合并
                    needUpdate = outstr.index(word)
                    score[needUpdate] = score[needUpdate] + likes[index]


                else:
                    outstr.append(word)
                    score.append(likes[index])
                #所有的分词结果存储
                allStr.append(word)
        index = index + 1

    # 统计数组中元素出现次数
    print(outstr.index("行业"))
    print(score[outstr.index("行业")])
    print(Counter(allStr))

likesAly()












