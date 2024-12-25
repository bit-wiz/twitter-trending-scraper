from dotenv import load_dotenv
from os import environ
import json

load_dotenv()


class Config(object):
    DEBUG = True

    with open('config.txt', 'r') as file:
        data = file.read()

    array_of_dicts = json.loads(data)

    COOKIES = array_of_dicts

    MONGO_URI = environ.get("MONGO_URL")
