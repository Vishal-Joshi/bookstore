from flask import request, jsonify, Blueprint

from ..book_service import BookService
from ..models import Book

book_bp = Blueprint('books', __name__, url_prefix='/books')


@book_bp.route('', methods=['POST'])
def add_book():
    data = request.get_json()
    if BookService.get_book(data['title']):
        return jsonify({
            "message": f"book with {data['title']} already exists"
        }), 409
    else:
        book = BookService.add_book(data)
        return jsonify({
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "author": book.author,
            "price": book.price
        }), 201


@book_bp.route('', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])
