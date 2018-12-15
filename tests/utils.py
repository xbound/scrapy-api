import json

CONTENT_TYPE = 'application/json'


def post_json(client, url, json_dict):
    return client.post(
        url, data=json.dumps(json_dict), content_type=CONTENT_TYPE)


def put_json(client, url, json_dict):
    return client.put(
        url, data=json.dumps(json_dict), content_type=CONTENT_TYPE)


def json_response(response):
    return json.loads(response.data.decode('utf8'))
