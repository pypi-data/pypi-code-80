from inti.MA.MAMetadata import MAColTypes, MAColumnNames, MACollectionNames
from inti.MA.MABase import MABase
from inti.MA.MAExecutor import MAExecutor
from joblib import Parallel, delayed
import logging
import psutil
import bson
import time


class MAAdvanced(MABase):
    def __init__(self, ma_dir, database_name, sep='\t', buffer_size=1024 * 1024, dburi='mongodb://localhost:27017/',
                 log_file='maadvancedbase.log', info_level=logging.DEBUG):
        """
        Class to parse advanced subsolder on Microsoft Academic dataset.

        The directory should have the next files
        advanced/EntityRelatedEntities.txt
        advanced/FieldOfStudyChildren.txt
        advanced/FieldOfStudyExtendedAttributes.txt
        advanced/FieldsOfStudy.txt
        advanced/PaperFieldsOfStudy.txt
        advanced/PaperRecommendations.txt
        advanced/RelatedFieldOfStudy.txt

        Parameters:
        ma_dir: string
            path to MA directory dataset, with the 3 folders mag/nlp and advanced
        db_name:string
            database name on for MongoDB
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
        """
        super().__init__(ma_dir, database_name, MACollectionNames["advanced"], sep, buffer_size, dburi,
                         log_file, info_level)

    def process(self, collection_name, line):
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
        col_names = MAColumnNames["advanced"][collection_name]
        if isinstance(line, type(bytes())):
            line = line.decode('utf-8')
        fields = line.split(self.sep)
        if len(fields) == len(col_names):
            for index in range(len(col_names)):
                col_name = col_names[index]
                if col_name in MAColTypes["advanced"]["long"]:
                    value = fields[index].strip()
                    if value == "":
                        value = 0
                    try:
                        register[col_name] = bson.int64.Int64(value)
                    except BaseException:
                        print("VALUE = ", value, collection_name)
                elif col_name == "Rank" and collection_name == "RelatedFieldOfStudy":  # the only exception
                    if value == "":
                        value = 0.0
                    register[col_name] = float(value)
                elif col_name in MAColTypes["advanced"]["int"]:
                    if value == "":
                        value = 0
                    register[col_name] = bson.int64.Int64(value)
                elif col_name in MAColTypes["advanced"]["float"]:
                    if value == "":
                        value = 0.0
                    register[col_name] = float(value)
                else:
                    register[col_names[index]] = fields[index]

            return register
        else:
            pass

    def create_indexes(self, max_threads=None):
        '''
        Method to create indexes in parallel.
        '''
        indexes = {}
        for collection_name in self.collection_names:
            indexes[collection_name] = []
            col_indexes = MAColumnNames["advanced"]['{}_indexes'.format(
                collection_name)]
            for index in col_indexes:
                indexes[collection_name].append(index)
        if max_threads is None:
            jobs = psutil.cpu_count()
        else:
            jobs = max_threads
        Parallel(
            n_jobs=jobs)(
            delayed(
                self.create_index)(
                collection_name,
                index) for collection_name,
            index in indexes.items())

    def run(self, max_threads=None):
        """
        Checkpoint supported!
        """
        checkpoint = self.checkpoint_get()
        collections = []
        for col in checkpoint["advanced"]:
            if checkpoint["advanced"][col] == 0:
                collections.append(col)
        self.checkpoint_clean_collections("advanced")

        for collection in collections:
            advanced_file = self.ma_dir + 'advanced/{}.txt'.format(collection)
            print("=== Loading " + advanced_file)
            start = time.time()
            MAExecutor(
                self,
                advanced_file,
                collection,
                max_threads=max_threads)
            end = time.time()
            hours, rem = divmod(end - start, 3600)
            minutes, seconds = divmod(rem, 60)
            print(
                "=== {:0>2}h:{:0>2}m:{:05.2f}s".format(
                    int(hours),
                    int(minutes),
                    seconds))
            print("=== Updating Ckp " + advanced_file)
            self.checkpoint_update("advanced", collection)
        self.resume("advanced")
