# -*- coding: utf-8 -*-
import json
import logging
import os
import sqlite3

from peewee import (
    BooleanField,
    CharField,
    Field,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    UUIDField,
)

logger = logging.getLogger(__name__)

db = SqliteDatabase(None)


class JSONField(Field):
    field_type = "text"

    def db_value(self, value):
        if value is None:
            return
        return json.dumps(value)

    def python_value(self, value):
        if value is None:
            return
        return json.loads(value)


class CachedImage(Model):
    id = UUIDField(primary_key=True)
    width = IntegerField()
    height = IntegerField()
    url = TextField()

    class Meta:
        database = db
        table_name = "images"


class CachedElement(Model):
    id = UUIDField(primary_key=True)
    parent_id = UUIDField(null=True)
    type = CharField(max_length=50)
    image_id = ForeignKeyField(CachedImage, backref="elements", null=True)
    polygon = JSONField(null=True)
    initial = BooleanField(default=False)
    worker_version_id = UUIDField(null=True)

    class Meta:
        database = db
        table_name = "elements"


class CachedTranscription(Model):
    id = UUIDField(primary_key=True)
    element_id = ForeignKeyField(CachedElement, backref="transcriptions")
    text = TextField()
    confidence = FloatField()
    worker_version_id = UUIDField()

    class Meta:
        database = db
        table_name = "transcriptions"


# Add all the managed models in that list
# It's used here, but also in unit tests
MODELS = [CachedImage, CachedElement, CachedTranscription]


def init_cache_db(path):
    db.init(
        path,
        pragmas={
            # SQLite ignores foreign keys and check constraints by default!
            "foreign_keys": 1,
            "ignore_check_constraints": 0,
        },
    )
    db.connect()
    logger.info(f"Connected to cache on {path}")


def create_tables():
    """
    Creates the tables in the cache DB only if they do not already exist.
    """
    db.create_tables(MODELS)


def merge_parents_cache(parent_ids, current_database, data_dir="/data", chunk=None):
    """
    Merge all the potential parent task's databases into the existing local one
    """
    assert isinstance(parent_ids, list)
    assert os.path.isdir(data_dir)
    assert os.path.exists(current_database)

    # Handle possible chunk in parent task name
    # This is needed to support the init_elements databases
    filenames = [
        "db.sqlite",
    ]
    if chunk is not None:
        filenames.append(f"db_{chunk}.sqlite")

    # Find all the paths for these databases
    paths = list(
        filter(
            lambda p: os.path.isfile(p),
            [
                os.path.join(data_dir, parent, name)
                for parent in parent_ids
                for name in filenames
            ],
        )
    )

    if not paths:
        logger.info("No parents cache to use")
        return

    # Open a connection on current database
    connection = sqlite3.connect(current_database)
    cursor = connection.cursor()

    # Merge each table into the local database
    for idx, path in enumerate(paths):
        logger.info(f"Merging parent db {path} into {current_database}")
        statements = [
            "PRAGMA page_size=80000;",
            "PRAGMA synchronous=OFF;",
            f"ATTACH DATABASE '{path}' AS source_{idx};",
            f"REPLACE INTO elements SELECT * FROM source_{idx}.elements;",
            f"REPLACE INTO transcriptions SELECT * FROM source_{idx}.transcriptions;",
        ]

        for statement in statements:
            cursor.execute(statement)
        connection.commit()
