from tests.utils import post_json, put_json, json_response


def test_image_put(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/images/', json_payload)
    assert 'task_id' in response
    assert 'task_status' in response


def test_image_post(client):
    json_payload = {'url': 'http://example.com'}
    response = put_json(client, '/api/images/', json_payload)
    json_payload = {'task_id': response['task_id']}
    response = post_json(client, '/api/images/', json_payload)
    assert 'task_id' in response
    assert 'task_status' in response