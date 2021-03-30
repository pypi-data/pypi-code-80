


from kraken_record.kraken_record import Kraken_record as KR

from kraken_db.kraken_db import Kraken_db as DB

from kraken_cache.kraken_cache import Kraken_cache as CACHE

#from kraken_datatype.kraken_datatype import Kraken_datatype as DATATYPE

import json

# Initialize cache
cache = CACHE()

# Initialize db
db = DB()


class Kraken:

    def __init__(self):

        a = 1


    def get(self, record_type, record_id):
        
        
        return self._get(record_type, record_id)


    def search(self, record_type, search_terms):
        record = {}

        return record


    def post(self, record_type, record_id, record): 

        return self._post(record_type, record_id, record)

    
    def ingest(self, datasource_id, records):
        # Convert record based on predefined mapping and store in krkn


        # Retrieve mapping



        # Convert record


        # Post record
        self._post(None, None, records)



        return 


    def _get(self, record_type, record_id):

        if not record_type or not record_id:
            return None


        # Retrieve record from cache
        cache_id = record_type + '/' + record_id
        record = cache.get(cache_id)


        # If not in cache, Retrieve record from db
        if not record:
            path = record_type + '/' + record_id
            record = db.get(path)

        # Remove db data
        if record:
            record.pop('createdDate', None)
            record.pop('@id', None)


        # Convert krkn record to json record
        if record:
            kr = KR()
            kr.load(record)
        else:
            kr = None

        # Set to null of no id
        if not kr or not kr.record_id:
            kr = None


        return kr


    def _post(self, record_type, record_id, records):

        # Convert to list if not one
        if not isinstance(records, list):
            records = [records]



        # Process record and store result in cache
        for record in records:
            self._post_process_record(record_type, record_id, record)

        # Save cache content to db
        records = cache.export()
        for record in records:
            db_path = record.get('kraken:record_type', None) + '/' + record.get('kraken:record_id', None)
            db.post(db_path, record)

        #Reset all cache data (after save to db)
        cache.clear_all()


        # Save cache content as json files in krkn files


        return


    def _post_process_record(self, record_type, record_id, record):

        # Check if record is valid


        # Retrieve type schema
        schema = {}


        # Validate and standardize record keys


        # validate and standardize record values
        #dt = DATATYPE()
        #record = dt.clean(record, schema)


        # Transform record into krkn format and flatten
        if not isinstance(record, KR):
            kr_new_record = KR()
            kr_new_record.set(record)
        else:
            kr_new_record = record

        # Override record type and id if one was provided
        if record_type:
            kr_new_record.record_type = record_type
        if record_id:
            kr_new_record.record_id = record_id

        # Reassign recordtype and id
        record_type = kr_new_record.record_type
        record_id = kr_new_record.record_id


        # Retrieve sub_records (from flattening)
        sub_records = kr_new_record.sub_records


        # Process sub records
        for sub_record in sub_records:
            print('a', sub_record.get())
            self._post_process_record(None, None, sub_record)


        # Retrieve record from cache/db
        kr_db_record = self._get(record_type, record_id)  
        

        # Merge records (new and old) 
        if kr_db_record:
            merged_record = kr_new_record + kr_db_record
        else:
            merged_record = kr_new_record

        # If record changed, save to cache
        if kr_db_record == None or merged_record > kr_db_record:
            cache_id = record_type + '/' + record_id
            cache.set(cache_id, merged_record.dump())


        return record_id

