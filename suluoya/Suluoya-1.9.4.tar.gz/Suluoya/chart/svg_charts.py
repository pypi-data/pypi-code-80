import pygal

#折线图
def line(data={},x_labels=[],path='line'):
    l=pygal.Line()
    if data=={}:
        data={'旺季':[2,3,6,5,9,16,18],
            '淡季':[1,2,3,5,6,2,7]}
    if x_labels==[]:
        l.x_labels=list(map(str,range(2008,2014)))
    for i,j in data.items():
        l.add(i,j)
    l.x_labels=x_labels
    l.render_to_file(f'{path}.svg')



#饼图
def pie(dic=None,path='pie'):
    pie=pygal.Pie(inner_radius=0.6)
    if dic==None:
        pie.add("优秀",19)
        pie.add("良好",36)
        pie.add("合格",36)
        pie.add("不合格",4)
        pie.add("较差",2)
    elif type(dic)==dict:
        for i,j in dic.items():
            pie.add(i,j)
    
    pie.render_to_file(f'{path}.svg')

#散点图
def scatter(data=[[1,3],[2,4]],name=['Suluoya'],title='Suluoya',path='scatter-plot'):
    xy_chart = pygal.XY(stroke=False) # stroke参数是指是否禁用连线
    xy_chart.title = title
    for i in name:
        xy_chart.add(i, data)
    xy_chart.render_to_file(path+'.svg')
    
    
    
#
##Bar()绘制条形图
#hist = pygal.Bar()
#x= ['1', '2', '3', '4', '5', '6']
#y=[10,30,15,35,67,43]
#hist.x_labels =x
#hist.x_title = "Result"
#hist.y_title = "Number"
#hist.add('条形图', y)
#hist.render_to_file('bar.svg')

#hist=pygal.Bar(margin_bottom=10,#图与低端距离，类似的有上下左右
#                  height=450,
#                  #style=NeonStyle,#设置绘图风格，pygal拥有23种style，
#                  #其它style可选：'BlueStyle', 'CleanStyle', 'DarkColorizedStyle', 'DarkGreenBlueStyle', 'DarkGreenStyle', 'DarkSolarizedStyle', 'DarkStyle', 'DarkenStyle', 'DefaultStyle', 'DesaturateStyle', 'LightColorizedStyle', 'LightGreenStyle', 'LightSolarizedStyle', 'LightStyle', 'LightenStyle', 'NeonStyle', 'ParametricStyleBase', 'RedBlueStyle', 'RotateStyle', 'SaturateStyle', 'SolidColorStyle', 'Style', 'TurquoiseStyle'
#                  
#                  ##title设置
#                  title=u'Some points', #图标题
#                  x_title='X Axis',#x轴标题
#                  y_title='Y Axis',#y轴标题
#                  
#                  ##label设置
#                  show_x_labels=True,#显示x轴标签
#                  x_label_rotation=20,#x轴标签倾斜角度
#                  x_labels = list('ABCD'),#自定义x轴标签
#                  value_formatter = lambda x: "%.2f" % x,#y轴刻度值格式化输出
#                  
#                  ##图例legend设置
#                  show_legend=True,#开启图例
#                  legend_at_bottom=True,#图例放置于底部
#                  legend_at_bottom_columns=2,#图例标签显示行数
#                  legend_box_size=12,#图例前箱子大小
#                  
#                  ##坐标轴axis设置
#                  include_x_axis=True,#坐标轴开启
#                  range=(0, 30),#设置y轴刻度值范围
#                  
#                  secondary_range=(10, 25),#第二坐标轴刻度范围
#                  xrange=(0,10),#x轴刻度范围
#                  
#                  ##柱子上text设置
#                  print_values=True,#开启柱子上文本
#                  print_values_position='top',#文本位置
#                  style=LightSolarizedStyle(
#                  value_font_family='googlefont:Raleway',#文本字体设置
#                  value_font_size=15,#大小
#                  value_colors=('red','blue'),#颜色设置
#                  ),
#                  
#                 )
#
#
##HorizontalBar()创建水平条形图
#bar=pygal.HorizontalBar()
#bar.title="小学生成绩分布图"
#bar.add("优秀",19)
#bar.add("良好",36)
#bar.add("合格",36)
#bar.add("不合格",4)
#bar.add("较差",2)
#bar.render_to_file('bar1.svg')
#
#
##HorizontalStackedBar()绘制水平堆叠条形图
#bar2=pygal.HorizontalStackedBar()
#bar2.title='员工销售情况图'
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#bar2.x_labels=["小二","张三","李四","小桐","王五","小小","赵六"]
#bar2.x_title='销售量'
#bar2.y_title='人员'
#bar2.add('旺季',x)
#bar2.add('淡季',y)
#bar2.render_to_file('bar2.svg')
#
##XY()绘制函数图像
##数学公式这些要用到math模块
#from math import cos 
#xy_chart = pygal.XY()
#xy_chart.title = '函数图'
##需提供一个横纵坐标元组作为元素的列表,即提供几个（x,y）坐标点的列表
#xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
#xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
#xy_chart.add('x = 1', [(1, -5), (1, 5)])
#xy_chart.add('x = -1', [(-1, -5), (-1, 5)])
#xy_chart.add('y = 1', [(-5, 1), (5, 1)])
#xy_chart.add('y = -1', [(-5, -1), (5, -1)])
#xy_chart.render_to_file('bar_chart.svg')
#
#
##HorizontalLine()绘制水平折线图
#line1=pygal.HorizontalLine()
#line1.title='销售线图'
#line1.x_labels=map(str,range(2008,2014))
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#line1.add('旺季',x)
#line1.add('淡季',y)
#line1.render_to_file('line1.svg')
#
##StackedLine(fill=True)绘制叠加侧线图
#line2=pygal.StackedLine(fill=True)
#line2.title='叠加侧线图'
#line2.x_labels=map(str,range(2008,2014))
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#line2.add('旺季',x)
#line2.add('淡季',y)
#line2.render_to_file('line2.svg')
#
##Radar()绘制雷达图
#radar=pygal.Radar()
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#radar.title='淡旺季雷达分布图'
#radar.add('旺季',x)
#radar.add('淡季',y)
#radar.render_to_file('radar.svg')
#
##Histogram()绘制直方图
##使用函数Histogram()绘制直方图是一个特殊的条形图，它包含3个数值：纵坐标高度，横坐标开始和横坐标结束。
#gram=pygal.Histogram()
#gram.title='直方图'
#gram.add('宽直条',[(4,0,10),(4,5,12),(2,0,16)])
#gram.add('窄直条',[(9,1,2),(12,4,4.6)])
#gram.render_to_file('gram.svg')