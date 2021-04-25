import allure
import logging

from ui.pages.base_page import BasePage
from ui.pages.campaign_new_page import CampaignNewPage
from ui.locators.dashboard_locators import DashboardPageLocators

logger = logging.getLogger('test')


class DashboardPage(BasePage):
    locators = DashboardPageLocators()
    url = 'https://target.my.com/dashboard'

    @allure.step('Создание кампании.')
    def create_campaign(self, file_path, name):
        create = self.find(self.locators.CREATE)
        if create is None or not create.is_displayed():
            create = self.find(self.locators.CREATE_NEW)
        create.click()
        campaign = CampaignNewPage(self.driver)
        campaign.create_banner(file_path, name)
        assert self.is_opened()

    @allure.step('Удаление кампании.')
    def delete_campaign(self, name):
        checkbox = (self.locators.CAMPAIGN_CHECKBOX[0], self.locators.CAMPAIGN_CHECKBOX[1].format(name))
        self.click(checkbox)
        self.click(self.locators.ACTION_CAMPAIGN_MENU)
        self.click(self.locators.ACTION_CAMPAIGN_DELETE)