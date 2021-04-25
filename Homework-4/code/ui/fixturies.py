import os

import pytest
from appium import webdriver


def get_driver(appium_url):
    driver = webdriver.Remote(appium_url, desired_capabilities={
        "platformName": "Android",
        "platformVersion": "8.1",
        "automationName": "Appium",
        "appPackage": "ru.mail.search.electroscope",
        "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
        "app": os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../resources/Marussia_v1.39.1.apk')),
        "autoGrantPermissions": True
    })
    return driver


@pytest.fixture(scope='function')
def driver(config):
    appium_url = config['appium']
    browser = get_driver(appium_url)
    yield browser
    browser.quit()
