from flask import Response
import random
from . import constants
import os
import json
from PIL import Image
import mysql.connector


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


def create_response(response_type: int, errmsg="", error="", message="", status_code=501) -> dict:
    response_dict = constants.DEFAULT_RESPONSE.copy()
    if response_type == constants.RESPONSE_TYPES.OK:
        response_dict["message"] = message
        return response_dict

    if response_type == constants.RESPONSE_TYPES.ERROR or True:
        response_dict["status"] = "error"
        response_dict["errmsg"] = errmsg
        response_dict["error"] = error
        response_dict["status_code"] = status_code
        return response_dict


def respond(response_dict: dict) -> Response:
    response_to_user = Response()
    response_to_user.content_type = "application/json"
    response_to_user.status_code = response_dict["status_code"]
    response_to_user.data = json.dumps(response_dict)
    return response_to_user


def optimize_images(url: str, photo_id: str) -> None:
    directory = os.path.dirname(url)
    file = os.path.basename(url)
    mysql_conn = mysql.connector.connect(
        user=constants.DB_USER,
        password=constants.DB_PASSWORD,
        host=constants.DB_HOST,
        database=constants.DB_DATABASE,
        port=constants.DB_PORT)

    image = Image.open(url)
    max_width = 0
    for width in constants.WIDTH_BREAKPOINTS:
        if image.size[0] >= width:
            max_width = width
            width_percent = (width / float(image.size[0]))
            height = int((float(image.size[1]) * float(width_percent)))
            img = image.copy()
            img = img.resize((width, height), Image.ANTIALIAS)
            img.save(os.path.join(directory, str(width) + "_" + file))

    cursor = mysql_conn.cursor()
    cursor.execute(f"UPDATE photos SET max_width = '{max_width}' WHERE id='{photo_id}';")
    mysql_conn.commit()
    cursor.close()
    mysql_conn.close()
