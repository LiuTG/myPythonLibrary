# /usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from lxml import etree
import xlrd,xlwt,xlutils
import time


cookie = {
    'Cookie':'JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
             'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644; '
             'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
             'index_location_city=%E6%B7%B1%E5%9C%B3; '
             'TG-TRACK-CODE=index_navigation; _gat=1; '
             '_gid=GA1.2.807135798.1504227456; _ga=GA1.2.1721572155.1504227456; '
             'LGSID=20170901085741-8ea70793-8eb0-11e7-902f-5254005c3644; '
             'LGRID=20170901095027-ed9ebf87-8eb7-11e7-902f-5254005c3644; '
             'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
             'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504230623;'
             'SEARCH_ID=a274b85f40b54d4da62d5e5740427a0a'
}

headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/60.0.3112.90 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_java?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
}
cookies = {
    'Cookie': 'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644;'
              'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
              'index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=7277bc08d137413dac2590cea0465e39; '
              'TG-TRACK-CODE=search_code; JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
              'PRE_UTM=; PRE_HOST=; '
              'PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; '
              'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3413383.html; _gat=1; _'
              'gid=GA1.2.807135798.1504227456; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504252636; _ga=GA1.2.1721572155.1504227456; '
              'LGSID=20170901153335-dd437749-8ee7-11e7-903c-5254005c3644; '
              'LGRID=20170901155728-336ca29d-8eeb-11e7-9043-5254005c3644',
}
data = {
    'first': False,
    'pn':1,
    'kd': '高级产品经理', #搜索的职位关键字
    'city':"上海"
}

def get_job(data):
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
    page = requests.post(url=url, cookies=cookie, headers=headers, data=data)
    page.encoding = 'utf-8'
    result = page.json()
    jobs = result['content']['positionResult']['result']

    book = xlwt.Workbook(encoding='utf-8')  # 创建excel对象
    sheet = book.add_sheet('sheet1')  # 添加一个表

    line = 0

    for job in jobs:


        companyShortName = job['companyShortName']
        positionId = job['positionId']  # 主页ID
        companyFullName = job['companyFullName']  # 公司全名
        companyLabelList = job['companyLabelList']  # 福利待遇
        companySize = job['companySize']  # 公司规模
        industryField = job['industryField']
        createTime = job['createTime']  # 发布时间
        district = job['district']  # 地区
        education = job['education']  # 学历要求
        financeStage = job['financeStage']  # 上市否
        firstType = job['firstType']  # 类型
        secondType = job['secondType']  # 类型
        formatCreateTime = job['formatCreateTime']  # 发布时间
        publisherId = job['publisherId']  # 发布人ID
        salary = job['salary']  # 薪资
        workYear = job['workYear']  # 工作年限
        positionName = job['positionName']  #
        jobNature = job['jobNature']  # 全职
        positionAdvantage = job['positionAdvantage']  # 工作福利
        positionLables = job['positionLables']  # 工种

        detail_url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)
        response = requests.get(url=detail_url, headers=headers, cookies=cookies)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)
        #获取职位JD
        desc = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')

        print(companyFullName)
        print('%s 拉勾网链接:-> %s' % (companyShortName, detail_url))

        print('职位：%s' % positionName)
        sheet.write(line, 0, positionName)
        print('职位类型：%s' % firstType)
        sheet.write(line, 1, firstType)
        print('薪资待遇：%s' % salary)
        sheet.write(line, 2, salary)
        print('职位诱惑：%s' % positionAdvantage)
        sheet.write(line, 3, positionAdvantage)
        print('地区：%s' % district)
        sheet.write(line, 4, district)
        print('类型：%s' % jobNature)
        sheet.write(line, 5, jobNature)
        print('工作经验：%s' % workYear)
        sheet.write(line, 6, workYear)
        print('学历要求：%s' % education)
        sheet.write(line, 7, education)
        print('发布时间：%s' % createTime)
        sheet.write(line, 8, createTime)

        x = ''
        for label in positionLables:
            x += label + ','
        print('技能标签：%s' % x)
        print('公司类型：%s' % industryField)
        for des in desc:
            print(des)
        line = line + 1
        if line == 6:
            break

    filename = xlsfile = r"C:\Users\LTG\Desktop\Account.xls"
    book.save(filename)
    #time.sleep(0.01)


def url(data):
    for x in range(1,50):
        data['pn'] = x
        get_job(data)

if __name__ == '__main__':
    url(data)


#写数据
def write_excel(filename, data):
    book = xlwt.Workbook(encoding='utf-8')            #创建excel对象
    sheet = book.add_sheet('sheet1')  #添加一个表
    sheet.write(0, 0, 'EnglishName')  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容
    book.save(filename) #保存excel



