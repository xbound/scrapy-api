'''
Flask CLI managment scripts. Here you need to write code for Flask scripts.

$ flask <your command here>
'''

import click
from flask.cli import FlaskGroup, with_appcontext
from flask import current_app

@click.command('postman')
@with_appcontext
def postman_api():
    '''
    Generate Swagger api exportable to Postman.
    '''
    import pdb; pdb.set_trace()
    print('Test')

