from chibi_hybrid.chibi_hybrid import Chibi_hybrid
from chibi_command import Command_result
from chibi.net.network.interface import Network

from chibi_command import Command


class Interface_result( Command_result ):
    def parse_result( self ):
        self.result = Network.load_from_string( self.result )


class Ip( Command ):
    command = 'ip'
    captive = True
    result_class=Interface_result

    @Chibi_hybrid
    def addr( cls ):
        return cls( 'addr' )

    @addr.instancemethod
    def addr( self ):
        self.add_args( 'addr' )
        return self
