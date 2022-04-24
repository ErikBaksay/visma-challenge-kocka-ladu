from flask import Flask, request
from flask_mysqldb import MySQL
from core import api as core_api
import core.constants as constants

app = Flask(__name__)

app.config['MYSQL_HOST'] = constants.DB_HOST
app.config['MYSQL_USER'] = constants.DB_USER
app.config['MYSQL_PASSWORD'] = constants.DB_PASSWORD
app.config['MYSQL_DB'] = constants.DB_DATABASE
app.config['MYSQL_PORT'] = constants.DB_PORT

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "AA"


@app.route("/api/<user_request>", methods=["GET", "POST"])
def api(user_request):
    if user_request == "upload":
        return core_api.upload(request, mysql)
    return user_request


if __name__ == "__main__":
    app.run(debug=True)
