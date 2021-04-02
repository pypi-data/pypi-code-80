""" Network related functions. 
"""
import os
import sys
import json
import socket

import dofast.utils as df
from dofast.toolkits.telegram import YahooMail
from dofast.logger import Logger
from dofast.config import decode

from .toolkits.telegram import bot_messalert

socket.setdefaulttimeout(30)

logger = Logger('/var/log/phone.log')


def mail2foxmail(subject: str, message: str):
    r = decode('FOXMAIL')
    YahooMail().send(r, subject, message)


def mail2gmail(subject: str, message: str):
    r = decode('GMAIL2')
    YahooMail().send(r, subject, message)


class PapaPhone:
    def __init__(self):
        pass

    def get_headers(self):
        h = {}
        h["Cookie"] = decode('cmcc_cookie')
        h['Authorization'] = decode('cmcc_authorization')
        h["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        h["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        h['device'] = 'iPhone 7'
        h['Referer'] = 'https://h5.ha.chinamobile.com/hnmccClientWap/h5-rest/'
        return h

    def remain_flow(self) -> (float, str):
        try:
            url = 'https://h5.ha.chinamobile.com/h5-rest/flow/data'
            params = {'channel': 2, 'version': '6.4.2'}
            res = df.client.get(url, data=params, headers=self.get_headers())
            json_res = json.loads(res.text)
            flow = float(json_res['data']['flowList'][0]['surplusFlow'])
            unit = json_res['data']['flowList'][0]['surplusFlowUnit']
            logger.info(f'Papa iPhone data flow remain {flow} GB.')
            return flow, unit
        except Exception as e:
            logger.error(f'Get data flow failed: {repr(e)}')
            return -1, 'MB'

    def entry(self, retry: int = 3) -> None:
        receiver = decode('FOXMAIL')
        if retry <= 0:
            YahooMail().send(receiver, '手机余量查询失败', '已经连续重试 3 次，全部失败。')
            return

        flow, unit = self.remain_flow()
        if flow == -1:
            self.entry(retry - 1)
        elif flow < 1 or unit == 'MB':
            # subject = 'Papa手机流量充值提醒 \n'
            message = f'Papa手机流量还剩余 {flow} {unit}，可以充值了。'
            logger.info('\n'.join((receiver, subject, message)))
            bot_messalert(subject + message)


class Network:
    """Network related functions"""
    @classmethod
    def is_good_proxy(cls, proxy: str, proxy_type: str = 'socks5') -> bool:
        """Check whether this proxy is valid or not
        :params proxy: str, e.g. tw.domain.com:12345
        :params type:, str, proxy type, either socks or http(c)
        """
        ctype = 'socks5' if proxy_type == 'socks5' else 'proxy'
        resp = df.shell(f'curl -s -m 3 --{ctype} {proxy} ipinfo.io')
        return resp != ''

    def monitor_proxy(self, proxy_str: str = decode('http_proxy')) -> None:
        local_file = '/tmp/proxy_monitor.json'
        if not os.path.exists(local_file):
            with open(local_file, 'w') as f:
                f.write('{}')
        _info = json.load(open(local_file, 'r'))

        proxy_type = 'https' if proxy_str.startswith('http') else 'socks5'
        if not Network.is_good_proxy(proxy_str, proxy_type):
            failed_count = _info.get(proxy_str, 0) + 1
            if failed_count >= 30:
                msg = str(_info)
                ym = YahooMail()
                ym.send(decode('foxmail'), '代理失效', msg)
                failed_count = -1410  # Check every minute, alert once per day.
            _info[proxy_str] = failed_count
        else:
            _info[proxy_str] = 0

        json.dump(_info, open(local_file, 'w'), indent=2)

    @staticmethod
    def setup_socks5_proxy(port: int = 8888):
        ''' setup a socks5 proxy via SSH '''
        assert os.path.exists(
            '/root/.ssh/id_rsa.pub'), 'ssh pub key not set yet.'
        sshpub = df.textread('/root/.ssh/id_rsa.pub')[0]
        authorized_keys = df.textread('/root/.ssh/authorized_keys')
        if sshpub not in authorized_keys:
            with open('/root/.ssh/authorized_keys', 'a+') as f:
                f.write(sshpub + '\n')

        df.shell(f'ssh -fND 0.0.0.0:{port} localhost &')
        logger.info(f"SSH proxy {port} setup completes.")
