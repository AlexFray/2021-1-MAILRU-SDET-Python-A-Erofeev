from urllib.parse import urljoin

from ui.pages.base_page import BasePage
from ui.locators.main_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()
    url = 'http://testapp:8080/welcome'

    def logout(self):
        self.click(self.locators.LOGOUT)

    def get_quote(self):
        elements = self.finds(self.locators.QUOTE)
        return elements[0].text, elements[1].text