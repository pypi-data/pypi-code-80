from dofast.simple_parser import SimpleParser
from .network import Network, PapaPhone
from .linuxtools import LinuxTools

msg = """VPS toolkits 😏
-m(--monitor) ip:port ::: Monitor ip:port proxy
-ma(--messalert) message ::: Bot MessAlert. 
-k(--kill) process ::: Kill linux process.
-p(--phone) ::: Papa phone monitor.
-socks [port] ::: Set up a socks5 proxy.

-flow(--dataflow)::: papa cellphone dataflow monitor.
-hx(--happyxiao) ::: HappyXiao briefing newsletter.
"""


def parse_arguments():
    sp = SimpleParser()
    sp.add_argument('-m', '--monitor')
    sp.add_argument('-k', '--kill')
    sp.add_argument('-p', '--phone')
    sp.add_argument('-socks', '--socks')
    sp.add_argument('-flow', '--dataflow')
    sp.add_argument('-hx', '--happyxiao')
    sp.parse_args()

    if sp.monitor:
        Network().monitor_proxy(sp.monitor.value)

    elif sp.kill:
        LinuxTools().pskill(sp.kill.value)

    elif sp.phone:
        PapaPhone().entry()

    elif sp.socks:
        port = sp.socks.value
        if port == 'PLACEHOLDER': port = 8888
        Network.setup_socks5_proxy(port)

    elif sp.dataflow:
        from .crontab import papa_phone_dataflow
        papa_phone_dataflow()

    elif sp.happyxiao:
        from .crontab import HappyXiao
        HappyXiao.rss()

    else:
        for l in msg.split("\n"):
            c, e = (l + " ::: ").split(':::')[:2]
            print("{:<70} {:<20}".format(c, e))
