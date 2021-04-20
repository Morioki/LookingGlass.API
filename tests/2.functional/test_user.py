from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_user_all(client):
    json = {"query":"query getUsers{\n  users {\n    id\n  }\n}","operationName":"getUsers"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['users']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_user_specific(client):
    json = {"query":"query getUsers{\n  user {\n    id\n  }\n}","operationName":"getUsers"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['user']
    assert data['id'] == str(1)

def test_user_specific_failure(client):
    json = {"query":"query getUsers{\n  user {\n    id\n  }\n}","operationName":"getUsers"}
    response = client.post('/graphql',  json=json)
    data = response.json['data']['user']
    assert data is None # TODO look to see if there is a way to output an error