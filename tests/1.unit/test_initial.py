def test_ping(client):
    response = client.get('/')
    assert response.status_code == 200