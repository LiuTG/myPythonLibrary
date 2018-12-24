import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdate
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def incomeLine(x,y):
    #设置表格主题
    plt.style.use('seaborn-whitegrid')

    #定义x,y轴取值范围
    ax = plt.axis([0,19,1,12000])

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



#2016年7月,2016年8月,2016年9月,2016年10月,2016年11月,2016年12月,2017年1月,2017年2月,2017年3月,2017年4月,2017年5月,2017年6月,2017年7月,2017年8月,2017年9月,2017年10月,2017年11月,2017年12月
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
y = [0, 100, 3079, 3682.6, 3682.6, 3520.5, 3425.23, 7594.8, 4431.2, 4697.9, 4500, 4500, 7623, 7623.5, 3259.89, 9747,
     9749, 10499, 10899.08]
incomeLine(x,y)