"""Unit testing for Flask API files"""
from app import app

def test_admin_adque():
    """Tests adoption_queue from admin.py"""
    response = app.test_client().get('/api/adoption-queue')

    assert {
        'petID': 102,
        'pet_name': 'John',
        'pet_species': 'Cat',
        'requestID': 102,
        'submit_time': '2024-11-19 19:06',
        'userID': 100,
        'user_full_name':
        'John Marks'
    } in response.json

def test_admin_aq():
    """Tests approve_questionnaire from admin.py"""
    response = app.test_client().post('/api/approve-questionnaire/1')
    response_data = response.data.decode()

    assert response_data == '{"success": true}'

def test_admin_dq():
    """Tests deny_questionnaire from admin.py"""
    response = app.test_client().post('/api/deny-questionnaire/1')
    response_data = response.data.decode()

    assert response_data == '{"success": true}'

def test_user_postnoti():
    """Tests post_notification in user.py"""
    response = app.test_client().post('/api/notifications/100',
                        json={"message": "Questionnaire approved"})
    response_data = response.data.decode()

    assert response_data == '{"success": true}'

def test_user_getquest():
    """Tests get_questionnaire in user.py"""
    response = app.test_client().get('/api/questionnaire')
    response_data = response.data.decode()

    target = '["Do you prefer cats or dogs?", "Why do you want to adopt a pet?"]'
    assert response_data == target

def test_user_postquest():
    """Tests post_questionnaire in user.py"""
    response = app.test_client().post('/api/send-answer',
        json={"question": "Do you prefer dogs or cats?", "response": "cats",
              "comment": "N/A", "user_id": 100})
    response_data = response.data.decode()

    assert response_data == '{"success": true}'

def test_admin_quque():
    """Tests questionnaire_queue from admin.py"""
    response = app.test_client().get('/api/questionnaire-queue')
    assert {'questionnaireID': 100, 'userID': 100, 'user_full_name': 'John Marks'} in response.json

def test_admin_viewquestion():
    """Tests view_user_questionnaire from admin.py"""
    response = app.test_client().get('/api/questionnaire/100')
    response_data = " ".join(response.data.decode().split())

    assert '{"question":"Do you prefer dogs or cats?","response":"cats"}' in response_data

def test_user_getnotis():
    """Tests get_notifications from user.py"""
    response = app.test_client().get('/api/notifications/100')
    response_data = " ".join(response.data.decode().split())

    assert '"message":"Questionnaire approved"' in response_data

def test_user_readnoti():
    """Tests read_notification from user.py"""
    response = app.test_client().put('/api/notifications/read/1')
    response_data = " ".join(response.data.decode().split())

    assert response_data == '{"success": true}'

def test_pets_appr_adreq():
    """Tests approve_adoption_req from pets.py"""
    response = app.test_client().post('/api/admin/approve-adoption/101/100/100')
    response_data = " ".join(response.data.decode().split())

    assert response_data == '{"success": true}'

def test_pets_deny_adreq():
    """Tests deny_adoption_req from pets.py"""
    response = app.test_client().post('/api/admin/deny-adoption/101/100/101')
    response_data = " ".join(response.data.decode().split())

    assert response_data == '{"success": true}'

def test_pets_req_adoption():
    """Tests request_adoption from pets.py"""
    response = app.test_client().post('/api/request-adoption/100/102')
    response_data = " ".join(response.data.decode().split())

    assert response_data == '{"success": true}'

def test_pets_getpets():
    """Tests pets() from pets.py"""
    response = app.test_client().get('/api/pets')
    response_data = " ".join(response.data.decode().split())

    assert " ".join('{"description":"Senior cat. Spends most of his time'.split()) in response_data

def test_pets_unreq_adoption():
    """Tests unrequest_adoption from pets.py"""
    response = app.test_client().post('/api/unrequest-adoption/100/102')
    response_data = " ".join(response.data.decode().split())

    assert response_data == '{"success": true}'
