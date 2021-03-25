import random
import pytest
from base import BaseCase
import basic_locators as bl


class TestSuite(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.authorization('ero-feev7@yandex.ru', 'CPaf9Cm9P484BPB')
        assert self.driver.current_url == 'https://target.my.com/dashboard', 'Вход не выполнен.'

    @pytest.mark.UI
    def test_logout(self, auth):
        self.logout()
        assert self.driver.current_url == 'https://target.my.com/', 'Выход не выполнен.'

    @pytest.mark.UI
    def test_edit_profile(self, auth, fio=f'{random.randint(1000000, 9999999)}',
                          email=f'{random.randint(1000000, 9999999)}@mail.ru',
                          phone=f'{random.randint(1000000, 9999999)}'):
        self.edit_profile(FIO=fio, phone=phone, email=email)
        assert self.getText(bl.FIO) in fio, 'ФИО не изменилось или не совпадает.'
        assert self.getText(bl.PHONE) in phone, 'Телефон не изменилося или не совпадает.'
        assert self.getText(bl.EMAIL) in email, 'Почта не изменилась или не совпадает.'

    @pytest.mark.UI
    @pytest.mark.parametrize('button, link', [[bl.SEGMENTS, 'https://target.my.com/segments/segments_list'],
                                              [bl.STATISTICS, 'https://target.my.com/statistics/summary']])
    def test_check_menu(self, auth, button, link):
        self.click(button)
        assert self.driver.current_url == link
