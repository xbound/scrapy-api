'''
Flask CLI managment scripts. Here you need to write code for Flask scripts.

$ flask <your command here>
'''
import json
import click
from flask.cli import FlaskGroup, with_appcontext
from scrapy_api.extensions import api


@click.command('postman')
@with_appcontext
def postman_api():
    '''
    Generate Swagger api exportable to Postman.
    '''
    urlvars = False  # Build query strings in URLs
    swagger = True  # Export Swagger specifications
    data = api.as_postman(urlvars=urlvars, swagger=swagger)
    print(json.dumps(data))
