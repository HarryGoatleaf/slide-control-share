import io

def test_create_presentation(user):
    resp = user.post('/api/presentation/create',
        data={'slides':[(open('./tests/test.pdf', 'rb'),'test.pdf')]})
    data = resp.get_json()
    assert data['status'] == 'success'
    assert data['presentation']['current_slide'] == 1

def test_get_current_presentation(presentation):
    data = presentation.get('/api/presentation/' + str(presentation.presentation_id)).get_json()
    assert data['status'] == 'success'
    assert data['presentation']['id'] == presentation.presentation_id

def test_get_slides(user):
    with open('./tests/test.pdf', 'rb') as file:
        testpdf = file.read()
        # create presentation
        data1 = user.post('/api/presentation/create', data={'slides':[(io.BytesIO(testpdf),'test.pdf')]}).get_json()
        presentation_id = data1['presentation']['id']
        # fetch slides
        resp = user.get('/api/presentation/' + str(presentation_id) + '/slides')
        responsepdf = resp.data
        assert testpdf == responsepdf

def test_get_nonexistent_presentation(user):
    data = user.get('/api/presentation/nonexistent').get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'presentation does not exist'

def test_create_presentation_without_user(client):
    resp = client.post('/api/presentation/create',
        data={'slides':[(open('./tests/test.pdf', 'rb'),'test.pdf')]})
    data = resp.get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'unknown user'

def test_create_presentation_without_slides(user):
    resp = user.post('/api/presentation/create', data = {})
    data = resp.get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'missing slides'

def test_create_presentation_wrong_filetype(user):
    resp = user.post('/api/presentation/create',
        data={'slides':[(open('./tests/test.pdf', 'rb'),'test.txt')]})
    data = resp.get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'only pdfs allowed'

def test_create_corrupted_presentation(user):
    resp = user.post('/api/presentation/create',
        data={'slides':[(open('./tests/corrupted.pdf', 'rb'),'corrupted.pdf')]})
    data = resp.get_json()
    assert data['status'] == 'failed'
    assert data['message'] == 'corrupt pdf'

def test_join_presentation(presentation, second_user):
    data = second_user.get('/api/presentation/' + str(presentation.presentation_id)).get_json()
    assert data['status'] == 'success'
    assert data['presentation']['id'] == presentation.presentation_id

def test_switch_presentation(presentation, second_presentation):
    # switch presentation
    data = second_presentation.get('/api/presentation/'
        + str(presentation.presentation_id)).get_json()
    assert data['status'] == 'success'
    assert presentation.presentation_id == data['presentation']['id']
    assert second_presentation.presentation_id != data['presentation']['id']

def test_get_current_slide(presentation):
    data = presentation.get('/api/presentation/'
        + str(presentation.presentation_id) + '/current_slide').get_json()
    assert data['status'] == 'success'
    assert data['current_slide'] == 1

def test_set_current_slide(presentation):
    data = presentation.post('/api/presentation/'
        + str(presentation.presentation_id) + '/current_slide',
         json={'new_slide': 2}).get_json()
    assert data['status'] == 'success'

def test_set_and_get_current_slide(presentation):
    data = presentation.post('/api/presentation/'
        + str(presentation.presentation_id) + '/current_slide',
         json={'new_slide': 2}).get_json()
    assert data['status'] == 'success'
    data = presentation.get('/api/presentation/'
        + str(presentation.presentation_id) + '/current_slide').get_json()
    assert data['status'] == 'success'
    assert data['current_slide'] == 2