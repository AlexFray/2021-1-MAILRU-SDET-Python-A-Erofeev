import pytest
from tests.base import BaseCase


class TestAndroid(BaseCase):
    @pytest.mark.AndroidUI
    def test_search_text(self):
        self.main_page.search_text('Russia', 'население страны составляет 146',
                                   'численность населения россии', '146 млн.')

    @pytest.mark.AndroidUI
    def test_change_source_news(self, source_name='Вести FM'):
        name_news = self.main_page.edit_source(source_name)
        assert name_news == 'Вести ФМ'

    @pytest.mark.AndroidUI
    @pytest.mark.parametrize('expression, res', [['5*5', '25']])
    def test_calculation(self, expression, res):
        assert self.main_page.calculation(expression, res) == res

    @pytest.mark.AndroidUI
    def test_info_app(self, version='1.39.1'):
        self.main_page.check_info(version)
