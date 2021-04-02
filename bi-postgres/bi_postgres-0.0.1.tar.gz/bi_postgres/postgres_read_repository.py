import sqlalchemy
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from bi_postgres.errors.session_failed_error import SessionFailedError


class PostgresReadRepository():
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
        try:
            Session = sessionmaker(bind=self.__engine, autoflush=False, autocommit=False)
            self.__session = Session()
            yield self.__session
        except Exception:
            raise SessionFailedError()
        finally:
            self.__session.close()

    def select_one(self, model, filters: dict):
        with self.session() as db:
            rows = db.query(model).filter_by(**filters).first()
            return rows

    def select_all(self, model, filters: dict):
        with self.session() as db:
            rows = db.query(model).filter_by(**filters).all()
            return rows

    def execute(self, query: str):
        with self.session() as db:
            results = db.execute(query)
            return [{column: value for column, value in row.items()} for row in results]
