from mysql.builder import MySQLBuilder
import pytest


class MySQLBase:

    def prepare(self, path):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, file_path):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        self.prepare(file_path)
