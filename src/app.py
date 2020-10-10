import os
import json
import logging
from pathlib import Path
from http import HTTPStatus
from flask import Flask, request, Response
from werkzeug.serving import run_simple


APP_NAME = "Flask Boilerplate"
ROOT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VERSION_PATH = Path(ROOT_PATH, 'VERSION')


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.logger.info('Starting {}...'.format(APP_NAME))


def log_endpoint_call(endpoint):
    app.logger.info('{} called'.format(endpoint))


def log_http_response(code, payload):
    payload = {'payload': payload}
    if code == HTTPStatus.OK:
        app.logger.info(payload)
    elif code == HTTPStatus.BAD_REQUEST:
        app.logger.warning(payload)
    elif code == HTTPStatus.INTERNAL_SERVER_ERROR:
        app.logger.error(payload, exc_info=True)


def create_http_response(code=HTTPStatus.OK, payload=None):
    payload = payload or {}
    log_http_response(code, payload)
    return Response(json.dumps(payload), status=code, mimetype='application/json')


def read_version():
    with VERSION_PATH.open('rt') as f:
        version = f.read()
    return version


@app.route('/', methods=['GET'])
def hello_endpoint():
    log_endpoint_call(request.path)
    return create_http_response(payload='Hello world, I am {}!'.format(APP_NAME))


@app.route('/version', methods=['GET'])
def version_endpoint():
    log_endpoint_call(request.path)
    return create_http_response(payload=read_version())


# See https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/#starting-your-app-with-uwsgi for uwsgi instructions
# Production Command: uwsgi --ini uwsgi.ini
# Development Command: python3 app.py
# Main only gets called if Development Command is used
if __name__ == '__main__':
    run_simple('localhost', 5000, app, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
