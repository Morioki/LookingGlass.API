from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)


def test_genre_all(client):
    json = {"query":"query getGenres{\n  genres {\n    id\n  }\n}","operationName":"getGenres"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['genres']
    assert len(data) > 0 and data[0]['id'] == str(1)

def test_genre_specific(client):
    json = {"query":"query getGenre{\n  genre(genreId: 1) {\n    id\n  }\n}","operationName":"getGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['genre']
    assert data['id'] == str(1)

def test_genre_specific_failure(client):
    json = {"query":"query getGenre{\n  genre(genreId: 9999999999) {\n    id\n  }\n}","operationName":"getGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['genre']
    assert data is None # TODO look to see if there is a way to output an error

def test_genre_insert(client):
    query = "mutation genre{\n  insertGenre(description: \"Test Record To Insert\", active: false) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"genre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertGenre']['success']
    ValueStorage.genre_id = int(response.json['data']['insertGenre']['id'])
    assert success

def test_genre_insert_failure(client):
    query = "mutation genre{\n  insertGenre(description: \"Test Record To Insert\", parentId: 99999999,active: false) {\n    success\n    id\n  }\n}"
    json = {"query": query,"operationName":"genre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertGenre']['success']
    assert not success

def test_genre_update(client):
    assert ValueStorage.genre_id is not None
    query = "mutation genre{\n  updateGenre(genreId: " + str(ValueStorage.genre_id) + ", description: \"Testing Update\") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"genre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateGenre']['success']
    assert success

def test_genre_update_failure(client):
    assert ValueStorage.genre_id is not None
    query = "mutation genre{\n  updateGenre(genreId: " + str(ValueStorage.genre_id) + ") {\n    success\n  }\n}"
    json = {"query": query,"operationName":"genre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateGenre']['success']
    assert not success

def test_genre_delete(client):
    assert ValueStorage.genre_id is not None
    query = "mutation genre{\n  deleteGenre(genreId: " + str(ValueStorage.genre_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"genre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteGenre']['success']
    assert success

def test_genre_delete_failure(client):
    assert ValueStorage.genre_id is not None
    query = "mutation genre{\n  deleteGenre(genreId: " + str(ValueStorage.genre_id) + ") {\n    success\n  }\n}"
    json = {"query": query ,"operationName":"genre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteGenre']['success']
    assert not success
