import pytest
from backend import create_app, db
import socketio

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def second_client(app):
    return app.test_client()

@pytest.fixture
def user(client):
    client.post('/api/user/name',json = {'username': 'pytest'})
    return client

@pytest.fixture
def second_user(second_client):
    second_client.post('/api/user/name',json = {'username': 'second_pytest'})
    return second_client

@pytest.fixture
def presentation(user):
    data = user.post('/api/presentation/create',
        data={'slides':[(open('./tests/test.pdf', 'rb'),'test.pdf')]}).get_json()
    user.presentation_id = data['presentation']['id']
    return user

@pytest.fixture
def second_presentation(second_user):
    data = second_user.post('/api/presentation/create',
        data={'slides':[(open('./tests/test.pdf', 'rb'),'test.pdf')]}).get_json()
    second_user.presentation_id = data['presentation']['id']
    return second_user