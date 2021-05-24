import pytest
import os
from mysql.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.recreate_db()
    mysql_client.connect()
    mysql_client.create_count_requests()
    mysql_client.create_count_top_resources()
    mysql_client.create_internal_errors()
    mysql_client.create_big_requests_error()
    mysql_client.create_count_requests_type()
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function')
def file_path(repo_root):
    return os.path.join(repo_root, 'resources', 'access.log')
