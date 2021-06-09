import allure
import pytest
from tests_ui.base import BaseCase


class Test(BaseCase):
    authorize = False

    @allure.title('Авторизация в системе.')
    def test_authorization(self, credentials):
        """
        Проверка авторизации в системе.

        Предусловие:
        1. Взять данные пользователя, созданные на этапе инициализации базы данных.

        Шаги:
        1. Перейти на стартовую страницу приложения.
        2. Ввести логин и пароль.
        3. Нажать кнопку "LOGIN".

        Ожидаемый результат:
        Авторизация прошла успешно. Отображается главная страница приложения.
        """
        main_page = self.login_page.authorization(*credentials)
        assert main_page.find(main_page.locators.LOGOUT), 'Кнопка выхода не найдена.'

    @allure.title('Проверка работы кнопки выхода.')
    def test_logout(self, main_page):
        """
        Проверка работы кнопки Logout.

        Предусловие:
        1. Авторизоваться в системе.

        Шаги:
        1. Нажать кнопку "Logout".

        Ожидаемый результат:
        Открылась страница авторизации.
        """
        main_page.logout()
        assert self.login_page.find(self.login_page.locators.CREATE) is not None, 'Кнопка создания пользователя не найдена.'

    @allure.title('Проверка отображения имени и VK ID пользователя.')
    def test_view_vk_id(self, user_vk):
        """
        Проверка отображения имени и VK ID пользователя.

        Предусловия:
        1. Создать пользователя.
        2. Присвоить созданному пользователю VK ID в мок-сервисе.

        Шаги:
        1. Авторизоваться под созданным пользователем.
        2. Обратить внимание на правый верхний угол.

        Ожидаемый результат:
        В верхнем правом углу наличие надписи "Logged as (username созданного пользователя).", а также наличие надписи
        "VK ID: (vk_id созданного пользователя)."
        """
        main_page = self.login_page.authorization(user_vk['user'], user_vk['pass'])
        vk_id = (main_page.locators.VK_ID[0], main_page.locators.VK_ID[1].format(user_vk['id']))
        user_id = (main_page.locators.USER_ID[0], main_page.locators.USER_ID[1].format(user_vk['user']))
        assert main_page.find(vk_id) is not None, 'ID пользователя VK не найден.'
        assert main_page.find(user_id) is not None, 'Имя пользователя не найдено.'

    @allure.title('Проверка отображения имени и отсутствия VK ID пользователя.')
    def test_not_view_vk_id(self, user_db):
        """
        Проверка отображения имени и отсутствия VK ID пользователя.

        Предусловия:
        1. Создать пользователя.

        Шаги:
        1. Авторизоваться под созданным пользователем.
        2. Обратить внимание на правый верхний угол.

        Ожидаемый результат:
        В верхнем правом углу наличие надписи "Logged as (username созданного пользователя)" и отсутствие надписи
        "VK ID: "
        """
        main_page = self.login_page.authorization(user_db.username, user_db.password)
        vk_id = (main_page.locators.VK_ID[0], main_page.locators.VK_ID[1].format(''))
        user_id = (main_page.locators.USER_ID[0], main_page.locators.USER_ID[1].format(user_db.username))
        assert main_page.find(vk_id) is None, 'Надпись c VK ID найдена на главной страница.'
        assert main_page.find(user_id) is not None, "Имя пользователя не найдено."

    @allure.title('Проверка отображения новой цитаты при обновлении.')
    def test_new_quote(self, main_page):
        """
        Проверка отображения цитат на главной странице.

        Предусловие:
        1. Авторизоваться в системе.

        Шаги:
        1. Обратить внимание на цитату в нижней части страницы.
        2. Обновить страницу.
        3. Вновь посмотреть на цитату внизу.

        Ожидаемый результат:
        В п.1 и п.3 отображается надпись "powered by ТЕХНОАТОМ".
        Цитаты не совпадают после обновления страницы.
        """
        title, quote = main_page.get_quote()
        self.driver.refresh()
        title_new, new_quote = main_page.get_quote()
        assert title == title_new == 'powered by ТЕХНОАТОМ', 'Заголовок отсутствует или не соответствует предыдущему.'
        assert quote != new_quote, 'Цитаты повторяются.'

    @pytest.mark.parametrize('login, password, message', [
        ['admin', 'dasd', 'Incorrect username length'],
        ['adminn', 'admi', 'Invalid username or password'],
        ['    ', '    ', 'Invalid username or password'],
        ['   ', 'dsdds', 'Invalid username or password'],
        ['dsdsdsd', '    ', 'Invalid username or password']
    ])
    @allure.title('Авторизация некорректными учётными данными.')
    def test_uncorrect_authorization(self, login, password, message):
        """
        Проверка авторизации некорректными данными.

        Предусловие:
        1. Создать набор некорректных данных.

        Шаги:
        1. Ввести данные из набора.

        Ожидаемый результат:
        Текст ответ соответствует тому, какие данные некорректны. Текст ошибки корректен и написан в локализации
        всего приложения.
        """
        self.login_page.authorization_negative(login, password)
        assert self.login_page.find(self.login_page.locators.ERROR) is not None, \
            'Поле c сообщением об ошибке не отображается.'
        assert self.login_page.wait_text(message, self.login_page.locators.ERROR), \
            'Корректное сообщение об ошибке не найдено.'

    @allure.title('Авторизация заблокированным пользователем.')
    def test_authorization_blocked(self, blocked_user):
        """
        Проверка авторизации пользователем, который был заблокирован.

        Предусловие:
        1. Взять авторизационные данные заблокированного пользователя.

        Шаги:
        1. Ввести данные заблокированного пользователя.
        2. Нажать кнопку "LOGIN".

        Ожидаемый результат:
        Получена ошибка: "Your account has been blocked."
        """
        self.login_page.authorization_negative(blocked_user['user'], blocked_user['pass'])
        assert self.login_page.find(self.login_page.locators.ERROR) is not None, \
            'Поле c сообщением об ошибке не отображается.'
        assert self.login_page.wait_text('Your account has been blocked.', self.login_page.locators.ERROR), \
            'Корректное сообщение об ошибке не найдено.'

    @allure.title('Регистрация пользователя с корректными данными.')
    def test_registration(self, registration, create_user):
        """
        Проверка регистрации пользователя с корректными данными.

        Предусловие:
        1. Создать набор корректных данных для регистрации.
        2. Перейти на страницу регистрации.

        Шаги:
        1. Ввести имя пользователя, email пароль и подтверждение пароля.
        2. Подставить галочку согласия.
        3. Нажать кнопку "REGISTER".

        Ожидаемый результат:
        Регистрация прошла успешно. Пользователь авторизован, открыта главная страница.
        """
        main_page = registration.correct_create(create_user['user'], create_user['pass'], create_user['email'],
                                                create_user['pass'])
        assert main_page.find(main_page.locators.LOGOUT), 'Кнопка выхода отсутствует. Главная страница не загрузилась.'

    @pytest.mark.parametrize('username, password, email, conf_password, message', [
        ['admin', 'admin', 'admin@admin.com', 'admin', 'Incorrect username length'],
        ['admin', 'admin', 'admin@admin', 'admin', 'Invalid username and email address'],
        ['admin', '   ', 'admin@admin', '   ', 'Invalid username and email address and password'],
        ['admin', 'admin', 'admin@admin', 'admin', 'Invalid username and email address. Passwords must match'],
        ['adminn', 'admin', 'admin@admin.com', 'admin', 'User already exist'],
        ['adminr', 'admin', 'admin@admin.ru', 'admin', 'User already exist'],
        ['adminn', 'admin', 'admin@admin', 'admin', 'Invalid email address'],
        ['adminm', 'admin', 'ad-in@admin.', 'admin', 'Invalid email address'],
        ['adminm', 'admin', '   ', 'admin', 'Invalid email address'],
        ['adminm', 'admin', 'admin@', 'admin', 'Incorrect email length'],
        ['adminm', 'admin1', 'admin@admin.com', 'admin2', 'Passwords must match'],
        ['adminm', '   ', 'admin@admin.com', '   ', 'Invalid password'],
        ['adminm', '%', 'admin@admin.com', '%', 'Invalid password'],
        ['%%%%%%', 'admin', 'admin@admin.lu', 'admin', 'Invalid username']
    ])
    @allure.title('Проверка валидации формы регистрации.')
    def test_uncorrect_registation(self, registration, username, password, email, conf_password, message):
        """
        Проверка регистрации пользователя с некорректными данными.

        Предусловия:
        1. Создать набор с некорректными данными для регистрации.
        2. Перейти на страницу регистрации.

        Шаги:
        1. Ввести имя пользователя, email пароль и подтверждение пароля.
        2. Подставить галочку согласия.
        3. Нажать кнопку "REGISTER".

        Ожидаемый результат:
        Отображается ошибка в соответствии с тем, какие данные были указаны некорректно. Текст ошибки отображается
        корректно. Локализация ошибки соответствует локализации всего приложения.
        """
        registration.uncorrect_create(username, password, email, conf_password)
        assert registration.wait_text(message, registration.locators.ERROR), 'Корректная ошибка регистрации отсутствует.'
