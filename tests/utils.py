import json

CONTENT_TYPE = 'application/json'


def get_json(client, url, json_dict):
    return client.get(url, data=json_dict)

def post_json(client, url, json_dict):
    return client.post(
        url, data=json.dumps(json_dict), content_type=CONTENT_TYPE)


def put_json(client, url, json_dict):
    return client.put(
        url, data=json.dumps(json_dict), content_type=CONTENT_TYPE)


