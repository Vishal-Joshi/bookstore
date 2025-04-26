from src.bookstore.extensions import db
from src.bookstore.models import Book


class BookService:

    @staticmethod
    def add_book(data):
        book = Book(
            title=data['title'],
            description=data['description'],
            author=data['author'],
            price=data['price']
        )
        db.session.add(book)
        db.session.commit()
        return book

    @staticmethod
    def get_book(title):
        book_with_title = Book.query.filter_by(title=title).first()
        return book_with_title
