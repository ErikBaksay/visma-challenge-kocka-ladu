from flask import Flask, request
import mysql.connector
from core import api as core_api
import core.constants as constants
import core.functions as functions

app = Flask(__name__)

mysql_conn = mysql.connector.connect(
    user=constants.DB_USER,
    password=constants.DB_PASSWORD,
    host=constants.DB_HOST,
    database=constants.DB_DATABASE,
    port=constants.DB_PORT)

not_found_response = functions.create_response(constants.RESPONSE_TYPES.ERROR, errmsg="not_found", error="This resource was not found.", status_code=404)
not_found_response = functions.respond(not_found_response)


@app.route("/")
def hello_world():
    return "AA"


@app.route('/api/<user_request>', defaults={'category': None}, methods=["GET", "POST"])
@app.route("/api/<user_request>/<category>", methods=["GET", "POST"])
def api(user_request, category):
    if user_request == "upload":
        return core_api.upload(request, mysql_conn)
    if user_request == "get":
        return core_api.get(request, mysql_conn, category)
    return not_found_response


if __name__ == "__main__":
    app.run(debug=True)
    mysql_conn.close()
