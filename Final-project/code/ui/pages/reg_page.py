from urllib.parse import urljoin

import allure

from ui.pages.base_page import BasePage
from ui.locators.reg_locators import RegPageLocators
from ui.pages.main_page import MainPage


class RegPage(BasePage):
    locators = RegPageLocators()
    url = 'http://testapp:8080/reg'

    @allure.step('Создание пользователя в системе: {username}, {password}, {email}, {password_confirm}.')
    def create_user(self, username, password, email, password_confirm=None):
        self.inputText(username, self.locators.USERNAME)
        self.inputText(password, self.locators.PASSWORD)
        self.inputText(email, self.locators.EMAIL)
        password_confirm = password_confirm if password_confirm is not None else password
        self.inputText(password_confirm, self.locators.PASSWORD_CONFIRM)
        self.click(self.locators.ACCEPT)
        self.click(self.locators.SUBMIT)

    def correct_create(self, username, password, email, password_confirm):
        self.create_user(username, password, email, password_confirm)
        return MainPage(self.driver)

    def uncorrect_create(self, username, password, email, password_confirm):
        self.create_user(username, password, email, password_confirm)
