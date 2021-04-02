import sqlalchemy
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from bi_postgres.errors.session_not_initialized_error import SessionNotInitializedError


class PostgresWriteRepository():
    def __init__(self, connection_params: dict):
        connection_string = URL(
            drivername='postgres',
            username=connection_params.get('username'),
            password=connection_params.get('password'),
            host=connection_params.get('host'),
            port=int(connection_params.get('port')),
            database=connection_params.get('database')
        )

        self.__engine = sqlalchemy.create_engine(connection_string)
        self.__session = None

    @contextmanager
    def session(self):
        self.__validate_session()
        yield self.__session
        self.__session.flush()

    def start_transaction(self):
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine, autoflush=True, autocommit=False)
            self.__session = Session()

    def commit(self):
        self.__validate_session()
        self.__session.commit()
        self.__session.close()
        self.__session = None

    def rollback(self):
        self.__validate_session()
        self.__session.rollback()

    def insert(self, row):
        with self.session() as db:
            db.add(row)

    def bulk_insert(self, rows):
        with self.session() as db:
            for row in rows:
                db.add(row)

    def update(self, model, filters, properties):
        with self.session() as db:
            row = db.query(model).filter_by(**filters).first()

            for key, value in properties.items():
                setattr(row, key, value)

    def bulk_update(self, model, filters, properties):
        with self.session() as db:
            rows = db.query(model).filter_by(**filters).all()

            for row in rows:
                for (key, value) in properties.items():
                    setattr(row, key, value)

    def delete(self, model, filters):
        with self.session() as db:
            db.query(model).filter_by(**filters).first().delete()

    def bulk_delete(self, model, filters):
        with self.session() as db:
            db.query(model).filter_by(**filters).all().delete()

    def execute(self, query: str):
        with self.session() as db:
            db.execute(query)

    def __validate_session(self):
        if self.__session is None:
            raise SessionNotInitializedError()
