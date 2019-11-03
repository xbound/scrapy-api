import json

CONTENT_TYPE = 'application/json'


def json_response(response) -> dict:
    return json.loads(response.data.decode('utf8'))


def post_json(client, url, json_dict) -> dict:
    response = client.post(url,
                           data=json.dumps(json_dict),
                           content_type=CONTENT_TYPE)
    return json_response(response)


def put_json(client, url, json_dict) -> dict:
    response = client.put(url,
                          data=json.dumps(json_dict),
                          content_type=CONTENT_TYPE)
    return json_response(response)
