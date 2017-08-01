import logging
from urllib.parse import unquote
import requests
import re

# Not ideal
# If we get rid of the requirement for the API to be
# able to see the file system this API can run on a host
# with significantly fewer permissions
from os import listdir
from os.path import join

from flask import Blueprint, jsonify, Response
from flask_restful import Resource, Api, reqparse

from .lib import OCRBuilder

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


def get_volumes(identifier):
    if not re.match("^mvol-[0-9]{4}$", identifier):
        raise ValueError("bad identifier")
    path_parts = identifier.split("-")
    path = join(
        BLUEPRINT.config['MVOL_ROOT'],
        *path_parts
    )
    volume_identifiers = []
    for x in listdir(path):
        volume_identifiers.append(identifier+"-"+x)

    # Filter
    volume_identifiers = [x for x in volume_identifiers if
                          re.match("^mvol-[0-9]{4}-[0-9]{4}$", x)]

    return sorted(volume_identifiers, key=lambda page: int(page[11:]))


def get_issues(identifier):
    if not re.match("^mvol-[0-9]{4}-[0-9]{4}$", identifier):
        raise ValueError("bad identifier")
    path_parts = identifier.split("-")
    path = join(
        BLUEPRINT.config['MVOL_ROOT'],
        *path_parts
    )
    issue_identifiers = []
    for x in listdir(path):
        issue_identifiers.append(identifier+"-"+x)

    # Filter
    issue_identifiers = [x for x in issue_identifiers if
                         re.match("^mvol-[0-9]{4}-[0-9]{4}-[0-9]{4}$", x)]

    return sorted(issue_identifiers, key=lambda page: int(page[16:]))


def get_pages(identifier):
    if not re.match("^mvol-[0-9]{4}-[0-9]{4}-[0-9]{4}$", identifier):
        raise ValueError("bad identifier")
    path_parts = identifier.split("-")
    path = join(
        BLUEPRINT.config['MVOL_ROOT'],
        *path_parts,
        "TIFF"
    )
    page_identifiers = []
    for x in listdir(path):
        page_identifiers.append(
            identifier+"_{}".format(x.split("_")[1][:-4])
        )

    # Filter
    page_identifiers = [x for x in page_identifiers if
                        re.match("^mvol-[0-9]{4}-[0-9]{4}-[0-9]{4}_[0-9]{4}$", x)]

    return sorted(page_identifiers, key=lambda page: int(page[21:]))


def response_200(r):
    if not r.status_code == 200:
        raise ValueError()


class Root(Resource):
    def get(self):
        return {"Status": "Not broken!"}


class Nav(Resource):
    def get(self, identifier):
        result = {}
        result['self'] = unquote(identifier)
        for x in get_pages, get_issues, get_volumes:
            try:
                result['children'] = x(unquote(identifier))
            except ValueError:
                pass
        if 'children' not in result:
            raise Error("Unrecognized Identifier!")
        return result


class OCR(Resource):
    def get(self, identifier):
        parser = reqparse.RequestParser()
        parser.add_argument('jpg_width', type=int, required=True)
        parser.add_argument('jpg_height', type=int, required=True)
        args = parser.parse_args()

        # Grab the dc
        dc_request = requests.get(
            BLUEPRINT.config['RETRIEVER_URL'] + unquote(identifier) + "/metadata"
        )
        response_200(dc_request)
        dc_str = dc_request.text

        # Get the struct
        # TODO
        pass

        # Determine what identifiers are in this issue
        pages = get_pages(unquote(identifier))

        # Create an array to hold the dicts of information per page
        info_dicts = []
        # Build the info dicts
        for page_id in pages:
            info_dict = {}
            tif_techmd_request = requests.get(
               "{}{}/tif/technical_metadata".format(BLUEPRINT.config['RETRIEVER_URL'], page_id)
            )
            response_200(tif_techmd_request)
            tif_techmd_json = tif_techmd_request.json()

            alto_request = requests.get(
                "{}{}/ocr/limb".format(BLUEPRINT.config['RETRIEVER_URL'], page_id)
            )
            response_200(alto_request)
            alto_str = alto_request.text

            width, height = tif_techmd_json['width'], tif_techmd_json['height']
            info_dict['identifier'] = page_id
            info_dict['tif_width'] = width
            info_dict['tif_height'] = height
            info_dict['jpg_width'] = args['jpg_width']
            info_dict['jpg_height'] = args['jpg_height']
            info_dict['alto'] = alto_str
            info_dict['struct_page'] = None  # TODO
            info_dict['struct_milestone'] = None  # TODO

            # Drop it in the bucket
            info_dicts.append(info_dict)

        builder = OCRBuilder(
            dc_str,
            info_dicts
        )

        return Response(builder.get_xtf_converted_book(), mimetype="text/xml")


@BLUEPRINT.record
def handle_configs(setup_state):
    app = setup_state.app
    BLUEPRINT.config.update(app.config)
    if BLUEPRINT.config.get('DEFER_CONFIG'):
        log.debug("DEFER_CONFIG set, skipping configuration")
        return

    if BLUEPRINT.config['RETRIEVER_URL'][-1] is not "/":
        BLUEPRINT.config['RETRIEVER_URL'] = BLUEPRINT.config['RETRIEVER_URL'] + "/"

    if BLUEPRINT.config.get("VERBOSITY"):
        log.debug("Setting verbosity to {}".format(str(BLUEPRINT.config['VERBOSITY'])))
        logging.basicConfig(level=BLUEPRINT.config['VERBOSITY'])
    else:
        log.debug("No verbosity option set, defaulting to WARN")
        logging.basicConfig(level="WARN")


API.add_resource(Root, "/")
API.add_resource(Nav, "/<path:identifier>/nav")
API.add_resource(OCR, "/<path:identifier>/ocr")
