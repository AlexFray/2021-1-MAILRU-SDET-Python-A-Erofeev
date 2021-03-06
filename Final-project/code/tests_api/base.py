import allure
import pytest
from mimesis import Person
from mysql.builder import MySQLBuilder
from mysql.models import *


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    @allure.title('Инициализация базовых классов.')
    def setup(self, api_client, credentials, credentialsBlock, mysql_client):
        self.api_client = api_client
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
        if self.authorize:
            self.api_client.login(*credentials)

    @pytest.fixture(scope='function')
    @allure.title('Генерация пользовательских данных.')
    def user(self):
        person = Person()
        return {'username': person.username()[:16], 'password': person.password(),
                'email': person.email()}

    @pytest.fixture(scope='function')
    @allure.title('Создание пользователя в базе данных.')
    def user_db(self) -> Users:
        return self.mysql_builder.create_user()

    @pytest.fixture(scope='function')
    @allure.title('Создание заблокированного пользователя в базе данных.')
    def user_block(self) -> Users:
        return self.mysql_builder.create_user(access=0)
