from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['USERDB']}:{os.environ['PASSWORDDB']}@{os.environ['HOST']}/{os.environ['DBNAME']}"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

class Config():
    """ Represents an abstract class that will be used to another models."""

    def create_database(self):
        Base.metadata.create_all(engine)
