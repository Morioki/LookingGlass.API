from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_playthroughstatus_all(client):
    json = {"query":"query getPlaythroughStatuses{\n  playthroughstatuses {\n    id\n  }\n}","operationName":"getPlaythroughStatuses"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughstatuses']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_playthroughstatus_specific(client):
    json = {"query":"query getPlaythroughStatus{\n  playthroughstatus(playthroughstatusId: 1) {\n    id\n  }\n}","operationName":"getPlaythroughStatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughstatus']
    assert data['id'] == str(1)

def test_playthroughstatus_specific_failure(client):
    json = {"query":"query getPlaythroughStatus{\n  playthroughstatus(playthroughstatusId: 99999999) {\n    id\n  }\n}","operationName":"getPlaythroughStatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['playthroughstatus']
    assert data is None # TODO look to see if there is a way to output an error

def test_playthroughstatus_insert(client):
    query = "mutation playthroughstatus{\n  insertPlaythroughStatus(description: \"Test Insert\", active: false) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"playthroughstatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertPlaythroughStatus']['success']
    ValueStorage.playthroughstatus_id = int(response.json['data']['insertPlaythroughStatus']['id'])
    assert success

# def test_playthroughstatus_insert_failure(client):
#     query = "mutation playthroughstatus{\n  insertPlaythroughStatus(description: \"Test Insert\", active: false) {\n    success\n    id\n  }\n}"
#     json = {"query": query,"operationName":"playthroughstatus"}
#     response = client.post('/graphql', headers=ValueStorage.headers, json=json)
#     success = response.json['data']['insertPlaythroughStatus']['success']
#     assert not success

def test_playthroughstatus_update(client):
    assert ValueStorage.playthroughstatus_id is not None
    query = "mutation playthroughstatus{\n  updatePlaythroughStatus(playthroughstatusId: " + str(ValueStorage.playthroughstatus_id) + ", description: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"playthroughstatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlaythroughStatus']['success']
    assert success

def test_playthroughstatus_update_failure(client):
    assert ValueStorage.playthroughstatus_id is not None
    query = "mutation playthroughstatus{\n  updatePlaythroughStatus(playthroughstatusId: " + str(ValueStorage.playthroughstatus_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"playthroughstatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlaythroughStatus']['success']
    assert not success

def test_playthroughstatus_delete(client):
    assert ValueStorage.playthroughstatus_id is not None
    query = "mutation playthroughstatus{\n  deletePlaythroughStatus(playthroughstatusId: " + str(ValueStorage.playthroughstatus_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"playthroughstatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlaythroughStatus']['success']
    assert success

def test_playthroughstatus_delete_failure(client):
    assert ValueStorage.playthroughstatus_id is not None
    query = "mutation playthroughstatus{\n  deletePlaythroughStatus(playthroughstatusId: " + str(ValueStorage.playthroughstatus_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"playthroughstatus"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlaythroughStatus']['success']
    assert not success
