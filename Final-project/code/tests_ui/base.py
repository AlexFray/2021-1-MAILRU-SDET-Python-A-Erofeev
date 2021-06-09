import pytest
import requests
from _pytest.fixtures import FixtureRequest

from mysql.builder import MySQLBuilder
from mysql.models import Users
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.reg_page import RegPage


class MockError(Exception):
    pass


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report, mysql_client):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)

        self.login_page = LoginPage(driver)
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            self.main_page = MainPage(driver)

    @pytest.fixture(scope='function')
    def registration(self):
        self.login_page.click(self.login_page.locators.CREATE)
        return RegPage(self.driver)

    @pytest.fixture(scope='function')
    def main_page(self, credentials):
        return self.login_page.authorization(*credentials)

    @pytest.fixture(scope='function')
    def user_vk(self, vk_url=None):
        user = self.mysql_builder.create_user()
        r = requests.post('mock:8060/user', json={'username': user.username})
        if r.status_code != 201:
            raise MockError(f'Мок сервис не доступен или произошла ошибка! Ответ: {r.json()}')
        vk_id = r.json()['vk_id']
        return {'user': user.username, 'pass': user.password, 'id': vk_id}

    @pytest.fixture(scope='function')
    def user_db(self) -> Users:
        return self.mysql_builder.create_user()
