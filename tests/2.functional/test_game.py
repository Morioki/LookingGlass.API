from api.helpers import random_string_generator
from tests.conftest import ValueStorage

name = random_string_generator(20)

def test_game_all(client):
    json = {"query":"query getGames{\n  games {\n    id\n    name\n    releaseyear\n    platforms {\n      platformcode\n    }\n    genres {\n      description\n    }\n    developer\n    publisher\n    mainseries\n    subseries\n    notes\n    entrydate\n  }\n}","operationName":"getGames"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['games']
    assert len(data) > 0 and data[0]['id'] == str(1)

# TODO Find way to trigger all exception

def test_game_specific(client):
    json = {"query":"query getGame{\n  game(gameId: 1) {\n    name\n    id\n  }\n}","operationName":"getGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['game']
    assert data['id'] == str(1)

def test_game_specific_failure(client):
    json = {"query":"query getGame{\n  game(gameId: 99999999) {\n    name\n    id\n  }\n}","operationName":"getGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    data = response.json['data']['game']
    assert data is None # TODO look to see if there is a way to output an error

def test_game_insert(client):
    query = "mutation insertGame {\n  insertGame(name: " + f"\"{name}\" " + ", releaseYear: 2021) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"insertGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['insertGame']['success']
    ValueStorage.game_id = int(response.json['data']['insertGame']['id'])
    assert success

def test_game_insert_failure(client):
    # name = random_string_generator(20)
    query = "mutation insertGame {\n  insertGame(name: " + f"\"{name}\" " + ", releaseYear: 2021) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"insertGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    # print(response.json['data'])
    success = response.json['data']['insertGame']['success']
    assert not success

def test_game_update(client):
    assert ValueStorage.game_id is not None
    query = "mutation updateGame {\n  updateGame(gameId: " + str(ValueStorage.game_id) + ", developer:\"test\") {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"updateGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateGame']['success']
    assert success

def test_game_update_failure(client):
    assert ValueStorage.game_id is not None
    query = "mutation updateGame {\n  updateGame(gameId: " + str(ValueStorage.game_id) + ", developer:\"test\") {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"updateGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['updateGame']['success']
    assert not success

def test_game_append_genre(client):
    assert ValueStorage.game_id is not None
    query = "mutation appendGenre {\n  appendGenreToGame(gameId: " + str(ValueStorage.game_id) + ", genreId: 1) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"appendGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['appendGenreToGame']['success']
    assert success

def test_game_append_genre2(client):
    assert ValueStorage.game_id is not None
    query = "mutation appendGenre {\n  appendGenreToGame(gameId: " + str(ValueStorage.game_id) + ", genreId: 2) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"appendGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['appendGenreToGame']['success']
    assert success

def test_game_append_genre_failure(client):
    assert ValueStorage.game_id is not None
    query = "mutation appendGenre {\n  appendGenreToGame(gameId: " + str(ValueStorage.game_id) + ", genreId: 999999) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"appendGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['appendGenreToGame']['success']
    assert not success

def test_game_remove_genre(client):
    assert ValueStorage.game_id is not None
    query = "mutation removeGenre {\n  removeGenreFromGame(gameId: " + str(ValueStorage.game_id) + ", genreId: 1) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"removeGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['removeGenreFromGame']['success']
    assert success

def test_game_remove_genre_failure(client):
    assert ValueStorage.game_id is not None
    query = "mutation removeGenre {\n  removeGenreFromGame(gameId: " + str(ValueStorage.game_id) + ", genreId: 9999999) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"removeGenre"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['removeGenreFromGame']['success']
    assert not success

def test_game_append_platform(client):
    assert ValueStorage.game_id is not None
    query = "mutation appendPlatform {\n  appendPlatformToGame(gameId: " + str(ValueStorage.game_id) + ", platformId: 1) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"appendPlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['appendPlatformToGame']['success']
    assert success

def test_game_append_platform2(client):
    assert ValueStorage.game_id is not None
    query = "mutation appendPlatform {\n  appendPlatformToGame(gameId: " + str(ValueStorage.game_id) + ", platformId: 2) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"appendPlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['appendPlatformToGame']['success']
    assert success

def test_game_append_platform_failure(client):
    assert ValueStorage.game_id is not None
    query = "mutation appendPlatform {\n  appendPlatformToGame(gameId: " + str(ValueStorage.game_id) + ", platformId: 999999) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"appendPlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['appendPlatformToGame']['success']
    assert not success

def test_game_remove_platform(client):
    assert ValueStorage.game_id is not None
    query = "mutation removePlatform {\n  removePlatformFromGame(gameId: " + str(ValueStorage.game_id) + ", platformId: 1) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"removePlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['removePlatformFromGame']['success']
    assert success

def test_game_remove_platform_failure(client):
    assert ValueStorage.game_id is not None
    query = "mutation removePlatform {\n  removePlatformFromGame(gameId: " + str(ValueStorage.game_id) + ", platformId: 9999999) {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"removePlatform"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['removePlatformFromGame']['success']
    assert not success
 
def test_game_delete(client):
    assert ValueStorage.game_id is not None
    query = "mutation deleteGame {\n  deleteGame(gameId: " + str(ValueStorage.game_id) + ") {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"deleteGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteGame']['success']
    assert success

def test_game_delete_failure(client):
    assert ValueStorage.game_id is not None
    query = "mutation deleteGame {\n  deleteGame(gameId: " + str(ValueStorage.game_id) + ") {\n    success\n    errors\n    field\n    id\n  }\n}"
    json = {"query": query,"operationName":"deleteGame"}
    response = client.post('/graphql', headers=ValueStorage.headers, json=json)
    success = response.json['data']['deleteGame']['success']
    assert not success