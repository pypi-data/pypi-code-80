
import os
import sys
import logging
import time

from pymongo import MongoClient
from inti.MA.MAMetadata import MACollectionNames


class MABase:
    def __init__(self, ma_dir, db_name, collection_names, sep='\t', buffer_size=1024 * 1024,
                 dburi='mongodb://localhost:27017/', log_file='mabase.log', info_level=logging.DEBUG):
        '''
        Base class to process Macrosoft Academic Graph on MongoDB

        Parameters:
        ma_dir: string
            path to MA directory dataset, with the 3 folders mag/nlp and advanced
        db_name:string
            database name on for MongoDB
        collection_names: list of string
            this is a parameter provided by the child class with the name of the collections for every
            sub folder mag/npl or advanced
        sep: string
            separator for the *.txt files, the default one is '\t'
        buffer_size: int
            parameter that specifies the size of the buffer for every process,
            while the text files are loaded on RAM before insert if on MongoDB
        dburi: string
            database uri for connection
        log_file:string
            file log name
        info_level: logging flag
            the default at the moment is DEBUG
        '''
        self.ma_dir = ma_dir
        self.buffer_size = buffer_size
        self.info_level = info_level
        self.log_file = log_file
        self.logger = logging.getLogger(__name__)
        self.set_info_level(info_level)
        self.db_name = db_name
        self.collection_names = collection_names
        self.sep = sep
        self.dburi = dburi

    def process(self, collection_name, line):
        '''
        To be implemented by children
        '''
        self.logger.error(
            'ERROR: this method is not implemented yet, it cant be use in the base class')
        sys.exit(1)
        return ""

    def resume(self, ma_dir):
        '''
        Show the resume of loaded information on MongoDB
        '''
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        print("=== Resume ")
        for col in MACollectionNames[ma_dir]:
            print("====== {} = {}".format(col, db[col].count_documents({})))
        client.close()

    def checkpoint_get(self):
        '''
        method to get the checkpoint status

        Returns:
            checkpoint: dict
                information about the checkpoint
        '''
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        collection = db["checkpoint"]
        if collection.count_documents({"_id": 0}) == 0:
            self.checkpoint_create()
        checkpoint = collection.find_one({'_id': 0})
        client.close()
        return checkpoint

    def checkpoint_update(self, ma_dir, collection):
        '''
        Method to update the checkpoint for an specific subfolder and collection

        Parameters:
        ma_dir: string
            subfolder on ma, options are (mag,nlp ot advanced)
        collection:
            name of the collection to save the checkpoint, ex: Papers
        '''
        checkpoint = self.checkpoint_get()
        checkpoint[ma_dir][collection] = 1
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        col = db["checkpoint"]
        col.update_one({'_id': 0}, {"$set": checkpoint})
        client.close()

    def checkpoint_create(self, overwrite=False):
        '''
        Method to create the checkpoint collection on MongoDB
        Parameter:
        overwrite:bool
            resets the checkpoint if required
        '''
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        collection = db["checkpoint"]
        if collection.count_documents({"_id": 0}) == 0 or overwrite:
            print("=== Creating CheckPoint")
            collection.drop()
            reg = {'_id': 0}
            for ma_dir in list(MACollectionNames.keys()):
                reg[ma_dir] = {}
                for col in MACollectionNames[ma_dir]:
                    reg[ma_dir][col] = 0
            collection.insert_one(reg)
        client.close()

    def checkpoint_clean_collections(self, ma_dir):
        '''
        method to remove collections partially added,
        if it was correctly added the checkpoint should be correctly added.
        md_dir:string
            subfolder, options are mag,nlp or advanced
        '''
        checkpoint = self.checkpoint_get()
        client = MongoClient(self.dburi)
        db = client[self.db_name]
        del checkpoint['_id']
        for collection in checkpoint[ma_dir]:
            if checkpoint[ma_dir][collection] == 0:
                db[collection].drop()
        client.close()

    def create_index(self, collection_name, index):
        '''
        Method to create index for an specific colletion
        Parameters:
        collection:string
            name of the collection, example Papers
        index: list of tuples
            list of tuples specifying the name of the index an type: ex: [("Doi","text","PaperId",1)]
        '''
        self.client = MongoClient(self.dburi)
        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]
        print('=== Creating index {} = {}'.format(collection_name, index))
        start = time.time()
        self.collection.create_index(index)
        end = time.time()
        hours, rem = divmod(end - start, 3600)
        minutes, seconds = divmod(rem, 60)
        print("====== Index {} {} time ({:0>2}h:{:0>2}m:{:05.2f}s)".format(
            collection_name, index, int(hours), int(minutes), seconds))
        self.client.close()

    def create_indexes(self, max_threads=None):
        '''
        To be implemented by children
        '''
        self.logger.error(
            'ERROR: this method is not implemented yet, it cant be use in the base class')
        sys.exit(1)
        return ""

    def set_info_level(self, info_level):
        '''
        Information level for debug or verbosity of the application (https://docs.python.org/3.1/library/logging.html)
        '''
        if info_level != logging.DEBUG:
            logging.basicConfig(filename=self.log_file, level=info_level)
        self.info_level = info_level

    def process_wrapper(self, file_name, collection_name,
                        chunkStart, chunkSize):
        '''
        Allows to insert the content of the file in the MongoDB

        Parameters:
        file_name:string
            name of the file, ex: ...mag/Papers.txt
        collection_name:string
            name of the collection on MongoDB ex: Papers
        chunkStart:int
            starting point to read the file
        chunkSize:int
            size of the chunk from the starting point
        '''
        self.client = MongoClient(self.dburi)
        self.db = self.client[self.db_name]
        self.collection = self.db[collection_name]

        with open(file_name, 'rb') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).decode('utf-8').split('\r\n')
            processed_lines = []
            for line in lines:
                line = self.process(collection_name, line)
                if line is not None:
                    processed_lines.append(line)
            if len(processed_lines) > 0:
                self.collection.insert_many(processed_lines, ordered=False)
        self.client.close()

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
        fileEnd = os.path.getsize(file_name)
        with open(file_name, 'rb') as f:
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
        To be implemented by children
        '''
        self.logger.error(
            'ERROR: this method is not implemented yet, it cant be use in the base class')
        sys.exit(1)
        return ""
