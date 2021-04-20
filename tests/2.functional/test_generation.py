from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_generation_all(client):
    json = {"query":"query getGeneration{\n  generations {\n    id\n  }\n}","operationName":"getGeneration"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['generations']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_generation_specific(client):
    json = {"query":"query getGeneration{\n  generation(generationId: 1) {\n    id\n  }\n}","operationName":"getGeneration"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['generation']
    assert data['id'] == str(1)

def test_generation_specific_failure(client):
    json = {"query":"query getGeneration{\n  generation(generationId: 99999999) {\n    id\n  }\n}","operationName":"getGeneration"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['generation']
    assert data is None # TODO look to see if there is a way to output an error

def test_generation_insert(client):
    query = "mutation generation{\n  insertGeneration(generationcode: \"99\", description: \"Test Record To Insert\") {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"generation"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertGeneration']['success']
    ValueStorage.generation_id = int(response.json['data']['insertGeneration']['id'])
    assert success

def test_generation_insert_failure(client):
    query = "mutation generation{\n  insertGeneration(generationcode: \"9999\", description: \"Test Record To Insert\") {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"generation"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertGeneration']['success']
    assert not success

def test_generation_update(client):
    assert ValueStorage.generation_id is not None
    query = "mutation generation{\n  updateGeneration(generationId: " + str(ValueStorage.generation_id) + ", generationcode: \"66\", description: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"generation"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateGeneration']['success']
    assert success

def test_generation_update_failure(client):
    assert ValueStorage.generation_id is not None
    query = "mutation generation{\n  updateGeneration(generationId: " + str(ValueStorage.generation_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"generation"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateGeneration']['success']
    assert not success

def test_generation_delete(client):
    assert ValueStorage.generation_id is not None
    query = "mutation generation{\n  deleteGeneration(generationId: " + str(ValueStorage.generation_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"generation"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteGeneration']['success']
    assert success

def test_generation_delete_failure(client):
    assert ValueStorage.generation_id is not None
    query = "mutation generation{\n  deleteGeneration(generationId: " + str(ValueStorage.generation_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"generation"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteGeneration']['success']
    assert not success
