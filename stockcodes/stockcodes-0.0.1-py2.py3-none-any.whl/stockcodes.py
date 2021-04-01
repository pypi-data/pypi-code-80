##author:jopil
##email: jopil@163.com

##being maintained solo by jopil 
##npm twin: stockcodes

import requests
import pandas as pd
import random
import warnings

warnings.filterwarnings('ignore')

def getCodeList():
    headerdata={
        'Referer':'http://www.sse.com.cn/assortment/stock/list/share/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    ##沪市主板
    url="http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=1"
    r=requests.session()
    r.get('http://www.sse.com.cn/assortment/stock/list/share/')
    b=r.get(url,headers=headerdata)
    s=b.text
    l=s.split('\n')
    dd=list(map(lambda x:[s.strip() for s in x],[k.strip().split('\t') for k in l]))
    SHZBdata=pd.DataFrame(dd[1:-1],columns=dd[0])[['代码','简称']]
    SHZBdata['所属板块']='沪市主板'
    ##沪市科创
    url="http://query.sse.com.cn/security/stock/downloadStockListFile.do?csrcCode=&stockCode=&areaName=&stockType=8"
    b=r.get(url,headers=headerdata)
    s=b.text
    l=s.split('\n')
    dd=list(map(lambda x:[s.strip() for s in x],[k.strip().split('\t') for k in l]))
    KCdata=pd.DataFrame(dd[1:-1],columns=dd[0])[['代码','简称']]
    KCdata['所属板块']='科创板'
    #深交所(主板、中小、创业板)
    url=f'http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110x&TABKEY=tab1&random={random.random()}'
    SZdata=pd.read_excel(url)
    SZdata['公司代码']=SZdata['公司代码'].map(lambda x:str(x).zfill(6))
    SZdata = SZdata[['公司代码','公司简称']]
    SZdata.rename(columns={'公司代码':'代码','公司简称':'简称'}, inplace=True)
    SZdata['所属板块']=SZdata['代码'].map(lambda x: '深市主板' if x[0:3]=='000' else '创业板' if x[0:2]=='30' else '科创板')
    #合并返回
    return SHZBdata.append(KCdata,ignore_index=True).append(SZdata,ignore_index=True)