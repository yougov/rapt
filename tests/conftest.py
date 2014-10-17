import os

from click.testing import CliRunner
from mock import patch

import pytest


@pytest.fixture()
def cli():
    env = {
        'VELOCIRAPTOR_URL': 'http://testrapt',
        'VELOCIRAPTOR_AUTH_DOMAIN': 'testrapt',
        'VELOCIRAPTOR_USERNAME': 'rapt_user',
        'VELOCIRAPTOR_PASSWORD': 'secret',
    }
    return CliRunner(env=env)


@pytest.fixture()
def query(request):
    query_patcher = patch('rapt.models.query')
    query = query_patcher.start()
    request.addfinalizer(query_patcher.stop)
    return query


GET_VR_PATCHER = patch('rapt.connection.get_vr')


def pytest_configure(config):
    GET_VR_PATCHER.start()
    os.environ['VELOCIRAPTOR_URL'] = 'http://testrapt'
    os.environ['VELOCIRAPTOR_AUTH_DOMAIN'] = 'testrapt'
    os.environ['VELOCIRAPTOR_USERNAME'] = 'rapt_user'


def pytest_unconfigure(config):
    GET_VR_PATCHER.stop()
