"""Telegram bot"""
import json
import requests
import dofast.utils as du

from dofast.config import decode

proxies = {'https': decode('http_proxy')}


def bot_say(api_token: str, text: str, bot_name: str = 'PlutoShare'):
    url = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id=@{bot_name}&text={text}"
    requests.get(url, proxies=proxies)


def bot_messalert(msg: str) -> None:
    bot_say(decode('mess_alert'), msg, bot_name='messalert')


def read_hema_bot():
    bot_updates = decode('pluto_share')
    resp = du.client.get(bot_updates, proxies=proxies)
    print(json.loads(resp.text))


def download_file_by_id(file_id: str) -> None:
    bot_updates = decode('pluto_share')
    file_url = bot_updates.replace('getUpdates', f'getFile?file_id={file_id}')
    json_res = du.client.get(file_url, proxies=proxies).text
    file_name = json.loads(json_res)['result']['file_path']

    file_url = bot_updates.replace('getUpdates',
                                   file_name).replace('/bot', '/file/bot')
    du.download(file_url, proxy=proxies)
