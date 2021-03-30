import pygal

#Line()绘制折线图
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

# stroke参数是指是否禁用连线
def scatter(data=[[1,3],[2,4]],name=['Suluoya'],title='Suluoya',path='scatter-plot'):
    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = title
    for i in name:
        xy_chart.add(i, data)
    xy_chart.render_to_file(path+'.svg')