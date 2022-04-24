import threading
from flask import Response, request
from . import functions
from . import constants
import os
import mysql.connector

# temporarily
USER_ID = 1


def get_database() -> mysql.connector:
    mysql_conn = mysql.connector.connect(
        user=constants.DB_USER,
        password=constants.DB_PASSWORD,
        host=constants.DB_HOST,
        database=constants.DB_DATABASE,
        port=constants.DB_PORT)

    return mysql_conn


def get_category(category_string: str):
    """
    Maps category string to category number related to DB category table
    :param category_string: one out of five strings known for database
    :return: integer defining category
    """
    category_id = -1
    category_id = constants.POST_CATEGORIES.NEWCOMERS if category_string == "newcomers" else category_id
    category_id = constants.POST_CATEGORIES.NEW_PROJECTS if category_string == "new-projects" else category_id
    category_id = constants.POST_CATEGORIES.TOURNAMENTS if category_string == "tournaments" else category_id
    category_id = constants.POST_CATEGORIES.SPORT_CHALLENGES if category_string == "sport-challenges" else category_id
    category_id = constants.POST_CATEGORIES.OTHER_EVENTS if category_string == "other-events" else category_id

    return category_id


def upload(user_request: request) -> Response:
    """
    Uploads new posts to database based on request body. More about DB in README.md in this folder
    :param user_request: Flask request containing information for upload
    :param mysql_conn: MySQL pooled connection
    :return: Flask response
    """
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

    mysql_conn = get_database()
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
    mysql_conn.close()

    response_dict = functions.create_response(constants.RESPONSE_TYPES.OK)
    return functions.respond(response_dict)


def get(user_request: request, category: str) -> Response:
    """
    Returns posts from database based on category. More about DB in README.md in this folder.
    :param user_request: Flask request containing information for return
    :param mysql_conn: MySQL pooled connection
    :param category: one of the five categories
    :return: Flask response
    """
    if user_request.method != "GET":
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "method_not_allowed", "This method is not allowed", 405)
        return functions.respond(response_dict)

    category_id = get_category(category)
    if category_id == -1:
        response_dict = functions.create_response(constants.RESPONSE_TYPES.ERROR, "category_not_set", "Post category was not set.", 400)
        return functions.respond(response_dict)

    mysql_conn = get_database()
    cursor = mysql_conn.cursor()
    cursor.execute(f"SELECT id, title, description, uploaded FROM posts WHERE category_id='{category_id}' ORDER BY uploaded DESC, id DESC LIMIT 10;")
    responses = cursor.fetchall()

    response_dict = {}
    for response in responses:
        response_dict[str(response[0])] = {"title": response[1], "description": response[2], "uploaded_time": response[3].strftime("%Y-%m-%d"), "images": []}

    ids_str = ", ".join(list(response_dict.keys()))
    if ids_str:
        cursor.execute(f"SELECT ph.path, ph.alt_text, ph.max_width, p.id FROM photos ph, posts p WHERE p.id IN ({ids_str}) AND p.id = ph.post_id ORDER BY p.uploaded DESC, p.id DESC, ph.id;")
        responses = cursor.fetchall()

    cursor.close()
    mysql_conn.close()

    for response in responses:
        response_dict[str(response[3])]["images"].append([response[0], response[1], response[2]])

    response_dict = functions.create_response(constants.RESPONSE_TYPES.OK, message=list(response_dict.values()))
    return functions.respond(response_dict)


"""
# TODO: register, login
def register():
    response_to_user = Response()
    response_to_user.content_type = "application/json"
"""
