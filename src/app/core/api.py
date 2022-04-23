from flask import Response, request
from . import functions
from . import constants
import json
import os
from flask_mysqldb import MySQL

request_ =\
  {
    "category": "",
    "title": "",
    "description": ""
  }

default_response = {
    "status": "OK",
    "errmsg": "",
    "error": "",
    "status_code": 200
}


def create_response(response_type: int, msg="", message="", status_code=501) -> dict:
    response_dict = default_response.copy()
    if response_type == constants.RESPONSE_TYPES.OK:
        return response_dict

    if response_type == constants.RESPONSE_TYPES.ERROR or True:
        response_dict["errmsg"] = msg
        response_dict["error"] = message
        response_dict["status_code"] = status_code
        return response_dict


def upload(user_request: request, mysql_conn: MySQL) -> Response:
    response_to_user = Response()
    response_to_user.content_type = "application/json"

    for image in user_request.files.getlist("pictures"):
        uuid = functions.create_image_uuid(image)

        if not uuid:
            response_dict = create_response(
              constants.RESPONSE_TYPES.ERROR, "not_enough_uuids", "There are not enough UUIDS for images.", 507)
            response_to_user.status_code = response_dict["status_code"]
            response_to_user.data = json.dumps(response_dict)
            return response_to_user

        uuid_path = os.path.join(constants.IMAGE_FOLDER_PATH, uuid)

        with open(uuid_path, "wb") as img:
            img.write(image.stream.read())

    cursor = mysql_conn.connection.cursor()
    cursor.execute("""INSERT INTO users(username, name, surname, email, password) VALUE ('jefinko', 'Jozef', 'Sabo', 'jjj@jj.sk', 'emailo')""")
    mysql_conn.connection.commit()
    cursor.close()

    return response_to_user
