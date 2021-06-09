import logging
import shutil
import sys
from mysql.client import MySQLClient
from ui.fixtures import *
from settings import appconf


def pytest_addoption(parser):
    parser.addoption('--url', default='http://testapp:8080')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--network_docker', default='final_default')
    parser.addoption('--selenoid_ip', default='172.19.0.1')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MySQLClient(user='root', password='pass', db_name=appconf.MYSQL_DB, host=appconf.MYSQL_HOST, port=appconf.MYSQL_PORT)
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def credentials():
    return 'adminn', 'admin'


@pytest.fixture(scope='function')
def credentialsBlock():
    return 'userblock', 'userblock'


@pytest.fixture(scope='function')
def api_client(config):
    return Client(config['url'])


@pytest.fixture(scope='function')
def second_user(config, credentials):
    second_api_client = Client(config['url'])
    second_api_client.login(*credentials)
    return second_api_client


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    if request.config.getoption('--selenoid'):
        selenoid = f"http://{request.config.getoption('--selenoid_ip')}:4444"
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
    else:
        selenoid = None
        vnc = False

    browser = request.config.getoption('--browser')
    debug_log = request.config.getoption('--debug_log')
    network = request.config.getoption('--network_docker')
    return {'url': url, 'browser': browser, 'debug_log': debug_log, 'selenoid': selenoid, 'vnc': vnc, 'network': network}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_test_dir = 'C:\\tests'
    else:
        base_test_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):  # execute only once on main worker
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
