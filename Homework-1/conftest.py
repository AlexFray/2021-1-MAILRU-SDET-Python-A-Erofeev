from selenium import webdriver
import pytest


@pytest.fixture(scope='function')
def driver():
    browser = webdriver.Chrome(executable_path='/home/aleksey/Projects/2021-1-MAILRU-SDET-Python-A-Erofeev/Homework-1/chromedriver')
    browser.get('https://target.my.com/')
    browser.set_window_size(1920, 1080)
    yield browser
    browser.close()
