import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.main_page import MainPage


class BaseCase:
    @pytest.fixture()
    def main_page(self, driver, config):
        return MainPage(driver)

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.main_page: MainPage = request.getfixturevalue('main_page')
