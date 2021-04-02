import os
import logging

from elasticsearch import Elasticsearch, helpers

from inti.MA.MAExecutor import MAExecutor

from inti.MA.MAMetadata import MAColumnNames


class MAESLoader:
    def __init__(self, file_name, index_name, field_name, col_names, sep='\t', buffer_size=1024 * 1024,
                 db_ip='127.0.0.1', db_port=9200, timeout=120, log_file='maesbase.log', info_level=logging.DEBUG):
        '''
        Class to load a field from a Microsoft Academic file on Elastic Search database,

        Parameter:
            file_name: string
                name of the file to load, ex: .../mag/Papers.txt
            index_name:string
                database name (index) on for Elastic Search
            filed_name: string
                Name of the field for the index, ex: PaperTitle
            col_names: dict
                name of the columns for the given file.
                Object provide for Inti.MA.Metadata.MAColumnNames
            sep: string
                separator for the *.txt files, the default one is '\t'
            buffer_size: int
                parameter that specifies the size of the buffer for every process,
                while the text files are loaded on RAM before insert if on MongoDB
            db_ip: string
                database ip for connection to Elastic Search
            db_port: int
                database port for connection to Elastic Search
            timeout: int
                timeout for persistent connection to Elastic Search
            log_file:string
                file log name
            info_level: logging flag
                the default at the moment is DEBUG
        '''
        self.file_name = file_name
        self.buffer_size = buffer_size
        self.info_level = info_level
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.set_info_level(info_level)
        self.sep = sep
        self.db_ip = db_ip
        self.db_port = db_port
        self.timeout = timeout
        self.col_names = col_names
        self.field_name = field_name
        self.index_name = index_name

    def process(self, line):
        '''
        Process the line, adding the metadata to create a dictionary

        Parameters:
            line:string
                line from the MA file with the data values.
        Returns:
            register:dict
                dictionary with the information on  the metadata and values.
        '''
        register = {}
        if isinstance(line, type(bytes())):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        if len(fields) == len(self.col_names):
            for index in range(len(self.col_names)):
                col_name = self.col_names[index]
                register[col_name] = fields[index]

            return register
        else:
            # TODO:Error here
            pass

    def set_info_level(self, info_level):
        '''
        Information level for debug or verbosity of the application (https://docs.python.org/3.1/library/logging.html)
        '''
        if info_level != logging.DEBUG:
            logging.basicConfig(filename=self.log_file, level=info_level)
        self.info_level = info_level

    def process_wrapper(self, file_name, index_name, chunkStart, chunkSize):
        '''
        Allows to insert the content of the file in the Elastic Search

        Parameters:
        file_name:string
            name of the file, ex: ...mag/Papers.txt
        index_name:string
            name of the database(index) on Elastic Search ex: MAG
        chunkStart:int
            starting point to read the file
        chunkSize:int
            size of the chunk from the starting point
        '''
        es = Elasticsearch(
            HOST=self.db_ip,
            PORT=self.db_port,
            timeout=self.timeout)

        with open(self.file_name, 'rb') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).decode('utf-8').split('\r\n')
            processed_lines = []
            for line in lines:
                line = self.process(line)
                if line is not None:
                    entry = {"_index": self.index_name,
                             "_id": str(line['PaperId']),
                             "_source": {self.field_name: line[self.field_name]}}
                    processed_lines.append(entry)
        try:
            helpers.bulk(
                es,
                processed_lines,
                refresh=True,
                request_timeout=self.timeout)
        except Exception as e:
            # This can happen if the server is restarted or the connection
            # becomes unavilable
            print(str(e))

    def chunkify(self, file_name):
        '''
        Allows to split the file chunks, according to the buffer_size provided in the constructor

        Parameter:
            file_name: string
                filename to be splitted ex: ../mag/Papers.txt
        Returns:
            chunkStart: int
                starting point to read the file
            checkSize: int
                size of the buffer from the starting point.
                this is because we need to be sure we are reading the whole line until end of line.
        '''
        fileEnd = os.path.getsize(self.file_name)
        with open(self.file_name, 'rb') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(self.buffer_size, 1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break

    def run(self, max_threads=None):
        '''
        Calls the executor to run in parallel.
        '''
        MAExecutor(
            self,
            self.field_name,
            self.index_name,
            max_threads=max_threads)


def run(mag_dir, col_name, index_name, field_name, sep='\t', buffer_size=1024 * 1024,
        db_ip='127.0.0.1', db_port=9200, timeout=120, max_threads=None):
    '''
    Calls the executor to run in parallel.
    '''
    mag_file = mag_dir + '/{}.txt'.format(col_name)
    col_names = MAColumnNames["mag"][col_name]

    instance = MAESLoader(
        mag_file,
        index_name,
        field_name,
        col_names,
        sep,
        buffer_size,
        db_ip,
        db_port,
        timeout)
    instance.run(max_threads=max_threads)
