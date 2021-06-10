from urllib.parse import urljoin

import allure

from ui.pages.base_page import BasePage
from ui.locators.main_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()
    url = 'http://testapp:8080/welcome'

    @allure.step('Выход из системы.')
    def logout(self):
        self.click(self.locators.LOGOUT)

    @allure.step('Получение заголовка и цитаты.')
    def get_quote(self):
        elements = self.finds(self.locators.QUOTE)
        return elements[0].text, elements[1].text