import time
from tests.utils import post_json, put_json, json_response


def test_document_put(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/documents/', json_payload)
    assert 'task_id' in response
    assert 'task_status' in response


def test_document_post(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/documents/', json_payload)
    json_payload = {'task_id': response['task_id']}
    response = post_json(client, '/api/documents/', json_payload)
    assert 'task_id' in response
    assert 'task_status' in response


def test_document_get(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/documents/', json_payload)
    json_payload = {'task_id': response['task_id']}
    response = post_json(client, '/api/documents/', json_payload)
    while response['task_status'] != 'SUCCESS':
        response = post_json(client, '/api/documents/', json_payload)
        time.sleep(1)
    response = json_response(
        client.get('/api/documents/{}'.format(response['task_id'])))
    assert response['text'] != None
    assert response['status_code'] != None
