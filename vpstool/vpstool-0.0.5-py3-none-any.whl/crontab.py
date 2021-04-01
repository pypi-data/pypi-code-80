''' crontab tasks '''
from dofast.toolkits.telegram import YahooMail
from .network import PapaPhone, mail2gmail


def alltasks():
    pass


def papa_phone_dataflow():
    value, unit = PapaPhone().remain_flow()
    msg = f'papa cellphone data flow {value} {unit}'
    mail2gmail(subject='日常流量提醒', message=msg)
