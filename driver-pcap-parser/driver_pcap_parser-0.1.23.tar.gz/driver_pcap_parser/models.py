class DataOut(object):
    def __init__(self, terminal_serial,
                 terminal_client_id=None,
                 terminal_type=None,
                 src_ip=None, dst_ip=None,
                 tcp_sport=None, tcp_dport=None,
                 src_mac=None, dst_mac=None,
                 pkt_time=None):
        self.terminal_serial = terminal_serial
        self.terminal_client_id = terminal_client_id
        self.terminal_type = terminal_type
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.tcp_sport = tcp_sport
        self.tcp_dport = tcp_dport
        self.src_mac = src_mac
        self.dst_mac = dst_mac
        self.pkt_time = pkt_time

    def __dict__(self):
        return dict(terminal_serial=self.terminal_serial,
                    terminal_client_id=self.terminal_client_id,
                    terminal_type=self.terminal_type,
                    src_ip=self.src_ip,
                    dst_ip=self.dst_ip,
                    tcp_sport=self.tcp_sport,
                    tcp_dport=self.tcp_dport,
                    src_mac=self.src_mac,
                    dst_mac=self.dst_mac,
                    pkt_time=self.pkt_time
                    )

    def __repr__(self):
        return str(self.__dict__())
