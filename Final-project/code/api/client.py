import logging

import allure
import requests

from urllib.parse import urljoin
from requests.cookies import cookiejar_from_dict

logger = logging.getLogger('test')


class ErrorRequest(Exception):
    pass


class Client:
    def __init__(self, addr):
        self.addr = addr
        self.session = requests.Session()

    @property
    def login_page_headers(self):
        return {
            'location': f'{self.addr}/welcome/',
            'Vary': 'Cookie'
        }

    @allure.step('Авторизация пользователем {login}:{password}')
    def login(self, login, password):
        data = {
            'username': login,
            'password': password,
            'submit': "Login"
        }
        r = self._request('POST', '/login', data=data, header=self.login_page_headers)
        try:
            response_cookies = r.headers['Set-Cookie'].split(';')
        except Exception as e:
            raise ErrorRequest(e)
        if r.status_code != 302:
            raise ErrorRequest(f'Ошибка авторизации. {r.status_code} != 302')
        session_token = [s for s in response_cookies if 'session' in s][0].split('=')[-1]
        self.session.cookies = cookiejar_from_dict({'session': session_token})

    @allure.title('Выход из сессии.')
    def logout(self):
        r = self._request('GET', '/logout')
        if r.status_code != 302:
            raise ErrorRequest(f'Ошибка выхода из системы. {r.status_code} != 302')

    @allure.step("Создание пользователя: {username}, {password}, {email}")
    def create_user(self, username, password, email):
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        r = self._request('POST', '/api/add_user', json=data)
        logger.info(f"response: code={r.status_code}, data={r.text}")
        return r.status_code, r.text

    @allure.step("Создание пользователя: {username}")
    def delete_user(self, username):
        r = self._request('GET', f'/api/del_user/{username}')
        logger.info(f"response: code={r.status_code}, data={r.text}")
        return r.status_code, r.text

    @allure.step("Блокировка пользователя: {username}")
    def block_user(self, username):
        r = self._request('GET', f'/api/block_user/{username}')
        logger.info(f"response: code={r.status_code}, data={r.text}")
        return r.status_code, r.text

    @allure.step("Активация пользователя: {username}")
    def accept_user(self, username):
        r = self._request('GET', f'/api/accept_user/{username}')
        logger.info(f"response: code={r.status_code}, data={r.text}")
        return r.status_code, r.text

    @allure.step("Запрос статуса.")
    def status(self):
        r = self._request('GET', '/status')
        logger.info(f"response: code={r.status_code}, data={r.json()}")
        return r.status_code, r.json()

    def _request(self, method, path, data=None, param=None, json=None, header=None):
        url = urljoin(self.addr, path)
        kwargs = {
            'allow_redirects': False
        }
        if param:
            kwargs['params'] = param
        if json:
            kwargs['json'] = json
        if data:
            kwargs['data'] = data
        if header:
            kwargs['headers'] = header

        logger.info(f"request {method} - {path} - data={data} - json={json}")
        return self.session.request(method, url, **kwargs)
