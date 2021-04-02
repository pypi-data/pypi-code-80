''' crontab tasks '''
import json
import os
import requests

from bs4 import BeautifulSoup
from .toolkits.telegram import bot_messalert
from .network import PapaPhone


def alltasks():
    pass


def papa_phone_dataflow():
    value, unit = PapaPhone().remain_flow()
    msg = f'papa cellphone data flow {value} {unit}'
    bot_messalert('日常流量提醒\n' + msg)


class HappyXiao:
    @staticmethod
    def rss(url: str = 'https://happyxiao.com/') -> None:
        rsp = BeautifulSoup(requests.get(url).text, 'lxml')
        more = rsp.find_all('a', attrs={'class': 'more-link'})
        articles = {m.attrs['href']: '' for m in more}
        jsonfile = 'hx.json'

        if not os.path.exists(jsonfile):
            open(jsonfile, 'w').write('{}')

        j = json.load(open(jsonfile, 'r'))
        res = '\n'.join(
            HappyXiao.brief(k) for k in articles.keys() if k not in j)
        j.update(articles)
        json.dump(j, open(jsonfile, 'w'), indent=2)
        if res:
            bot_messalert(res.replace('#', '%23'))

    @staticmethod
    def brief(url) -> str:
        rsp = BeautifulSoup(requests.get(url).text, 'lxml')
        art = rsp.find('article')
        res = url + '\n' + art.text.replace('\t', '') + str(art.a)
        return res
