import os
import allure
import pytest
from mimesis.random import Random
from mimesis import Person
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from api.client import Client

random = Random()
person = Person()


class UnsupportedBrowserType(Exception):
    pass


@pytest.fixture(scope='function')
def user():
    username = random.randstr(length=6)
    password = random.randstr(length=6)
    email = person.email()
    return {'user': username, 'pass': password, 'email': email}


@pytest.fixture(scope='function')
def create_user(user, api_client, credentials):
    api_client.login(*credentials)
    api_client.create_user(user['user'], user['pass'], user['email'])
    yield user
    api_client.delete_user(user['user'])


@pytest.fixture(scope='function')
def blocked_user(api_client, create_user):
    api_client.block_user(create_user['user'])
    return create_user


@pytest.fixture(scope='session')
def cookies(credentials, config):
    api_client = Client(config['url'])
    api_client.login(*credentials)

    cookies_list = []
    for cookie in api_client.session.cookies:
        cookie_dict = {'domain': cookie.domain, 'name': cookie.name, 'value': cookie.value, 'secure': cookie.secure,
                       'httpOnly': True}
        cookies_list.append(cookie_dict)

    return cookies_list


def get_driver(config):
    browser_name = config['browser']
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = ChromeOptions()

        if selenoid is not None:
            caps = {
                'browserName': browser_name,
                'version': '89.0',
                'sessionTimeout': '2m'
                # 'additionalNetworks': [config.get('network')]
            }
            if vnc:
                caps['version'] += '_vnc'
                caps['enableVNC'] = True
            browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)
        else:
            manager = ChromeDriverManager(version='latest', log_level=0)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()

        if selenoid is not None:
            caps = {
                'browserName': browser_name,
                'version': '86.0',
                'sessionTimeout': '2m'
            }
            if vnc:
                caps['version'] += '_vnc'
                caps['enableVNC'] = True
            browser = webdriver.Remote(selenoid + '/wd/hub', options=options, desired_capabilities=caps)
        else:
            manager = GeckoDriverManager(version='latest', log_level=0)
            browser = webdriver.Firefox(executable_path=manager.install(), options=options)
    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')
    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser = get_driver(config)

    browser.get(url)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)
