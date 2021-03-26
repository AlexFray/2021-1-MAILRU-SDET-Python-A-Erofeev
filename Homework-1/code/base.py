import pytest
import basic_locators as bl
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains

TIME_WAIT = 10


class BaseCase:
    driver = None
    config = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    @pytest.fixture(scope='function')
    def auth(self):
        self.authorization('ero-feev7@yandex.ru', 'CPaf9Cm9P484BPB')

    def authorization(self, login, password):
        self.find(bl.SIGN_IN).click()
        self.inputText(login, bl.LOGIN)
        self.inputText(password, bl.PASSWORD)
        self.find(bl.ENTER).click()
        time.sleep(3)

    def logout(self):
        self.click(bl.USER_ACCOUNT)
        self.find(bl.MENU_ACCOUNT)
        time.sleep(1)
        self.click(bl.EXIT)
        time.sleep(1)

    def edit_profile(self, FIO, phone, email):
        self.driver.get('https://target.my.com/profile/contacts')
        self.inputText(FIO, bl.FIO)
        self.inputText(phone, bl.PHONE)
        self.inputText(email, bl.EMAIL)
        self.find(bl.SAVE).click()
        time.sleep(2)
        self.driver.refresh()
        time.sleep(2)

    def find(self, locator):
        try:
            return WebDriverWait(self.driver, TIME_WAIT).until(ec.presence_of_element_located(locator))
        except exceptions.TimeoutException:
            return None

    def inputText(self, text, locator):
        input = self.find(locator)
        input.clear()
        input.send_keys(text)

    def click(self, locator):
        actions = ActionChains(self.driver)
        actions.click(self.find(locator)).perform()

    def getText(self, locator):
        return self.find(locator).get_attribute('value')

