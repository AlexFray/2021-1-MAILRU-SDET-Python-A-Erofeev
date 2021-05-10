import os
import re

import pytest
from appium import webdriver


def get_driver(appium_url, app):
    driver = webdriver.Remote(appium_url, desired_capabilities={
        "platformName": "Android",
        "platformVersion": "8.1",
        "automationName": "Appium",
        "appPackage": "ru.mail.search.electroscope",
        "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
        "app": os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../resources/{app}')),
        "autoGrantPermissions": True
    })
    return driver


@pytest.fixture(scope='function')
def driver(config):
    appium_url = config['appium']
    app = config['app']
    browser = get_driver(appium_url, app)
    yield browser
    browser.quit()


@pytest.fixture(scope='session')
def version(config):
    version_app = re.search(r'\d{1,2}.\d{1,3}.\d{1,3}', config['app'])
    return version_app.group()
