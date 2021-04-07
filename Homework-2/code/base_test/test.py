import allure
import pytest
from selenium.webdriver.common.by import By

from base import BaseCase


class TestSuite(BaseCase):
    @pytest.mark.UI
    @pytest.mark.parametrize('login, password', [
        ['+79999999999', '123123'],
        ['ero-feev7@yandex.ru', 'password']
    ])
    @allure.title('Проверка авторизации под пользователем {login}:{password}')
    def test_authorization_negative(self, login, password):
        page = self.MainPage.authorization_negative(login, password)
        assert 'Error' in page.find(page.locators.ERROR).text

    @pytest.mark.UI
    @allure.title('Проверка создания кампании.')
    def test_create_campaign(self, file_path, name_campaign):
        dashboard, name = name_campaign
        dashboard.create_campaign(file_path, name)
        table = (dashboard.locators.NAME_CAMPAIGN[0], dashboard.locators.NAME_CAMPAIGN[1].format(name))
        assert self.MainPage.find(table).text == name

    @pytest.mark.UI
    @allure.title('Проверка создания сегмента.')
    def test_create_segment(self, segment_for_create):
        segment, name = segment_for_create
        segment.create_segment(name)
        table = (segment.locators.NEW_SEGMENT[0], segment.locators.NEW_SEGMENT[1].format(name))
        assert self.MainPage.find(table).text == name

    @pytest.mark.UI
    @allure.title('Проверка удаления сегмента.')
    def test_delete_segment(self, segment_for_delete):
        segment, name = segment_for_delete
        segment.delete_segment(name)
        self.driver.refresh()
        table = (segment.locators.NEW_SEGMENT[0], segment.locators.NEW_SEGMENT[1].format(name))
        assert self.MainPage.find(table) is None
