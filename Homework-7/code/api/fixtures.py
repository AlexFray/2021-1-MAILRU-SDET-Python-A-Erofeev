import random

import pytest
from mimesis import Person
from mock.flask_mock import DATA

fake = Person()


@pytest.fixture(scope='function')
def create_user():
    id_user = random.randint(40, 60)
    DATA[id_user] = fake.first_name()
    yield {'id': id_user, 'name': DATA[id_user]}
