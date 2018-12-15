from tests.utils import json_response

def test_ping(client):
    response = client.get('api/ping/')
    data = json_response(response)
    assert 'response' in data
    assert data['response'] == 'OK' 
