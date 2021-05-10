from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class CountRequests(Base):
    __tablename__ = 'count_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<count_requests(" \
               f"id='{self.id}'," \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    count = Column(Integer, nullable=True)


class CountRequestsType(Base):
    __tablename__ = 'count_requests_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<count_requests_type(" \
               f"id='{self.id}'," \
               f"type='{self.type}', " \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=True)
    count = Column(Integer, nullable=True)


class CountTopResources(Base):
    __tablename__ = 'count_top_resources'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<count_top_resources(" \
               f"id='{self.id}'," \
               f"path='{self.path}', " \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(200), nullable=True)
    count = Column(Integer, nullable=True)


class InternalErrors(Base):
    __tablename__ = 'internal_errors'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<internal_errors(" \
               f"id='{self.id}'," \
               f"ip='{self.ip}', " \
               f"count='{self.count}', " \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20), nullable=True)
    count = Column(Integer, nullable=True)


class BigRequestsError(Base):
    __tablename__ = 'big_requests_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<internal_errors(" \
               f"id='{self.id}'," \
               f"path='{self.path}', " \
               f"code='{self.code}', " \
               f"size='{self.size}', " \
               f"ip='{self.ip}'" \
               f")>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(500), nullable=True)
    code = Column(Integer, nullable=True)
    size = Column(Integer, nullable=True)
    ip = Column(String(20), nullable=True)
