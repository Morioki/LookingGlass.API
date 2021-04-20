import pytest
from api import api

print('LOADING FROM CONFTEST.PY')

@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    with api.app.test_client() as client:
        yield client

class ValueStorage:
    game_id = None
    generation_id = None
    genre_id = None
    platform_id = None
    playthrough_id = None
    playthroughstatus_id = None
    playthroughtype_id = None
    session_id = None

    headers = {
        'API_TOKEN': 'testapikey'
    }