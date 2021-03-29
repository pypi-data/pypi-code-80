import re

from chibi.atlas import Chibi_atlas
from chibi.atlas.multi import Chibi_atlas_multi
from chibi.file import Chibi_file
from chibi.snippet.iter import chunk_each


__all__ = [ 'Chibi_conf' ]


class Chibi_conf( Chibi_file ):
    def read( self ):
        data = super().read()
        result = Chibi_atlas()
        lines = filter( bool, data.split( '\n' ) )
        lines = filter( lambda x: not x.startswith( ';' ), lines )
        for line in lines:
            key_data = line.split( '=', 1 )
            if len( key_data ) == 1:
                key = key_data[0]
                data = ''
            else:
                key, data = key_data
            key= key.strip()
            data = data.strip()
            result[ key ] = data
        return result

    def write( self, data ):
        result = ''
        for k, v in data.items():
            result += f'{k} = {v}\n'
        super().write( result )
