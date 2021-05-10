import re

from mysql.models import *
from base import MySQLBase


class TestCountRequests(MySQLBase):
    def prepare(self, path):
        count = 0
        with open(path) as file:
            while file.readline():
                count += 1

        self.mysql_builder.create_count_requests(count)

    def test_cr(self):
        line = self.mysql.session.query(CountRequests).all()
        print(line)
        assert len(line) == 1


class TestCountRequestsType(MySQLBase):
    def prepare(self, path):
        with open(path) as file:
            line = file.readline()
            count = {}
            while line:
                if ' "POST ' in line:
                    count['POST'] = count['POST'] + 1 if count.get('POST') else 1
                elif ' "GET ' in line:
                    count['GET'] = count['GET'] + 1 if count.get('GET') else 1
                elif ' "PUT ' in line:
                    count['PUT'] = count['PUT'] + 1 if count.get('PUT') else 1
                elif ' "HEAD ' in line:
                    count['HEAD'] = count['HEAD'] + 1 if count.get('HEAD') else 1
                line = file.readline()

            for key, value in count.items():
                print(key, value)
                self.mysql_builder.create_count_req_type(key, value)

    def test_crt(self):
        line = self.mysql.session.query(CountRequestsType).all()
        print(line)
        assert len(line) == 4


class TestCountTopResource(MySQLBase):
    def prepare(self, path):
        with open(path) as file:
            count = {}
            line = file.readline()
            while line:
                attr = line.split(' ')
                count[f'{attr[6]}'] = count[f'{attr[6]}'] + 1 if count.get(f'{attr[6]}') else 1
                line = file.readline()
            list_count = list(count.items())
            list_count.sort(key=lambda i: i[1])

        for line in list_count[len(list_count) - 10:]:
            self.mysql_builder.create_count_top_res(line[0], line[1])

    def test_ctr(self):
        line = self.mysql.session.query(CountTopResources).all()
        print(line)
        assert len(line) == 10


class TestBigRequestsError(MySQLBase):
    def prepare(self, path):
        results = set()
        with open(path) as file:
            line = file.readline()
            while line:
                attr = line.split(' ')
                if re.search(r'4\d{2}', attr[8]):
                    results.add((attr[6], attr[8], int(attr[9]), attr[0]))
                line = file.readline()
            results = list(results)
            results.sort(key=lambda i: i[2])

        for line in results[len(results) - 5:]:
            self.mysql_builder.create_big_req_error(line[0], line[1], line[2], line[3])

    def test_bre(self):
        line = self.mysql.session.query(BigRequestsError).all()
        print(line)
        assert len(line) == 5


class TestInternalError(MySQLBase):
    def prepare(self, path):
        with open(path) as file:
            result = {}
            line = file.readline()
            while line:
                attr = line.split(' ')
                if re.search(r'5\d{2}', attr[8]):
                    result[f'{attr[0]}'] = result[f'{attr[0]}'] + 1 if result.get(f'{attr[0]}') else 1
                line = file.readline()
            list_count = list(result.items())
            list_count.sort(key=lambda i: i[1])

        for line in list_count[len(list_count) - 5:]:
            self.mysql_builder.create_internal_error(line[0], line[1])

    def test_ie(self):
        line = self.mysql.session.query(InternalErrors).all()
        print(line)
        assert len(line) == 5

