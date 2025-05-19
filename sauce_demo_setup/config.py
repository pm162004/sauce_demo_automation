import os
from dotenv import load_dotenv

load_dotenv()


class EnvVariables:

    WEB_URL:str = os.getenv("WEB_URL")
    USER_NAME = os.getenv("USER_NAME")
    PASSWORD = os.getenv("PASSWORD")


config = EnvVariables()
