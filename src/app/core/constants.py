from dotenv import dotenv_values

env_values = dotenv_values("./.env")


class RESPONSE_TYPES:
    OK = 0
    ERROR = 1


class POST_CATEGORIES:
    NEWCOMERS = 1
    NEW_PROJECTS = 2
    TOURNAMENTS = 3
    SPORT_CHALLENGES = 4
    OTHER_EVENTS = 5


UUID_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
UUID_CREATION_TRIES = 10

IMAGE_UUID_LENGTH = 10
IMAGE_FOLDER_PATH = "../assets/images/uploads"


DB_HOST = env_values["DB_HOST"]
DB_USER = env_values["DB_USER"]
DB_PASSWORD = env_values["DB_PASSWORD"]
DB_PORT = int(env_values["DB_PORT"])
DB_DATABASE = env_values["DB_DATABASE"]

DEFAULT_RESPONSE = {
    "status": "OK",
    "errmsg": "",
    "error": "",
    "status_code": 200
}


