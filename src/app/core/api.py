from flask import Response, request
from . import functions
from . import constants
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


def get_category(category_string: str):
    category_id = -1
    category_id = constants.POST_CATEGORIES.NEWCOMERS if category_string == "newcomers" else category_id
    category_id = constants.POST_CATEGORIES.NEW_PROJECTS if category_string == "projects" else category_id
    category_id = constants.POST_CATEGORIES.TOURNAMENTS if category_string == "tournaments" else category_id
    category_id = constants.POST_CATEGORIES.SPORT_CHALLENGES if category_string == "sport" else category_id
    category_id = constants.POST_CATEGORIES.OTHER_EVENTS if category_string == "other" else category_id

    return category_id


def upload(user_request: request, mysql_conn: MySQL) -> Response:
    if request.method != "POST":
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "method_not_allowed", "This method is not allowed", 405)
        return functions.respond(response_dict)

    title = mysql_conn.connection.escape_string(user_request.form.get("title")).decode("utf-8")[:40]
    description = mysql_conn.connection.escape_string(user_request.form.get("description")).decode("utf-8")
    category = mysql_conn.connection.escape_string(user_request.form.get("category")).decode("utf-8")

    category_id = get_category(category)

    if category_id == -1:
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "category_not_set", "Post category was not set.", 400)
        return functions.respond(response_dict)

    cursor = mysql_conn.connection.cursor()

    cursor.execute(f"INSERT INTO posts(user_id, category_id, title, description) VALUES ('{USER_ID}', '{category_id}', '{title}', '{description}');")
    mysql_conn.connection.commit()

    cursor.execute(f"SELECT id FROM posts WHERE user_id='{USER_ID}' AND title='{title}' ORDER BY id DESC LIMIT 1;")
    post_id = cursor.fetchall()[0][0]

    for image in user_request.files.getlist("pictures"):
        uuid = functions.create_image_uuid(image)

        if not uuid:
            response_dict = functions.create_response(
              constants.RESPONSE_TYPES.ERROR, "not_enough_uuids", "There are not enough UUIDS for images.", 507)

            return functions.respond(response_dict)

        uuid_path = os.path.join(constants.IMAGE_FOLDER_PATH, uuid)

        with open(uuid_path, "wb") as img:
            img.write(image.stream.read())

        cursor.execute(f"INSERT INTO photos(creator, path, alt_text, post_id) VALUES ('{USER_ID}', '{uuid}', "
                       f"'alt_text', '{post_id}')")
        mysql_conn.connection.commit()

    cursor.close()

    response_dict = functions.create_response(constants.RESPONSE_TYPES.OK)
    return functions.respond(response_dict)


# TODO: register, login
def register():
    response_to_user = Response()
    response_to_user.content_type = "application/json"

