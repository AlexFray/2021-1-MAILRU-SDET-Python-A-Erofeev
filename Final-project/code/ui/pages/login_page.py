from urllib.parse import urljoin

import allure

from ui.pages.base_page import BasePage
from ui.locators.login_locators import LoginPageLocators
from ui.pages.main_page import MainPage


# from ui.locators


class LoginPage(BasePage):
    locators = LoginPageLocators()
    url = 'http://testapp:8080/'

    @allure.step('Ввод логина и пароля.')
    def login(self, login, password):
        self.inputText(login, self.locators.USERNAME)
        self.inputText(password, self.locators.PASSWORD)
        self.click(self.locators.SUBMIT)

    @allure.step('Проверка наличия ошибки по локатору: {locator}.')
    def check_error(self, locator):
        self.find(locator)

    def authorization(self, login, password):
        self.login(login, password)
        return MainPage(self.driver)

    def authorization_negative(self, login, password):
        self.login(login, password)
