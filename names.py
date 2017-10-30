import pandas as pd
import matplotlib.pylab as plt
import numpy as np


names1880=pd.read_csv('names/yob1880.txt',names=['name','sex','births'])
print(names1880)
print(names1880.groupby('sex').births.sum())

##定义各个函数备用
def add_prop(group):
    #births=group.births.astype(float)
    group['prop']=group.births/group.births.sum()
    return group

def get_top1000(group):
    return group.sort_values(by='births',ascending=False)[:1000]

def get_quantile_count(group,q=0.5):
    group=group.sort_values(by='prop',ascending=False)
    return (group.prop.cumsum().searchsorted(q)+1)[0]

get_last_letter=lambda x:x[-1]

years=range(1880,2011)
pieces=[]
columns=['name','sex','births']
for year in years:
    path='names/yob%d.txt'%year
    frame=pd.read_csv(path,names=columns)
    frame['year']=year
    pieces.append(frame)


names=pd.concat(pieces,ignore_index=True)##将各个文件数据整合在一起)
total_births=names.pivot_table('births',index='year',columns='sex',aggfunc=sum)
total_births.plot(title='Total births by sex and year')
plt.show()##图2-4：按性别和年度统计的总出生数


names=names.groupby(['year','sex']).apply(add_prop)##基于year和sex进行分块
top1000=names.groupby(['year','sex']).apply(get_top1000)
boys=top1000[top1000.sex=='M']
girls=top1000[top1000.sex=='F']
#print(girls)
total_births=top1000.pivot_table(values='births',index=['year'],columns='name',
                                 aggfunc=sum)
total_births[['John','Harry','Mary','Marilyn']].plot(subplots=True,figsize=(12,10),
                                                     grid=False,title='Number of births per year')
plt.subplots_adjust(wspace=0,hspace=0.6)####用于调整多个字图之间的距离，防止重叠，wspace为宽度方向，hspace为垂直方向
plt.show()##图2-5：几个男孩女孩名字随时间变化的使用量



table=top1000.pivot_table('prop',index=['year'],columns='sex',aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0,1.2,13),xticks=range(1880,2020,10))
plt.show()##图2-6：分性别统计的前1000个名字在总出生人数中的比例


diversity=top1000.groupby(['year','sex']).apply(get_quantile_count)
diversity=diversity.unstack('sex')
diversity.plot(title='Number of popular names in top50%')
plt.show()##图2-7：按年度统计的密度表


last_letters=names.name.map(get_last_letter)
table=names.pivot_table('births',index=last_letters,columns=['sex','year'],
                        aggfunc=sum)
subtable=table.reindex(columns=[1910,1960,2010],level='year')
letter_prop=subtable/subtable.sum()
fig,axes=plt.subplots(2,1,figsize=(10,8))
plt.subplots_adjust(wspace =0,hspace=0.6)##用于调整多个字图之间的距离，防止重叠，wspace为宽度方向，hspace为垂直方向
letter_prop['M'].plot(kind='bar',rot=0,ax=axes[0],title='Male')
letter_prop['F'].plot(kind='bar',rot=0,ax=axes[1],title='Female',legend=False)
plt.show()##图2-8：男孩女孩名字中各个末字母的比例

letter_prop=table/table.sum()
dny_ts=letter_prop.ix[['d','n','y'],'M'].T
dny_ts.plot()
plt.show()##图2-9：各年出生的男孩名字以d/n/y结尾的人数比例

##unique
all_names=top1000.name.unique()##['Mary' 'Anna' 'Emma' ..., 'Yousef' 'Joziah' 'Maxton']
print(all_names)
mask=np.array(['lesl' in x.lower() for x in all_names])##输出[False False False ..., False False False]
print(mask)
lesley_like=all_names[mask]##输出['Leslie' 'Lesley' 'Leslee' 'Lesli' 'Lesly']
print(lesley_like)

filterd=top1000[top1000.name.isin(lesley_like)]
filterd.groupby('name').births.sum()
table=filterd.pivot_table('births',index='year',columns='sex',aggfunc=sum)
print(table)
print('----------')
print(table.sum())
print('----------')
print(table.sum(1))
table=table.div(table.sum(1),axis=0)
print(table)
table.plot(style={'M':'k-','F':'k--'})
plt.show()##图2-10：各年度使用‘Lesley型’名字的男女比例