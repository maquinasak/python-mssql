import pytest

from app import app


@pytest.fixture(autouse=True)
def client():
    print("\nejecuto client")
    app.testing = True
    global client
    client = app.test_client()
    # return client
    yield
    print("\nteardonw fixture client")

def setup_module(module):
    print("\ninicio modulo")

def teardown_module(module):
    print("\nsaliendo del modulo")

def test_get_usuarios():
    response = client.get('/usuarios', json={})
    json_data = response.json
    assert response.status_code == 200
    assert json_data["rta"] == 'ok'

def test_get_usuarios_uno():
    emails = ["akouvach@gmail.com","akouvach@yahoo.com"]
    for valor in enumerate(emails):
        response = client.get(f"/usuarios/{valor}", json={})
        json_data = response.json
        assert response.status_code == 200 or response.status_code == 404
        assert json_data["rta"] == 'ok'

