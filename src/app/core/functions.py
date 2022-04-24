from flask import Response
import random
from . import constants
import os
import json


def create_image_uuid(image, with_check=True) -> str:
    tries = 1
    if with_check:
        tries = constants.UUID_CREATION_TRIES

    uuid = ""
    has_name = False
    for _ in range(tries):
        uuid = ""
        for __ in range(constants.IMAGE_UUID_LENGTH):
            random_integer = random.randint(0, len(constants.UUID_CHARACTERS) - 1)
            uuid += (constants.UUID_CHARACTERS[random_integer])

        uuid += "." + image.mimetype.split("/")[-1]

        if with_check:
            path = os.path.join(constants.IMAGE_FOLDER_PATH, uuid)
            if not os.path.isfile(path):
                has_name = True

    if with_check and not has_name:
        return ""
    # TODO: upload to folder with actual year

    return uuid


def create_response(response_type: int, msg="", message="", status_code=501) -> dict:
    response_dict = constants.DEFAULT_RESPONSE.copy()
    if response_type == constants.RESPONSE_TYPES.OK:
        return response_dict

    if response_type == constants.RESPONSE_TYPES.ERROR or True:
        response_dict["status"] = "error"
        response_dict["errmsg"] = msg
        response_dict["error"] = message
        response_dict["status_code"] = status_code
        return response_dict


def respond(response_dict: dict) -> Response:
    response_to_user = Response()
    response_to_user.content_type = "application/json"
    response_to_user.status_code = response_dict["status_code"]
    response_to_user.data = json.dumps(response_dict)
    return response_to_user
