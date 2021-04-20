from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_session_all(client):
    json = {"query":"query getSession{\n  sessions {\n    id\n  }\n}","operationName":"getSession"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['sessions']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_session_specific(client):
    json = {"query":"query getSession{\n  session(sessionId: 1) {\n    id\n  }\n}","operationName":"getSession"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['session']
    assert data['id'] == str(1)

def test_session_specific_failure(client):
    json = {"query":"query getSession{\n  session(sessionId: 999999999) {\n    id\n  }\n}","operationName":"getSession"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['session']
    assert data is None # TODO look to see if there is a way to output an error

def test_session_insert(client):
    query = "mutation session{\n  insertSession(gameId: 1, playthroughId: 1, startdate:\"2021-04-10T21:03:10.081979-07:00\", swhours: 1, swminutes: 1, swseconds: 1, swmilliseconds: 1) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"session"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertSession']['success']
    ValueStorage.session_id = int(response.json['data']['insertSession']['id'])
    assert success

def test_session_insert_failure(client):
    query = "mutation session{\n  insertSession(gameId: 9999999999, playthroughId: 1, startdate:\"2021-04-10T21:03:10.081979-07:00\", swhours: 1, swminutes: 1, swseconds: 1, swmilliseconds: 1) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"session"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertSession']['success']
    assert not success

def test_session_update(client):
    assert ValueStorage.session_id is not None
    query = "mutation session{\n  updateSession(sessionId: " + str(ValueStorage.session_id) + ", notes: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"session"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateSession']['success']
    assert success

def test_session_update_failure(client):
    assert ValueStorage.session_id is not None
    query = "mutation session{\n  updateSession(sessionId: " + str(ValueStorage.session_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"session"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateSession']['success']
    assert not success

def test_session_delete(client):
    assert ValueStorage.session_id is not None
    query = "mutation session{\n  deleteSession(sessionId: " + str(ValueStorage.session_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"session"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteSession']['success']
    assert success

def test_session_delete_failure(client):
    assert ValueStorage.session_id is not None
    query = "mutation session{\n  deleteSession(sessionId: " + str(ValueStorage.session_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"session"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteSession']['success']
    assert not success
