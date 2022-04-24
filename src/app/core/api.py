from flask import Response, request
from . import functions
from . import constants
import json
import os
from flask_mysqldb import MySQL

# temporarily
USER_ID = 1

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


def upload(user_request: request, mysql_conn: MySQL) -> Response:
    title = mysql_conn.connection.escape_string(user_request.form.get("title")).decode("utf-8")[:40]
    description = mysql_conn.connection.escape_string(user_request.form.get("description")).decode("utf-8")
    category = mysql_conn.connection.escape_string(user_request.form.get("category")).decode("utf-8")

    category_id = -1
    category_id = constants.POST_CATEGORIES.NEWCOMERS if category == "newcomers" else category_id
    category_id = constants.POST_CATEGORIES.NEW_PROJECTS if category == "projects" else category_id
    category_id = constants.POST_CATEGORIES.TOURNAMENTS if category == "tournaments" else category_id
    category_id = constants.POST_CATEGORIES.SPORT_CHALLENGES if category == "sport" else category_id
    category_id = constants.POST_CATEGORIES.OTHER_EVENTS if category == "other" else category_id

    if category_id == -1:
        response_dict = create_response(constants.RESPONSE_TYPES.ERROR, "category_not_set", "Post category was not set.", 400)
        return respond(response_dict)

    cursor = mysql_conn.connection.cursor()

    cursor.execute(f"INSERT INTO posts(user_id, category_id, title, description) VALUES ('{USER_ID}', '{category_id}', '{title}', '{description}');")
    mysql_conn.connection.commit()

    cursor.execute(f"SELECT id FROM posts WHERE user_id='{USER_ID}' AND title='{title}' ORDER BY id DESC LIMIT 1;")
    post_id = cursor.fetchall()[0][0]

    for image in user_request.files.getlist("pictures"):
        uuid = functions.create_image_uuid(image)

        if not uuid:
            response_dict = create_response(
              constants.RESPONSE_TYPES.ERROR, "not_enough_uuids", "There are not enough UUIDS for images.", 507)

            return respond(response_dict)

        uuid_path = os.path.join(constants.IMAGE_FOLDER_PATH, uuid)

        with open(uuid_path, "wb") as img:
            img.write(image.stream.read())

        cursor.execute(f"INSERT INTO photos(creator, path, alt_text, post_id) VALUES ('{USER_ID}', '{uuid}', "
                       f"'alt_text', '{post_id}')")
        mysql_conn.connection.commit()

    cursor.close()

    response_dict = create_response(constants.RESPONSE_TYPES.OK)
    return respond(response_dict)


# TODO: register, login
def register():
    response_to_user = Response()
    response_to_user.content_type = "application/json"

