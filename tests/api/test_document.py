from tests.utils import post_json, put_json, json_response


def test_document_put(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/document/', json_payload)
    data = json_response(response)
    assert 'task_id' in data
    assert 'task_status' in data


def test_document_post(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/document/', json_payload)
    data = json_response(response)
    json_payload = {'task_id': data['task_id']}
    response = post_json(client, '/api/document/', json_payload)
    assert 'task_id' in data
    assert 'task_status' in data