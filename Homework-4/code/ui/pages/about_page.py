from selenium.webdriver.common.by import By
from ui.locators.locators_about import AboutPageLocators
from ui.pages.base_page import BasePage


class AboutPage(BasePage):
    locators = AboutPageLocators()

    def check_version(self, version):
        version_app = self.find(self.locators.VERSION).text
        assert version in version_app

    def check_right(self):
        right = self.find(self.locators.COPYRIGHT).text
        assert 'Все права защищены' in right
