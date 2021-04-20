from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_playthroughtype_all(client):
    json = {"query":"query getPlaythroughTypes{\n  playthroughtypes {\n    id\n  }\n}","operationName":"getPlaythroughTypes"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughtypes']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_playthroughtype_specific(client):
    json = {"query":"query getPlaythroughType{\n  playthroughtype(playthroughtypeId: 1) {\n    id\n  }\n}","operationName":"getPlaythroughType"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughtype']
    assert data['id'] == str(1)

def test_playthroughtype_specific_failure(client):
    json = {"query":"query getPlaythroughType{\n  playthroughtype(playthroughtypeId: 999999999) {\n    id\n  }\n}","operationName":"getPlaythroughType"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughtype']
    assert data is None # TODO look to see if there is a way to output an error

def test_playthroughtype_insert(client):
    query = "mutation playthroughtype{\n  insertPlaythroughType(description: \"Test Insert\", active: false) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"playthroughtype"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertPlaythroughType']['success']
    ValueStorage.playthroughtype_id = int(response.json['data']['insertPlaythroughType']['id'])
    assert success

# def test_playthroughtype_insert_failure(client):
#     query = "mutation playthroughtype{\n  insertPlaythroughType(description: \"Test Insert\", active: false) {\n    success\n    id\n  }\n}"
#     json = {"query": query,"operationName":"playthroughtype"}
#     response = client.post('/graphql', headers=ValueStorage.headers, json=json)
#     success = response.json['data']['insertPlaythroughType']['success']
#     assert not success

def test_playthroughtype_update(client):
    assert ValueStorage.playthroughtype_id is not None
    query = "mutation playthroughtype{\n  updatePlaythroughType(playthroughtypeId: " + str(ValueStorage.playthroughtype_id) + ", description: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"playthroughtype"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlaythroughType']['success']
    assert success

def test_playthroughtype_update_failure(client):
    assert ValueStorage.playthroughtype_id is not None
    query = "mutation playthroughtype{\n  updatePlaythroughType(playthroughtypeId: " + str(ValueStorage.playthroughtype_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"playthroughtype"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlaythroughType']['success']
    assert not success

def test_playthroughtype_delete(client):
    assert ValueStorage.playthroughtype_id is not None
    query = "mutation playthroughtype{\n  deletePlaythroughType(playthroughtypeId: " + str(ValueStorage.playthroughtype_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"playthroughtype"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlaythroughType']['success']
    assert success

def test_playthroughtype_delete_failure(client):
    assert ValueStorage.playthroughstatus_id is not None
    query = "mutation playthroughtype{\n  deletePlaythroughType(playthroughtypeId: " + str(ValueStorage.playthroughstatus_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"playthroughtype"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlaythroughType']['success']
    assert not success
