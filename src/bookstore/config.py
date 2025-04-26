import os

"""
Hold the config for the application
"""


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("BOOKSTORE_DATABASE_URL", "sqlite:////Users/vjoshi/PycharmProjects/bookstore/site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
