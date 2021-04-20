from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_platform_all(client):
    json = {"query":"query getPlatforms{\n  platforms {\n    id\n  }\n}","operationName":"getPlatforms"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['platforms']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_platform_specific(client):
    json = {"query":"query getPlatform{\n  platform(platformId: 1) {\n    id\n  }\n}","operationName":"getPlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['platform']
    assert data['id'] == str(1)

def test_platform_specific_failure(client):
    json = {"query":"query getPlatform{\n  platform(platformId: 999999999) {\n    id\n  }\n}","operationName":"getPlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['platform']
    assert data is None # TODO look to see if there is a way to output an error

def test_platform_insert(client):
    query = "mutation platform{\n  insertPlatform(generationId: 1, platformcode:\"TST\" description: \"Test Record To Insert\", handheld:false, active: false) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"platform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertPlatform']['success']
    ValueStorage.platform_id = int(response.json['data']['insertPlatform']['id'])
    assert success

def test_platform_insert_failure(client):
    query = "mutation platform{\n  insertPlatform(generationId: 9999999999, platformcode:\"TST\" description: \"Test Record To Insert\", handheld:false, active: false) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"platform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertPlatform']['success']
    assert not success

def test_platform_update(client):
    assert ValueStorage.platform_id is not None
    query = "mutation platform{\n  updatePlatform(platformId: " + str(ValueStorage.platform_id) + ", description: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"platform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlatform']['success']
    assert success

def test_platform_update_failure(client):
    assert ValueStorage.platform_id is not None
    query = "mutation platform{\n  updatePlatform(platformId: " + str(ValueStorage.platform_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"platform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updatePlatform']['success']
    assert not success

def test_platform_delete(client):
    assert ValueStorage.platform_id is not None
    query = "mutation platform{\n  deletePlatform(platformId: " + str(ValueStorage.platform_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"platform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlatform']['success']
    assert success

def test_platform_delete_failure(client):
    assert ValueStorage.platform_id is not None
    query = "mutation platform{\n  deletePlatform(platformId: " + str(ValueStorage.platform_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"platform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deletePlatform']['success']
    assert not success
