import logging
from urllib.parse import unquote

from flask import Blueprint, jsonify, send_file
from flask_restful import Resource, Api, reqparse

BLUEPRINT = Blueprint('mvol_api', __name__)

BLUEPRINT.config = {}

API = Api(BLUEPRINT)

log = logging.getLogger(__name__)



class Error(Exception):
    err_name = "Error"
    status_code = 500
    message = ""

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def to_dict(self):
        return {"message": self.message,
                "error_name": self.err_name}


@BLUEPRINT.errorhandler(Error)
def handle_errors(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


class Root(Resource):
    def get(self):
        return {"Status": "Not broken!"}


class Struct(Resource):
    def get(self, identifier):
        return {}


class OCR(Resource):
    def get(self, identifier):
        return {}


@BLUEPRINT.record
def handle_configs(setup_state):
    app = setup_state.app
    BLUEPRINT.config.update(app.config)
    if BLUEPRINT.config.get('DEFER_CONFIG'):
        log.debug("DEFER_CONFIG set, skipping configuration")
        return

    if BLUEPRINT.config.get("VERBOSITY"):
        log.debug("Setting verbosity to {}".format(str(BLUEPRINT.config['VERBOSITY'])))
        logging.basicConfig(level=BLUEPRINT.config['VERBOSITY'])
    else:
        log.debug("No verbosity option set, defaulting to WARN")
        logging.basicConfig(level="WARN")


API.add_resource(Root, "/")
API.add_resource(Struct, "/<path:identifier>/struct")
API.add_resource(OCR, "/<path:identifier>/ocr")
