from flask_restplus import Namespace, Resource

ping_namespace = Namespace(
    'ping', description='Endpoint for checking service availability.')


@ping_namespace.route('/ping')
class PingAPI(Resource):
    '''
    Ping endpoint.
    '''

    def get(self):
        return {'message': 'OK'}
