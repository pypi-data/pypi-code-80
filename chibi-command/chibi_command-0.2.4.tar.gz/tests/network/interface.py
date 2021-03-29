from unittest import TestCase

from chibi_command.network.interfaces import Ip


class Test_ip_commnad( TestCase ):
    def test_addr_should_work( self ):
        c = Ip.addr()
        preview = c.preview()
        self.assertEqual( preview, 'ip addr' )
