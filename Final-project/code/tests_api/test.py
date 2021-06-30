import allure
import pytest
from tests_api.base import ApiBase
from mysql.models import Users
from api.client import ErrorRequest


class TestAuthorizedUser(ApiBase):
    @allure.title('Проверка создания пользователя.')
    def test_create_user(self, user):
        """
        Проверка создания пользователя через API.

        Предусловие:
        Создание тестовых данных: username, password и email.
        Авторизоваться в системе.

        Шаги:
        1. Отправить запрос с тестовыми данными через API.
        2. Найти пользователя по email в базе.

        Ожидаемый результат:
        Тестовые данные, отправленные через API совпадают с теми данными, что находятся в базе.
        По умолчанию у пользователя access == 1, а active = 0.
        Ответ на запрос создания равен 201.
        """
        code, response = self.api_client.create_user(user['username'], user['password'], user['email'])
        user_db = self.mysql.session.query(Users).filter_by(email=user['email']).first()
        assert user_db.username == user['username'], \
            f'Username не совпадают. В базе: {user_db.username}, отправлено: {user["username"]}.'
        assert user_db.email == user['email'], \
            f'Email не совпадают. В базе: {user_db.email}, отправлено: {user["password"]}.'
        assert user_db.password == user['password'], \
            f'Password не совпадают. В базе: {user_db.password}, отправлено: {user["email"]}.'
        assert user_db.access == 1, 'Access по умолчанию не равен 1.'
        assert user_db.active == 0, 'Active по умолчанию не равен 0.'
        assert code == 201, 'Код ответа не совпадает с ожидаемым.'

    @allure.title('Проверка удаления пользователя.')
    def test_delete_user(self, user_db):
        """
        Проверка метода удаления пользователя.

        Предусловие:
        1. Создать пользователя в базе.
        2. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на удаление созданного пользователя.
        2. Сделать запрос в базе на получение пользователей с почтой, с которой был создан пользователь.

        Ожидаемый результат:
        В базе отсутствует пользователь, который был удалён.
        Ответ на запрос удаления равен 204.
        """
        code, response = self.api_client.delete_user(user_db.username)
        assert code == 204, f'Код ошибки не совпадает с ожидаемым. {code} != 204.'
        assert 0 == self.mysql.session.query(Users).filter_by(username=user_db.username).count(), \
            'Пользователь не удалён из базы.'

    @allure.title('Проверка удаления несуществующего пользователя.')
    def test_delete_user(self, user):
        """
        Проверка удаления несуществующего пользователя.

        Предусловие:
        1. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на удаление несуществующего пользователя.

        Ожидаемый результат:
        Ответ на запрос удаления равен 404.
        """
        code, response = self.api_client.delete_user(user["username"])
        assert code == 404, f'Код ошибки не совпадает с ожидаемым. {code} != 404.'

    @allure.title('Проверка блокировки пользователя.')
    def test_block_user(self, user_db):
        """
        Проверка метода блокировки пользователя.

        Предусловия:
        1. Создать пользователя в базе.
        2. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на блокировку созданного пользователя.
        2. Запросить данные по созданному пользователю.

        Ожидаемый результат:
        Код ответа на запрос блокировки пользователя равен 200.
        Значение access в базе изменилось с 1 на 0.
        """
        code, response = self.api_client.block_user(user_db.username)
        assert code == 200, f'Код ошибки не совпадает с ожидаемым. {code} != 200.'
        self.mysql.session.expire(user_db)
        assert user_db.access == 0, 'Статус пользователя не изменился.'

    @allure.title('Проверка метода блокировки уже заблокированного пользователя.')
    def test_block_user_blocked(self, user_block):
        """
        Проверка метода блокировки уже заблокированного пользователя.

        Предусловия:
        1. Создать пользователя в базе со статусом access = 0.
        2. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на блокировку созданного пользователя.
        2. Запросить данные по созданному пользователю.

        Ожидаемый результат:
        Код ответа на запрос блокировки пользователя равен 200.
        Значение access в базе не изменилось.
        """
        code, response = self.api_client.block_user(user_block.username)
        assert code == 304, f'Код ошибки не совпадает с ожидаемым. {code} != 304.'
        self.mysql.session.expire(user_block)
        assert user_block.access == 0, 'Статус пользователя изменился.'

    @allure.title('Проверка метода блокировки несуществующего пользователя.')
    def test_block_user_not_found(self, user):
        """
        Проверка метода блокировки несуществующего пользователя.

        Предусловия:
        1. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на блокировку созданного пользователя.

        Ожидаемый результат:
        Код ответа на запрос блокировки пользователя равен 404.
        """
        code, response = self.api_client.block_user(user['username'])
        assert code == 404, f'Код ошибки не совпадает с ожидаемым. {code} != 404.'

    @allure.title('Проверка активации пользователя.')
    def test_accept_user(self, user_block):
        """
        Проверка метода активации пользователя.

        Предусловия:
        1. Создать пользователя в базе со статусом access = 0.
        2. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на разблокировку созданного пользователя.
        2. Запросить данные по созданному пользователю.

        Ожидаемый результат:
        Код ответа на запрос блокировки пользователя равен 200.
        Значение access в базе изменилось с 0 на 1.
        """
        code, response = self.api_client.accept_user(user_block.username)
        assert code == 200, f'Код ошибки не совпадает с ожидаемым. {code} != 200.'
        self.mysql.session.expire(user_block)
        assert user_block.access == 1, 'Статус пользователя не изменился.'

    @allure.title('Проверка метода активации уже активного пользователя.')
    def test_accept_user_accepted(self, user_db):
        """
        Проверка метода активации уже активного пользователя.

        Предусловия:
        1. Создать пользователя в базе со статусом access = 1.
        2. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на разблокировку созданного пользователя.
        2. Запросить данные по созданному пользователю.

        Ожидаемый результат:
        Код ответа на запрос блокировки пользователя равен 304.
        Значение access в базе не изменилось.
        """
        code, response = self.api_client.accept_user(user_db.username)
        assert code == 304, f'Код ошибки не совпадает с ожидаемым. {code} != 304.'
        self.mysql.session.expire(user_db)
        assert user_db.access == 1, 'Статус пользователя изменился.'

    @allure.title('Проверка метода активации несуществующего пользователя.')
    def test_accept_user_not_found(self, user):
        """
        Проверка метода активации несуществующего пользователя.

        Предусловия:
        1. Авторизоваться в системе для отправки API запросов.

        Шаги:
        1. Отправить запрос на разблокировку несуществующего пользователя.

        Ожидаемый результат:
        Код ответа на запрос блокировки пользователя равен 404.
        """
        code, response = self.api_client.accept_user(user['username'])
        assert code == 404, f'Код ошибки не совпадает с ожидаемым. {code} != 404.'

    @allure.title('Проверка получения статуса приложения.')
    def test_status(self):
        """
        Проверка получения статуса приложения.

        Шаги:
        1. Выполнить запрос на получения статуса приложения.

        Ожидаемый результат:
        Статус приложения - 'ок', код ответа равен 200.
        """
        code, response = self.api_client.status()
        assert response.get('status') in 'ok'
        assert code == 200, f'Код ошибки не совпадает с ожидаемым. {code} != 200.'

    @pytest.mark.parametrize('username, password, email', [
        ['admin', 'admin', 'admin@admin.com'],
        ['adminn', 'admin', 'admin@admin.com'],
        ['adminm', 'admin', 'ad-in@admin.'],
        ['adminm', 'admin', '   '],
        ['adminm', 'admin', 'admin@'],
        ['adminm', 'admin1', 'admin@admin.com'],
        ['adminm', '   ', 'admin@admin.com'],
        ['adminm', '%', 'admin@admin.com'],
        ['%%%%%%', 'admin', 'admin@admin.lu'],
        ['', 'admin', 'admin@admin.lu']
    ])
    @allure.title('Проверка некорректной регистрации.')
    def test_uncorrect_registration(self, username, password, email):
        """
        Проверка создания пользователя с некорректными данными через API.

        Предусловие:
        1. Авторизоваться в системе для отправки API запросов.
        2. Создать некорректный набор тестовых данных.

        Шаги:
        1. Сделать запрос с подсчётом количества пользователей.
        2. Отправить запрос на создание пользователя с некорректными данными из предусловия.
        3. Сделать запрос с подсчётом количества пользователей.

        Ожидаемый результат:
        Количество пользователей на шаге 1 и 3 совпадает.
        Код ответа на создание пользователя с некорректными данными равен 400, т.к. код 400 - плохой запрос (см. Документацию).
        """
        old = self.mysql.session.query(Users).count()
        code, response = self.api_client.create_user(username, password, email)
        new = self.mysql.session.query(Users).count()
        assert code == 400, f'Код ошибки не совпадает с ожидаемым. {code} != 400.'
        assert old == new, 'Количество пользователей изменилось. В базу добавлен новый.'


class TestUnauthorizedUser(ApiBase):
    authorize = False

    @pytest.mark.parametrize('login, password', [
        ['', ''],
        ['', 'admin'],
        ['adminn', '']
    ])
    @allure.title('Проверка авторизации с некорректными данными.')
    def test_incorrect_authorization(self, login, password):
        """
        Проверка авторизации с некорректными данными.

        Предусловие:
        Создать наборы некорректных данных.

        Шаги:
        1. Ввести логин и пароль.
        2. Отправить запрос на авторизацию.

        Ожидаемый результат:
        Авторизация не произошла. Сессионный токен не присвоен.
        """
        with pytest.raises(ErrorRequest):
            self.api_client.login(login, password)

    @allure.title('Проверка активации и деактивации сессии.')
    def test_delete_session(self, user, user_db):
        """
        Проверка деактивации куки сессии после выхода из системы.

        Предусловия:
        1. Создать пользователя, который будет авторизовываться в системе.
        2. Создать тестовые данные пользователя, который будет создаваться.

        Шаги:
        1. Авторизоваться пользователем из п.1 предусловий.
        2. Сохранить куки после авторизации.
        3. Запросить данные по пользователю, под которым была произведена авторизация в системе.
        4. Выйти из системы.
        5. Запросить данные по пользователю, под которым была произведена авторизация в системе.
        6. Подставить сохранённые куки и отправить запрос на создание пользователя с данными из п.2 предусловий.

        Ожидаемый результат:
        На п.3 значение active = 1, в поле start_active_time != null.
        На п.5 значение active = 0.
        На п.6 код ответа = 401.
        """
        self.api_client.login(user_db.username, user_db.password)
        cookie = self.api_client.session.cookies
        self.mysql.session.expire(user_db)
        assert user_db.active == 1, 'Статус сессии не изменился на активный.'
        assert user_db.start_active_time is not None, 'Дата последней активной сессии не активировалась.'
        self.api_client.logout()
        self.mysql.session.commit()
        self.mysql.session.expire(user_db)
        assert user_db.active == 0, 'Статус сессии не изменился на неактивный.'
        self.api_client.session.cookies = cookie
        code, response = self.api_client.create_user(user['username'], user['password'], user['email'])
        assert code == 401, 'Операция выполнена по неактивному пользователю.'

    @allure.title('Проверка создания пользователя без авторизации.')
    def test_create_user(self, user):
        """
        Проверка создания пользователя без авторизации..

        Предусловия:
        1. Создать тестовые username, password, email.

        Шаги:
        1. Отправить API запрос с тестовыми данными из п.1 предусловий.
        2. Сделать запрос в базе по email из предусловия.

        Ожидаемый результат:
        Запись в базе не появилась. Код ответа на API запрос равен 401.
        """
        code, response = self.api_client.create_user(user['username'], user['password'], user['email'])
        assert code == 401, f'Код ошибки не совпадает с ожидаемым. {code} != 401.'
        assert not self.mysql.session.query(Users).filter_by(
            email=user['email']).first(), 'Пользователь добавился в базу.'

    @allure.title('Проверка удаления пользователя без авторизации.')
    def test_delete_user(self, user_db):
        """
        Проверка удаления пользователя без авторизации.

        Предусловия:
        1. Создать пользователя в базе и взять его username.

        Шаги:
        1. Выполнить API запрос удаления пользователя.
        2. Запросить количество пользователей по username из предусловия.

        Ожидаемый результат:
        Количество найденных пользователей из п.2 равно 1.
        Код ответа на запрос из п.1 равен 401.
        """
        code, response = self.api_client.delete_user(user_db.username)
        assert code == 401, f'Код ошибки не совпадает с ожидаемым. {code} != 401.'
        assert 1 == self.mysql.session.query(Users).filter_by(
            username=user_db.username).count(), 'Пользователь удалился из базы.'

    @allure.title('Проверка блокировки пользователя без авторизации.')
    def test_block_user(self, user_db):
        """
        Проверка блокировки пользователя без авторизации.

        Предусловия:
        1. Создать пользователя в базе и взять его username.

        Шаги:
        1. Выполнить API запрос блокировки пользователя.
        2. Запросить статус пользователя по username из предусловия.

        Ожидаемый результат:
        Статус в поле access равен 1.
        Код ответа на запрос из п.1 равен 401.
        """
        code, response = self.api_client.block_user(user_db.username)
        assert code == 401, f'Код ошибки не совпадает с ожидаемым. {code} != 401.'
        self.mysql.session.expire(user_db)
        assert user_db.access == 1, 'Статус пользователя изменился.'

    @allure.title('Проверка активация пользователя без авторизации.')
    def test_accept_user(self, user_block):
        """
        Проверка активации пользователя без авторизации.

        Предусловие:
        1. Создать пользователя со статусом access = 0 и взять его username.

        Шаги:
        1. Выполнить запрос на активацию пользователя по username из предусловия.
        2. Выполнить запрос к базе по данному username.

        Ожидаемый результат:
        Код ответа на запрос активации пользователя равен 401.
        Значение в поле access = 0.
        """
        code, response = self.api_client.accept_user(user_block.username)
        assert code == 401, f'Код ошибки не совпадает с ожидаемым. {code} != 401.'
        self.mysql.session.expire(user_block)
        assert user_block.access == 0, 'Статус пользователя изменился.'
