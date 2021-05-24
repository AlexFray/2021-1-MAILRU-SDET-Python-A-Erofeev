from mysql.models import *
from parser_log.parse_log import *
from base import MySQLBase


class TestCountRequests(MySQLBase):
    count = 1

    def prepare(self, path):
        count_requests(self.mysql_builder, self.count)
        self.mysql.session.commit()

    def test_cr(self):
        line = self.mysql.session.query(CountRequests).all()
        assert len(line) == self.count


class TestCountRequestsType(MySQLBase):
    count = 4

    def prepare(self, path):
        count_requests_type(self.mysql_builder, path)
        self.mysql.session.commit()

    def test_crt(self):
        line = self.mysql.session.query(CountRequestsType).all()
        assert len(line) == self.count


class TestCountTopResource(MySQLBase):
    count = 10

    def prepare(self, path):
        count_top_resource(self.mysql_builder, path, self.count)
        self.mysql.session.commit()

    def test_ctr(self):
        line = self.mysql.session.query(CountTopResources).all()
        assert len(line) == self.count


class TestBigRequestsError(MySQLBase):
    count = 5

    def prepare(self, path):
        big_requests_error(self.mysql_builder, path, self.count)
        self.mysql.session.commit()

    def test_bre(self):
        line = self.mysql.session.query(BigRequestsError).all()
        assert len(line) == self.count


class TestInternalError(MySQLBase):
    count = 5

    def prepare(self, path):
        internal_error(self.mysql_builder, path, self.count)
        self.mysql.session.commit()

    def test_ie(self):
        line = self.mysql.session.query(InternalErrors).all()
        assert len(line) == self.count
