# -*- coding: UTF-8 -*-


import time
# 利息率
rate = 0.1
# 本金
principal = 1000
# 利息和
interest = 0
# 本息和
account = 0


# 本函数计算每月固定存入本金，指定月后累计的本金和数
# 每月固定存入本金（不可变） unitPrincipal
# 想要查看多少月后本息和是多少的月数 months
# 派息周期 payCycle
# 每个派息周期前后所包含的不计息时间 noPay
# 计算公式：
# 每个派息周期中的收益 = 每月本金*利率/365*派息周期；
# 月数中总共有多少个派息周期 = 月数对应天数/（派息周期+不计息时间）

#简化版，每月（30天）存储固定额的，每月（30天）计息一次，指定月后累计的本金和数（暂时只支持12月内）
# 本息和 account
def monthMoney(unitPrincipal,months):

    #当只输入一个统一金额时的计算
    lens = len(unitPrincipal)
    if months == 0:
        # 当不输入月数时，根据输入值个数确定月数
        months = len(unitPrincipal)

    i = 0
    interest =0
    # 本金和
    allPrincipal = 0
    while(i < months):
        # 核心公式：计算任意数量本金unitPrincipal，在rate利率下，存储365天的比例得到的利息interest
        # interest = unitPrincipal * rate * (months) / 12
        if(lens == 1):
            interest = unitPrincipal[0] * rate * (12 - i) / 12 + interest
            allPrincipal = allPrincipal + unitPrincipal[0]
        else:
            interest = unitPrincipal[i] * rate * (12 - i) / 12 + interest
            allPrincipal = allPrincipal + unitPrincipal[i]
        i = i + 1
    print(interest,allPrincipal + interest)

#unitPrincipal = [6500,6600,6700,6600,6700,6600,7100,6600,6100,6300]
unitPrincipal = [7300]

#monthMoney(unitPrincipal,10)

# 计算任意数量本金principal，在rate利率下，存储月数months，换算成365天的比例得到的利息interest（目前只支持一年的计算）
def baseInterest(principal,rate,months):
    # 利息
    interest = 0
    interest = principal * rate * months / 12
    print("计算任意数量本金principal，在rate利率下，存储月数months，换算成365天的比例得到的利息：")
    print(interest)
    return interest

#baseInterest(6000,0.105,9)


#在指定年度存钱计划后，计算每月要存多钱与指定存款后的财政赤字
def unitMoneySave():
    #获取当前月份
    nowMonth = time.strftime('%m', time.localtime(time.time()))

    #农历新年月份
    chineseNewYearMonth = 2


    # 将01的月份转换为1
    if nowMonth[0:1] == '0':
        nowMonth = nowMonth[1:2]

    # 本年投资剩余次数/月数，由于工资都是下一个月发，所以过新年的这个月工资不在本年度
    allMonth = 12 - int(nowMonth) + chineseNewYearMonth - 1

    #总额 #116500
    account = 116500
    #现有资金
    nowAccount = 30500
    #未完成额度
    needAccount = account - nowAccount

    #每月要存多钱
    unitMoney = (needAccount - baseInterest(nowAccount,0.105,allMonth)) / allMonth

    #现实中每月实际存款
    acMoney = 7000
    #财政赤字
    deficit = (unitMoney - acMoney) * allMonth

    print(unitMoney,deficit)

unitMoneySave()


