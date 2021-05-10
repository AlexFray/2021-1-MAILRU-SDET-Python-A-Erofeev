import shutil
import sys
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption('--appium', default='http://127.0.0.1:4723/wd/hub')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--apk', default='Marussia_v1.39.1.apk')


@pytest.fixture(scope='session')
def config(request):
    appium = request.config.getoption('--appium')
    debug_log = request.config.getoption('--debug_log')
    app = request.config.getoption('--apk')
    return {'appium': appium, 'debug_log': debug_log, 'app': app}


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


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))
