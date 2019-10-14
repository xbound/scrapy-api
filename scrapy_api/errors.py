'''
Module where all application exceptions are declared. Here you need to write code intended for use inside error handlers.
'''
from typing import Union
from flask_restplus import Api, Namespace, Model, fields


class APIError(Exception):
    '''
    Base API Error class. All app exceptions inherit from this class
    '''
    description = 'Internal failure'
    message = 'Internal server error'
    code = 'INTERNAL-ERROR'
    http_code = 500


class TaskDoesNotExist(APIError):
    '''
    Exception which is raised when endpoint
    recieves task_id of none existing task. 
    '''
    description = 'None existing task refrenced'
    message = 'Task with given id does not exist'
    code = 'INVALID-TASK-ID'
    http_code = 404


class Error404(APIError):
    '''
    Exception which is raised when unknown resource was requested.
    '''
    description = 'Unknown resource requested'
    message = 'Requested resource was not found'
    code = '404-NOT-FOUND'
    http_code = 404


class TaskNotProvided(APIError):
    '''
    Exception which is raised when unknown resource was requested.
    '''
    description = 'No task provided'
    message = 'Requested resource was not found'
    code = '400-NO-TASK'
    http_code = 400


# Type annotation for error object inside
# make_error_response function
ErrorType = Union[Exception, APIError]
NamespaceType = Union[Api, Namespace]


def make_error_response(error: ErrorType):
    '''Create JSON error response from exception
    object.

    :param error: exception object
    :return: dictionary with error response
    '''
    if not isinstance(error, APIError):
        error = APIError()
    return {
        'message': error.message,
        'code': error.code,
    }, error.http_code


def error_to_swagger(ns: NamespaceType, error: APIError):
    '''Generates Swagger model for endpoint from 
    ErroType object.

    :param ns: Flask-RESTPlus Namspace
    :param error: ErrorType object
    '''
    return ns.model(error.description, {
        'message': fields.String(example=error.message),
        'code': fields.String(example=error.code),
    })
