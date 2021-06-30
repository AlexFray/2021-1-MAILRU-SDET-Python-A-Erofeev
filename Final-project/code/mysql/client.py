import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from mysql.models import Base


class MySQLClient:

    def __init__(self, host, port: int, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self):
        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}',
            encoding='utf8'
        )
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine,
                                    autocommit=False,  # use autocommit on session.add
                                    expire_on_commit=False  # expire model after commit (requests data from database)
                                    )()
