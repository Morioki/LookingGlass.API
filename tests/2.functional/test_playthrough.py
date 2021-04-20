from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_playthrough_all(client):
    json = {"query":"query getPlaythroughs{\n  playthroughs {\n    id\n  }\n}","operationName":"getPlaythroughs"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughs']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_playthrough_specific(client):
    json = {"query":"query getPlaythrough{\n  playthrough(playthroughId: 1) {\n    id\n  }\n}","operationName":"getPlaythrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthrough']
    assert data['id'] == str(1)

def test_playthrough_specific_failure(client):
    json = {"query":"query getPlaythrough{\n  playthrough(playthroughId: 999999999) {\n    id\n  }\n}","operationName":"getPlaythrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthrough']
    assert data is None # TODO look to see if there is a way to output an error

def test_playthrough_insert(client):
    query = "mutation playthrough{\n  insertPlaythrough(gameId: 1, typeId: 1, statusId: 1) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"playthrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertPlaythrough']['success']
    ValueStorage.playthrough_id = int(response.json['data']['insertPlaythrough']['id'])
    assert success

def test_playthrough_insert_failure(client):
    query = "mutation playthrough{\n  insertPlaythrough(gameId: 999999999, typeId: 1, statusId: 1) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"playthrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertPlaythrough']['success']
    assert not success

def test_playthrough_update(client):
    assert ValueStorage.playthrough_id is not None
    query = "mutation playthrough{\n  updatePlaythrough(playthroughId: " + str(ValueStorage.playthrough_id) + ", notes: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"playthrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlaythrough']['success']
    assert success

def test_playthrough_update_failure(client):
    assert ValueStorage.playthrough_id is not None
    query = "mutation playthrough{\n  updatePlaythrough(playthroughId: " + str(ValueStorage.playthrough_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"playthrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlaythrough']['success']
    assert not success

def test_playthrough_delete(client):
    assert ValueStorage.playthrough_id is not None
    query = "mutation playthrough{\n  deletePlaythrough(playthroughId: " + str(ValueStorage.playthrough_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"playthrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlaythrough']['success']
    assert success

def test_playthrough_delete_failure(client):
    assert ValueStorage.playthrough_id is not None
    query = "mutation playthrough{\n  deletePlaythrough(playthroughId: " + str(ValueStorage.playthrough_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"playthrough"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlaythrough']['success']
    assert not success
