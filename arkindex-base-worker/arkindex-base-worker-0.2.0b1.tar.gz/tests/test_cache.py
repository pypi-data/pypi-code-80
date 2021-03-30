# -*- coding: utf-8 -*-
import os

import pytest
from peewee import OperationalError

from arkindex_worker.cache import create_tables, db, init_cache_db


def test_init_non_existent_path():
    with pytest.raises(OperationalError) as e:
        init_cache_db("path/not/found.sqlite")

    assert str(e.value) == "unable to open database file"


def test_init(tmp_path):
    db_path = f"{tmp_path}/db.sqlite"
    init_cache_db(db_path)

    assert os.path.isfile(db_path)


def test_create_tables_existing_table(tmp_path):
    db_path = f"{tmp_path}/db.sqlite"

    # Create the tables once…
    init_cache_db(db_path)
    create_tables()
    db.close()

    with open(db_path, "rb") as before_file:
        before = before_file.read()

    # Create them again
    init_cache_db(db_path)
    create_tables()

    with open(db_path, "rb") as after_file:
        after = after_file.read()

    assert before == after, "Existing table structure was modified"


def test_create_tables(tmp_path):
    db_path = f"{tmp_path}/db.sqlite"
    init_cache_db(db_path)
    create_tables()

    expected_schema = """CREATE TABLE "elements" ("id" TEXT NOT NULL PRIMARY KEY, "parent_id" TEXT, "type" VARCHAR(50) NOT NULL, "image_id" TEXT, "polygon" text, "initial" INTEGER NOT NULL, "worker_version_id" TEXT, FOREIGN KEY ("image_id") REFERENCES "images" ("id"))
CREATE TABLE "images" ("id" TEXT NOT NULL PRIMARY KEY, "width" INTEGER NOT NULL, "height" INTEGER NOT NULL, "url" TEXT NOT NULL)
CREATE TABLE "transcriptions" ("id" TEXT NOT NULL PRIMARY KEY, "element_id" TEXT NOT NULL, "text" TEXT NOT NULL, "confidence" REAL NOT NULL, "worker_version_id" TEXT NOT NULL, FOREIGN KEY ("element_id") REFERENCES "elements" ("id"))"""

    actual_schema = "\n".join(
        [
            row[0]
            for row in db.connection()
            .execute("SELECT sql FROM sqlite_master WHERE type = 'table' ORDER BY name")
            .fetchall()
        ]
    )

    assert expected_schema == actual_schema
