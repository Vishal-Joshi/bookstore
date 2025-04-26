from flask import Blueprint
from . import routes  # noqa: F401

book_bp = Blueprint('books', __name__, url_prefix='/books')

