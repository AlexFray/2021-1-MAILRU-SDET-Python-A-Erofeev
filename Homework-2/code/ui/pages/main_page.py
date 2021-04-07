import logging
import allure

from ui.pages.base_page import BasePage
from ui.locators.main_locators import MainPageLocators
from ui.pages.authorization_page import AuthorizationPage

logger = logging.getLogger('test')


class MainPage(BasePage):
    locators = MainPageLocators()
    url = 'https://target.my.com'

    @allure.step('Авторизация пользователем {login}:{password}')
    def authorization(self, login, password):
        logger.info('Открытие формы авторизации.')
        self.click(self.locators.SIGN_IN)
        logger.info('Заполнение логина и пароля.')
        self.inputText(login, self.locators.LOGIN)
        self.inputText(password, self.locators.PASSWORD)
        logger.info('Нажатие на кнопку входа.')
        self.click(self.locators.ENTER)

    @allure.step('Авторизация некорректным пользователем {login}:{password}')
    def authorization_negative(self, login, password):
        self.authorization(login, password)
        return AuthorizationPage(self.driver)
