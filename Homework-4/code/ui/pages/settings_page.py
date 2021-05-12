from ui.locators.locators_setting import SettingsPageLocators
from ui.pages.base_page import BasePage
from ui.pages.source_news_page import SourceNewsPage
from ui.pages.about_page import AboutPage


class SettingsPage(BasePage):
    locators = SettingsPageLocators()

    def edit_source_news(self, name_source):
        self.swipe_to_element(self.locators.SOURCE_NEWS, 10)
        self.click(self.locators.SOURCE_NEWS)
        SourceNewsPage(self.driver).change_source(name_source)

    def check_info(self, version):
        self.swipe_to_element(self.locators.ABOUT, 10)
        self.click(self.locators.ABOUT)
        about = AboutPage(self.driver)
        about.check_version(version)
        about.check_right()
