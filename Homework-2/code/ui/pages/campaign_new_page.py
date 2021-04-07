import allure
import logging

from ui.pages.base_page import BasePage
from ui.locators.campaign_new_locators import CampaignPageLocators

logger = logging.getLogger('test')


class CampaignNewPage(BasePage):
    url = 'https://target.my.com/campaign/new'
    locators = CampaignPageLocators()

    @allure.step('Создание и заполнение банера.')
    def create_banner(self, file_path, name):
        logger.info('Выбор типа конверсии.')
        self.click(self.locators.TRAFFIC)
        logger.info('Заполнение ссылки.')
        self.inputText('mail.ru', self.locators.LINK)
        logger.info('Выбор формата рекламного объявления.')
        self.click(self.locators.BANNER)
        logger.info('Заполнение названия кампании.')
        self.inputText(name, self.locators.NAME)
        logger.info(f'Загрузка картинки: {file_path}')
        file_upload = self.find(self.locators.UPLOAD_FILE)
        file_upload.send_keys(file_path)
        logger.info(f'Сохранение выбранной картинки.')
        self.click(self.locators.SAVE_IMAGE)
        logger.info(f'Ввод ссылки, куда будет вести картинка.')
        self.inputText('mail.ru', self.locators.LINK_FOR_BANNER)
        logger.info(f'Создание кампании.')
        self.click(self.locators.CREATE_CAMPAIGN)
