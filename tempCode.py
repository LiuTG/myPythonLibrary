from pyecharts import Bar,Line
#条形图生成
bar = Bar("PM2.5城市对比图", "涉及如下4个城市：西安，杭州，上海，北京")
bar.add("西安", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
bar.add("北京", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [51, 10, 6, 10, 35, 9])
# bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
#bar.render()    # 生成本地 HTML 文件


#折线图生成
date = [1,2,3,4,5,6]
PM25 = [13,21,34,167,234,2]
PM251 = [63,2,43,123,2,42]
line = Line("气温变化折线图", '2018-4-16', width=1200, height=600)
line.add("西安", date, PM25, mark_point=['average'],is_smooth=True)# is_datazoom_show=True)
line.add("上海", date, PM251, mark_line=['average'], is_smooth=True)

line.render('Line-High-Low.html')