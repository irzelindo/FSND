import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True


# Connect to the database
class Config:
    # TODO IMPLEMENT DATABASE URL

    DATABASE_NAME = "fyyur"
    SQLALCHEMY_DATABASE_URI = "postgres://{}:{}@{}/{}".format(
        'postgres', 'postgres', 'localhost:5432', DATABASE_NAME)
