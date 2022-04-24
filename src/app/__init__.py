from flask import Flask, request, Response
from flask_mysqldb import MySQL
from core import api as core_api
import core.constants as constants
import core.functions as functions

app = Flask(__name__)

app.config['MYSQL_HOST'] = constants.DB_HOST
app.config['MYSQL_USER'] = constants.DB_USER
app.config['MYSQL_PASSWORD'] = constants.DB_PASSWORD
app.config['MYSQL_DB'] = constants.DB_DATABASE
app.config['MYSQL_PORT'] = constants.DB_PORT


{"post_title", "description", "date", "images"}

mysql = MySQL(app)

not_found_response = functions.create_response(constants.RESPONSE_TYPES.ERROR, "not_found", "This resource was not found.", 404)
not_found_response = functions.respond(not_found_response)


@app.route("/")
def hello_world():
    return "AA"


@app.route('/api/<user_request>', defaults={'category': None}, methods=["GET", "POST"])
@app.route("/api/<user_request>/<category>", methods=["GET", "POST"])
def api(user_request, category):
    if user_request == "upload":
        return core_api.upload(request, mysql)
    return not_found_response


if __name__ == "__main__":
    app.run(debug=True)
