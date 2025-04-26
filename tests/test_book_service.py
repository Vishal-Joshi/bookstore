import pytest

from TestConfig import TestConfig
from src.bookstore import create_app
from src.bookstore.extensions import db
from src.bookstore.models import Book


@pytest.fixture
def app():
    app = create_app(config_object=TestConfig)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()
    yield db
    with app.app_context():
        db.drop_all()


def test_add_book(client, app, init_db):
    # given
    book_data = {
        "title": "book title",
        "description": "some description",
        "author": "Vishal Joshi",
        "price": 10
    }

    # when
    response = client.post('/books', json=book_data)

    # then
    assert response.status_code == 201
    assert response.json['title'] == book_data['title']
    assert response.json['description'] == book_data['description']
    assert response.json['author'] == book_data['author']
    assert response.json['price'] == book_data['price']

    with app.app_context():
        book_in_db = Book.query.filter_by(title=book_data['title']).first()
        assert book_in_db is not None
        assert book_in_db.title == book_data['title']
        assert book_in_db.description == book_data['description']
        assert book_in_db.author == book_data['author']
        assert book_in_db.price == book_data['price']


def test_should_return_bad_request_if_book_with_same_title_exists(client, app, init_db):
    # given
    book_data = {
        "title": "book title",
        "description": "some description",
        "author": "Vishal Joshi",
        "price": 10
    }
    client.post('/books', json=book_data)

    # when
    response = client.post('/books', json=book_data)

    # then
    assert response.status_code == 409
    assert response.json['message'] == f"book with {book_data['title']} already exists"


def test_should_get_all_books(client):
    book_data_1 = {
        'title': "title of book 1",
        'description': "description of book",
        'author': "VJ",
        'price': 10
    }

    book_data_2 = {
        'title': "title of book 2",
        'description': "description of book",
        'author': "VJ",
        'price': 10
    }

    client.post('/books', json=book_data_1)
    client.post('/books', json=book_data_2)

    # when
    response = client.get('/books')

    assert response.status_code == 200
    books = response.get_json()
    assert len(books) == 2
    assert books[0]['title'] == book_data_1['title']
    assert books[1]['title'] == book_data_2['title']


def test_should_be_able_to_get_books_with_specific_id(client):
    # given
    book_data_1 = {
        'title': "title of book 1",
        'description': "description of book",
        'author': "VJ",
        'price': 10
    }

    book_data_2 = {
        'title': "title of book 2",
        'description': "description of book",
        'author': "VJ",
        'price': 10
    }

    book_1_response = client.post('/books',json=book_data_1).get_json()
    book_2_response = client.post('/books',json=book_data_2).get_json()

    # when
    book_1_get_response = client.get(f"/books/{book_1_response['id']}")
    book_2_get_response = client.get(f"/books/{book_2_response['id']}")

    # then
    assert book_1_get_response.status_code == 200
    book1 = book_1_get_response.get_json()
    assert book1['title'] == book_1_response['title']
    book2 = book_2_get_response.get_json()
    assert book2['title'] == book_2_response['title']
