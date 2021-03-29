"""Top-level package for Driver PCAP parser."""

__author__ = """Andres Kepler"""
__email__ = 'andres.kepler@fleetcomplete.com'
__version__ = '0.1.24'

import datetime
import logstash
from scapy.all import *
from logstash_formatter import LogstashFormatterV1

from driver_pcap_parser.models import DataOut
from driver_pcap_parser import parsers
from driver_pcap_parser.parsers import get_json_serial, get_m7_serial, get_vt10_serial, get_ruptela_serial, \
    get_teltonika_serial

# configure logging
logging.basicConfig(level=logging.INFO)


def logsstash_logging(args):
    logsstash_host, logsstash_port = args.logstash.split(":")
    logsstash_logger = logging.getLogger()
    logsstash_logger.addHandler(logstash.LogstashHandler(logsstash_host,
                                                         int(logsstash_port),
                                                         version=1,
                                                         message_type="driver-parser"))


def packet_summary(packet):
    ip_src = None
    ip_dst = None
    tcp_sport = None
    tcp_dport = None
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
    if TCP in packet:
        tcp_sport = packet[TCP].sport
        tcp_dport = packet[TCP].dport
    return ip_src, ip_dst, tcp_sport, tcp_dport, packet.src, packet.dst, datetime.fromtimestamp(packet.time).isoformat()


def parse_file(args):
    if args.logstash:
        logsstash_logging(args)
    else:
        logsstash_logger = logging.getLogger()
        std_handler = logging.StreamHandler(stream=sys.stdout)
        std_handler.setFormatter(LogstashFormatterV1())
        logsstash_logger.addHandler(std_handler)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    serial_collector = []
    packets = rdpcap(args.filename)
    myip = args.filter_dst_ip
    if myip:
        packets = packets.filter(lambda x: x.payload.dst == myip)
    logging.debug("Start")
    # Let's iterate through every filtered packet
    for packet in packets:
        terminal_serial = ""
        terminal_client_id = None
        terminal_type = None
        packet_summ = packet_summary(packet)

        for parser_f in dir(parsers):
            parser_match = re.match("get_(.*)_serial", parser_f)
            if parser_match:
                parser_f = f"parsers.{parser_match.group(0)}(packet)"
                detector = eval(parser_f)
                _terminal_type = detector.get("terminal_type")
                _terminal_serial = detector.get("terminal_serial")
                if _terminal_serial and _terminal_type:
                    terminal_type = _terminal_type
                    terminal_serial = _terminal_serial
                    terminal_client_id = detector.get("terminal_client_id")
        if not re.match("\d{15}", terminal_serial) and \
            not (re.match("\d{7}", terminal_serial) and terminal_type == "Cellocator") and \
            not (re.match("\d{11}", terminal_serial) and terminal_type == "Bronco"):
            continue

        payload = DataOut(terminal_serial,
                          terminal_client_id,
                          terminal_type,
                          *packet_summ
                          )
        if terminal_serial not in serial_collector:
            serial_collector.append(terminal_serial)
            logging.info({"terminal_serial": payload.terminal_serial, "terminal_type": payload.terminal_type},
                         extra=payload.__dict__())
    logging.debug("Stop")
    return 0
