'''
Flask CLI managment scripts. Here you need to write code for Flask scripts.

$ flask <your command here>
'''
import json
import click
from flask.cli import FlaskGroup, with_appcontext
from scrapy_api.api.view import rest_api


@click.command('postman')
@with_appcontext
def postman_api():
    '''
    Generate Swagger api exportable to Postman.
    '''
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = rest_api.as_postman(urlvars=urlvars, swagger=swagger)
    print(json.dumps(data))
