import os
import shutil
import time
import requests
import logging
from mock import flask_mock
from requests.exceptions import ConnectionError
from api.fixtures import *
from settings.setting_mock import *


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='session')
def setting_mock():
    return {'HOST': HOST_MOCK, 'PORT': PORT_MOCK}


def pytest_addoption(parser):
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')
    return {'debug_log': debug_log}


@pytest.fixture(scope='function', autouse=True)
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


def start_mock():
    flask_mock.run_mock(HOST_MOCK, PORT_MOCK)
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{HOST_MOCK}:{PORT_MOCK}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError('Mock did not started in 5s!')


def pytest_configure(config):
    base_test_dir = "/tmp/tests"
    if not hasattr(config, 'workerinput'):
        start_mock()
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)
    config.base_test_dir = base_test_dir


def stop_mock():
    requests.get(f'http://{HOST_MOCK}:{PORT_MOCK}/shutdown')


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_mock()
