from tests.utils import json_response

def test_ping(client):
    response = json_response(client.get('api/ping/'))
    assert 'message' in response
    assert response['message'] == 'OK' 
