import pytest
import json
from app import app, db 

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def auth_token(client):

    response = client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 201

    
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    return json.loads(response.data)['access_token']

def test_user_registration(client):
    # Test successful registration
    response = client.post('/register', json={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 201
    assert b'User created successfully' in response.data

    # Test registration with an existing username
    response = client.post('/register', json={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 400
    assert b'Username already taken' in response.data



def test_user_login(client):
    response = client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'access_token' in response.data

    response = client.post('/login', json={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 400
    assert b'Invalid credentials' in response.data

def test_protected_resource(client, auth_token):
    response = client.get('/protected', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert b'Hello user' in response.data

def test_protected_resource_without_token(client):
    response = client.get('/protected')
    assert response.status_code == 400
    assert b'Missing Authorization Header' in response.data
