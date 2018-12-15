from flask_restplus import Namespace, Resource

api = Namespace(
    'ping', description='Ping endpoint for checking service availability.')


@api.route('/')
class PingAPI(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'response': 'OK'}, 200
