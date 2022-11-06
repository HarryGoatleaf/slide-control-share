def test_create_user(client):
    resp = client.post('/api/user/name',json = {'username': 'pytest'})
    data = resp.get_json()
    assert data['status'] == "success"
    assert data['user']['name'] == "pytest"

def test_create_malformed_user(client):
    resp = client.post('/api/user/name', json = {})
    data = resp.get_json()
    assert data['status'] == "failed"
    assert data['message'] == "malformed"

def test_get_name(user):
    resp = user.get('/api/user/name')
    data = resp.get_json()
    assert data['status'] == "success"
    assert data['user']['name'] == "pytest"

def test_get_unregistered_user(client):
    resp = client.get('/api/user/name')
    data = resp.get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'unknown user'

def test_already_registered_user(user):
    resp = user.post('/api/user/name',json = {'username': 'pytest2'})
    data = resp.get_json()
    assert data['status'] == "failed"
    assert data['message'] == "already registered"

def test_two_clients(user, second_client):
    resp = second_client.get('/api/user/name')
    data = resp.get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'unknown user'
    resp = user.get('/api/user/name')
    data = resp.get_json()
    assert data['status'] == "success"
    assert data['user']['name'] == "pytest"