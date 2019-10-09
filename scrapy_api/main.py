from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields, Namespace
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

blueprint = Blueprint('api', __name__)
api = Api(
    blueprint,
    version='1.0',
    title='Todo API',
    description='A simple TODO API',
)

ns = Namespace('todos', description='TODO operations')

TODOS = {
    'todo1': {
        'task': 'build an API'
    },
    'todo2': {
        'task': '?????'
    },
    'todo3': {
        'task': 'profit!'
    },
}

todo = api.model(
    'Todo',
    {'task': fields.String(required=True, description='The task details')})

listed_todo = api.model(
    'ListedTodo', {
        'id': fields.String(required=True, description='The todo ID'),
        'todo': fields.Nested(todo, description='The Todo')
    })


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))


parser = api.parser()
parser.add_argument('task',
                    type=str,
                    required=True,
                    help='The task details',
                    location='form')


@ns.route('/<string:todo_id>')
# @api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc(description='todo_id should be in {0}'.format(', '.join(
        TODOS.keys())))
    @ns.marshal_with(todo)
    def get(self, todo_id):
        '''Fetch a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @ns.doc(responses={204: 'Todo deleted'})
    def delete(self, todo_id):
        '''Delete a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @ns.doc(parser=parser)
    @ns.marshal_with(todo)
    def put(self, todo_id):
        '''Update a given resource'''
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.marshal_list_with(listed_todo)
    def get(self):
        '''List all todos'''
        return [{'id': id, 'todo': todo} for id, todo in TODOS.items()]

    @ns.doc(parser=parser)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a todo'''
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


api.add_namespace(ns)

app.register_blueprint(blueprint, url_prefix='/api/')

if __name__ == '__main__':
    app.run(debug=True)
