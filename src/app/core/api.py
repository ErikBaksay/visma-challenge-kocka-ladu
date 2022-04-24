import threading
from flask import Response, request
from . import functions
from . import constants
import os
import mysql.connector

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


def upload(user_request: request, mysql_conn: mysql.connector) -> Response:
    if user_request.method != "POST":
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "method_not_allowed", "This method is not allowed", 405)
        return functions.respond(response_dict)

    title = user_request.form.get("title")[:40]
    description = user_request.form.get("description")
    category = user_request.form.get("category")

    category_id = get_category(category)

    if category_id == -1:
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "category_not_set", "Post category was not set.", 400)
        return functions.respond(response_dict)

    cursor = mysql_conn.cursor()

    sql = "INSERT INTO posts(user_id, category_id, title, description) VALUES (%s, %s, %s, %s);"
    values = (USER_ID, category_id, title, description, )
    cursor.execute(sql, values)

    mysql_conn.commit()

    sql = "SELECT id FROM posts WHERE user_id=%s AND title=%s ORDER BY id DESC LIMIT 1;"
    values = (USER_ID, title, )
    cursor.execute(sql, values)
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

        sql = "INSERT INTO photos(creator, path, alt_text, post_id) VALUES (%s, %s, 'alt_text', %s)"
        values = (USER_ID, uuid, post_id)
        cursor.execute(sql, values)
        mysql_conn.commit()

        sql = "SELECT id FROM photos WHERE path=%s"
        values = (uuid, )
        cursor.execute(sql, values)
        photo_id = cursor.fetchall()[0][0]
        threading.Thread(target=functions.optimize_images, args=(uuid_path, photo_id, )).start()

    cursor.close()

    response_dict = functions.create_response(constants.RESPONSE_TYPES.OK)
    return functions.respond(response_dict)


def get(user_request: request, mysql_conn: mysql.connector, category: str) -> Response:
    if user_request.method != "GET":
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "method_not_allowed", "This method is not allowed", 405)
        return functions.respond(response_dict)

    category_id = get_category(category)
    if category_id == -1:
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "category_not_set", "Post category was not set.", 400)
        return functions.respond(response_dict)

    cursor = mysql_conn.cursor()
    cursor.execute(f"SELECT id, title, description, uploaded FROM posts WHERE category_id='{category_id}' ORDER BY uploaded DESC, id DESC LIMIT 10;")
    responses = cursor.fetchall()

    response_dict = {}
    for response in responses:
        response_dict[str(response[0])] = {"title": response[1], "description": response[2], "uploaded_time": response[3].strftime("%Y-%m-%d, %H:%M:%S"), "images": []}

    ids_str = ", ".join(list(response_dict.keys()))
    if ids_str:
        cursor.execute(f"SELECT ph.path, ph.alt_text, ph.max_width, p.id FROM photos ph, posts p WHERE p.id IN ({ids_str}) AND p.id = ph.post_id ORDER BY p.uploaded DESC, p.id DESC, ph.id;")
        responses = cursor.fetchall()

    cursor.close()

    for response in responses:
        response_dict[str(response[3])]["images"].append([response[0], response[1], response[2]])

    response_dict = functions.create_response(constants.RESPONSE_TYPES.OK, message=list(response_dict.values()))
    return functions.respond(response_dict)


# TODO: register, login
def register():
    response_to_user = Response()
    response_to_user.content_type = "application/json"

