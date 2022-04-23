import random
from . import constants
import os


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
